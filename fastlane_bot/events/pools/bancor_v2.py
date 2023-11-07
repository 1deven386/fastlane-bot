# coding=utf-8
"""
Contains the pool class for bancor v2. This class is responsible for handling bancor v2 pools and updating the state of the pools.

(c) Copyright Bprotocol foundation 2023.
Licensed under MIT
"""
from dataclasses import dataclass
from typing import Dict, Any, List

from web3 import Web3
from web3.contract import Contract

from fastlane_bot.events.pools.base import Pool


@dataclass
class BancorV2Pool(Pool):
    """
    Class representing a Bancor v2 pool.
    """

    exchange_name: str = "bancor_v2"

    @staticmethod
    def unique_key() -> str:
        """
        see base class.
        """
        return "address"

    @classmethod
    def event_matches_format(
        cls, event: Dict[str, Any], static_pools: Dict[str, Any]
    ) -> bool:
        """
        Check if an event matches the format of a Bancor v2 event.

        Parameters
        ----------
        event : Dict[str, Any]
            The event arguments.

        Returns
        -------
        bool
            True if the event matches the format of a Bancor v3 event, False otherwise.

        """
        event_args = event["args"]
        return "_rateN" in event_args

    def update_from_event(
        self, event_args: Dict[str, Any], data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        **** IMPORTANT ****
        Bancor V2 pools emit 3 events per trade. Only one of them contains the new token balances we want.
        The one we want is the one where _token1 and _token2 match the token addresses of the pool.
        """
        token0 = self.state.index.get_level_values("tkn0_address").tolist()[0]
        token1 = self.state.index.get_level_values("tkn1_address").tolist()[0]
        if (
            token0 == event_args["args"]["_token1"]
            and token1 == event_args["args"]["_token2"]
        ):
            data["tkn0_balance"] = event_args["args"]["_rateD"]
            data["tkn1_balance"] = event_args["args"]["_rateN"]
        elif (
            token0 == event_args["args"]["_token2"]
            and token1 == event_args["args"]["_token1"]
        ):
            data["tkn0_balance"] = event_args["args"]["_rateN"]
            data["tkn1_balance"] = event_args["args"]["_rateD"]
        else:
            data["tkn0_balance"] = self.state["tkn0_balance"].iloc[0]
            data["tkn1_balance"] = self.state["tkn1_balance"].iloc[0]

        self.update_pool_state_from_data(data)

        data["anchor"] = self.state["anchor"].iloc[0]
        data["cid"] = self.state.index.get_level_values("cid").tolist()[0]
        data["fee"] = self.state["fee"].iloc[0]
        data["fee_float"] = self.state["fee_float"].iloc[0]
        data["exchange_name"] = self.state.index.get_level_values(
            "exchange_name"
        ).tolist()[0]
        return data

    async def update_from_contract(
        self,
        contract: Contract,
        tenderly_fork_id: str = None,
        w3_tenderly: Web3 = None,
        w3: Web3 = None,
        tenderly_exchanges: List[str] = None,
    ) -> Dict[str, Any]:
        """
        See base class.
        """
        reserve0, reserve1 = await contract.caller.reserveBalances()
        tkn0_address, tkn1_address = await contract.caller.reserveTokens()
        fee = await contract.caller.conversionFee()

        params = {
            "fee": fee,
            "fee_float": fee / 1e6,
            "exchange_name": self.state.index.get_level_values(
                "exchange_name"
            ).tolist()[0],
            "address": self.state["address"].values[0],
            "anchor": await contract.caller.anchor(),
            "tkn0_balance": reserve0,
            "tkn1_balance": reserve1,
            "tkn0_address": tkn0_address,
            "tkn1_address": tkn1_address,
        }
        self.update_pool_state_from_data(params)
        return params
