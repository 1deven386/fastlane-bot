from typing import Union, List, Tuple, Any

from fastlane_bot.modes.base_triangle import ArbitrageFinderTriangleBase
from fastlane_bot.tools.cpc import CPCContainer
from fastlane_bot.tools.optimizer import CPCArbOptimizer


class ArbitrageFinderTriangleSingleBancor3(ArbitrageFinderTriangleBase):

    arb_mode = "single_triangle_bancor3"

    def find_arbitrage(
        self, candidates: List[Any] = None, ops: Tuple = None, best_profit: float = 0
    ) -> Union[List, Tuple]:
        """
        Find arbitrage opportunities in a market and returns either a list of candidates or the optimal opportunity.

        Returns:
            list or tuple: If self.result == self.AO_CANDIDATES, it returns a list of candidates.
                           Otherwise, it returns the optimal opportunity.
        """
        if self.base_exchange != "bancor_v3":
            self.ConfigObj.logger.warning(
                f"base_exchange must be bancor_v3 for {self.arb_mode}, setting it to bancor_v3"
            )
            self.base_exchange = "bancor_v3"

        self.ConfigObj.logger.info(
            f"flashloan_tokens for arb_mode={self.arb_mode} will be overwritten. "
        )
        self.flashloan_tokens = self.CCm.byparams(exchange="bancor_v3").tknys()

        if candidates is None:
            candidates = []

        # Get combinations of flashloan tokens
        combos = self.get_combos(
            self.flashloan_tokens, self.CCm, arb_mode=self.arb_mode
        )

        # Get the miniverse combinations
        all_miniverses = self.get_miniverse_combos(combos)

        if len(all_miniverses) == 0:
            return None

        # Check each source token and miniverse combination
        for src_token, miniverse in all_miniverses:
            r = None
            # self.ConfigObj.logger.debug(f"Checking flashloan token = {src_token}, miniverse = {miniverse}")

            try:
                # Run main flow with the new set of curves
                (
                    profit_src,
                    trade_instructions,
                    trade_instructions_df,
                    trade_instructions_dic,
                ) = self.run_main_flow(miniverse, src_token)

                # Get the cids of the carbon pools
                carbon_cids = [
                    curve.cid
                    for curve in miniverse
                    if curve.params.get("exchange") == "carbon_v1"
                ]

                if carbon_cids:

                    # Get the new set of curves
                    new_curves = self.get_mono_direction_carbon_curves(
                        miniverse=miniverse, trade_instructions_df=trade_instructions_df
                    )

                    # Rerun main flow with the new set of curves
                    (
                        profit_src,
                        trade_instructions,
                        trade_instructions_df,
                        trade_instructions_dic,
                    ) = self.run_main_flow(new_curves, src_token)
            except Exception:
                continue

            # Get the candidate ids
            cids = [ti["cid"] for ti in trade_instructions_dic]

            # Calculate the profit
            profit = self.calculate_profit(src_token, profit_src, self.CCm, cids)

            if str(profit) == "nan":
                self.ConfigObj.logger.debug("profit is nan, skipping")
                continue

            # Handle candidates based on conditions
            candidates += self.handle_candidates(
                best_profit,
                profit,
                trade_instructions_df,
                trade_instructions_dic,
                src_token,
                trade_instructions,
            )

            # Find the best operations
            best_profit, ops = self.find_best_operations(
                best_profit,
                ops,
                profit,
                trade_instructions_df,
                trade_instructions_dic,
                src_token,
                trade_instructions,
            )

        return candidates if self.result == self.AO_CANDIDATES else ops

    def run_main_flow(self, miniverse, src_token):

        # Instantiate the container and optimizer objects
        CC_cc = CPCContainer(miniverse)
        O = CPCArbOptimizer(CC_cc)

        # Perform the optimization
        r = O.margp_optimizer(src_token)

        # Get the profit in the source token
        profit_src = -r.result

        # Get trade instructions in different formats
        trade_instructions_df = r.trade_instructions(O.TIF_DFAGGR)
        trade_instructions_dic = r.trade_instructions(O.TIF_DICTS)
        trade_instructions = r.trade_instructions()

        return (
            profit_src,
            trade_instructions,
            trade_instructions_df,
            trade_instructions_dic,
        )

    def get_miniverse_combos(self, combos: List[Tuple]) -> List[Tuple]:
        """
        Get the miniverse combinations for a list of token pairs.

        Parameters
        ----------
        combos : list
            List of token pairs.

        Returns
        -------
        list
            List of miniverse combinations.

        """
        all_miniverses = []
        for tkn0, tkn1 in combos:
            external_curves = self.CCm.bypairs(f"{tkn0}/{tkn1}")
            external_curves += self.CCm.bypairs(f"{tkn1}/{tkn0}")
            external_curves = list(set(external_curves))
            carbon_curves = [
                curve
                for curve in external_curves
                if curve.params.get("exchange") == "carbon_v1"
            ]
            external_curves = [
                curve
                for curve in external_curves
                if curve.params.get("exchange") != "carbon_v1"
            ]
            if not external_curves and not carbon_curves:
                continue

            bancor_v3_curve_0 = (
                self.CCm.bypairs(f"BNT-FF1C/{tkn0}")
                .byparams(exchange="bancor_v3")
                .curves
            )
            bancor_v3_curve_1 = (
                self.CCm.bypairs(f"BNT-FF1C/{tkn1}")
                .byparams(exchange="bancor_v3")
                .curves
            )
            if bancor_v3_curve_0 is None or bancor_v3_curve_1 is None:
                continue
            if len(bancor_v3_curve_0) == 0 or len(bancor_v3_curve_1) == 0:
                continue

            miniverses = []
            if external_curves:
                for curve in external_curves:
                    miniverses += [bancor_v3_curve_0 + bancor_v3_curve_1 + [curve]]
            if carbon_curves:
                miniverses += [bancor_v3_curve_0 + bancor_v3_curve_1 + carbon_curves]

            if len(miniverses) > 0:
                all_miniverses += list(zip(["BNT-FF1C"] * len(miniverses), miniverses))
        return all_miniverses
