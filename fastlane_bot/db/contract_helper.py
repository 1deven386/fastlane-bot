"""
Helpers for the DB components of the Fastlane project.

(c) Copyright Bprotocol foundation 2023.
Licensed under MIT
"""
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

import requests
from brownie import Contract
from brownie.network.web3 import Web3

from fastlane_bot.data import abi
#import fastlane_bot.config as c
import fastlane_bot.data.abi as _abi


@dataclass
class ContractHelper:
    """
    Helper for contract-related functions in the DB components of the Fastlane project.

    Parameters
    ----------
    web3 : Web3
        web3 instance
    contracts: Dict[str, Contract]
        Dictionary of contract names and their corresponding Contract objects
    exchange_list : List[str]
        List of exchange names
    poll_interval : int
        Polling interval for the event listener

    """

    __VERSION__ = "3.0.1"
    __DATE__ = "04-26-2023"

    w3: Web3
    contracts: Dict[str, Any] = field(default_factory=dict)
    filters: List[Any] = field(default_factory=list)
    exchange_list: List[str] = field(default_factory=list)
    poll_interval: int = c.DEFAULT_POLL_INTERVAL

    def __post_init__(self):
        if c.CARBON_V1_NAME not in self.contracts:
            self.contracts[c.CARBON_V1_NAME] = {}
        if "CARBON_CONTROLLER_CONTRACT" not in self.contracts[c.CARBON_V1_NAME]:
            self.contracts[c.CARBON_V1_NAME]["CARBON_CONTROLLER_CONTRACT"] = self.initialize_contract_with_abi(
                c.CARBON_CONTROLLER_ADDRESS, abi.CARBON_CONTROLLER_ABI
            )
        self.filters = self.get_event_filters(self.exchange_list)

    @property
    def carbon_controller(self) -> Contract:
        """
        Returns the CarbonController contract
        """
        return self.contracts[c.CARBON_V1_NAME]["CARBON_CONTROLLER_CONTRACT"]

    @staticmethod
    def initialize_contract_with_abi(address: str, abi: List[Any]) -> Contract:
        """
        Initialize a contract with an abi

        Parameters
        ----------
        w3 : Web3
            web3 instance
        address : str
            address of the contract
        abi : List[Any]
            abi of the contract

        """
        return w3.eth.contract(address=address, abi=abi)


    @staticmethod
    def initialize_contract_without_abi(address: str, w3: Web3) -> Contract:
        """
        Initialize a contract without an abi

        Parameters
        ----------
        address : str
            address of the contract
        w3 : Web3
            web3 instance

        Returns
        -------
        Contract
            contract instance

        """
        abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={c.ETHERSCAN_TOKEN}"
        _abi = json.loads(requests.get(abi_endpoint).text)
        return w3.eth.contract(address=address, abi=_abi["result"])

    @staticmethod
    def initialize_contract(w3: Web3, address: str, _abi: Optional[List[Any]] = None) -> Contract:
        """
        Initialize a contract with an abi

        Parameters
        ----------
        w3 : Web3
            web3 instance
        address : str
            address of the contract
        abi : List[Any]
            abi of the contract

        """

        if _abi is None:
            return ContractHelper.initialize_contract_without_abi(address=address, w3=w3)
        else:
            return ContractHelper.initialize_contract_with_abi(address=address, abi=_abi, w3=w3)

    @staticmethod
    def contract_from_address(exchange_name: str, pool_address: str) -> Contract:
        """
        Returns the contract for a given exchange and pool address

        Parameters
        ----------
        exchange_name : str
            The name of the exchange
        pool_address : str
            The address of the pool

        Returns
        -------
        Contract
            The contract for the pool

        """

        if exchange_name == c.BANCOR_V2_NAME:
            return ContractHelper.initialize_contract(
                w3=c.w3,
                address=c.w3.toChecksumAddress(pool_address),
                _abi=abi.BANCOR_V2_CONVERTER_ABI,
            )
        elif exchange_name == c.BANCOR_V3_NAME:
            return c.BANCOR_NETWORK_INFO_CONTRACT
        elif exchange_name in c.UNIV2_FORKS:
            return ContractHelper.initialize_contract(
                w3=c.w3,
                address=c.w3.toChecksumAddress(pool_address),
                _abi=abi.UNISWAP_V2_POOL_ABI,
            )
        elif exchange_name == c.UNISWAP_V3_NAME:
            return ContractHelper.initialize_contract(
                w3=c.w3,
                address=c.w3.toChecksumAddress(pool_address),
                _abi=abi.UNISWAP_V3_POOL_ABI,
            )
        elif c.CARBON_V1_NAME in exchange_name:
            return ContractHelper.initialize_contract(
                w3=c.w3,
                address=c.w3.toChecksumAddress(pool_address),
                _abi=abi.CARBON_CONTROLLER_ABI,
            )
        else:
            raise NotImplementedError(f"Exchange {exchange_name} not implemented")

    def get_or_init_contract(self, exchange_name: str, pool_address: str) -> bool:
        """
        Returns whether a contract exists for a given exchange and pool address

        Parameters
        ----------
        exchange_name : str
            The name of the exchange
        pool_address : str
            The address of the pool

        Returns
        -------
        bool
            Whether a contract exists for the given exchange and pool address

        """

        if exchange_name not in self.contracts:
            self.contracts[exchange_name] = {}

        if pool_address not in self.contracts[exchange_name]:
            self.contracts[exchange_name][pool_address] = self.contract_from_address(
                exchange_name, pool_address
            )

        return self.contracts[exchange_name][pool_address]

    def get_contract_for_exchange(
            self, exchange: str = None, pool_address: str = None, init_contract=True
    ) -> Contract:
        """
        Get the relevant ABI for the exchange

        Parameters
        ----------
        exchange : str
            exchange name
        pool_address : str
            pool address
        init_contract : bool
            whether to initialize the contract or not

        Returns
        -------
        Contract
            contract object

        """
        if exchange == c.BANCOR_V2_NAME:
            return c.w3.eth.contract(abi=_abi.BANCOR_V2_CONVERTER_ABI, address=pool_address)

        elif exchange == c.BANCOR_V3_NAME:
            if init_contract:
                return c.w3.eth.contract(
                    abi=_abi.BANCOR_V3_POOL_COLLECTION_ABI,
                    address=c.w3.toChecksumAddress(c.BANCOR_V3_POOL_COLLECTOR_ADDRESS),
                )
            else:
                return c.BANCOR_NETWORK_INFO_CONTRACT

        elif exchange in c.UNIV2_FORKS:
            return c.w3.eth.contract(abi=_abi.UNISWAP_V2_POOL_ABI, address=pool_address)

        elif exchange == c.UNISWAP_V3_NAME:
            return c.w3.eth.contract(abi=_abi.UNISWAP_V3_POOL_ABI, address=pool_address)

        elif c.CARBON_V1_NAME in exchange:
            return c.CARBON_CONTROLLER_CONTRACT

    def get_filters_from_contract_and_exchange(self, exchange_name: str, contract: Contract) -> Any:
        """
        Returns the callable for the event filter for the given exchange

        Parameters
        ----------
        exchange_name : str
            The name of the exchange
        contract : Contract
            The exchange

        Returns
        -------
        Any
            The callable for the event filter
        """
        callables = []
        if c.BANCOR_V2_NAME in exchange_name:
            callables.append(contract.events.TokenRateUpdate)
        elif c.BANCOR_V3_NAME in exchange_name:
            callables.append(contract.events.TradingLiquidityUpdated)
        elif c.UNISWAP_V2_NAME in exchange_name:
            callables.append(contract.events.Sync)
        elif c.UNISWAP_V3_NAME in exchange_name:
            callables.append(contract.events.Swap)
        elif c.SUSHISWAP_V2_NAME in exchange_name:
            callables.append(contract.events.Sync)
        elif c.CARBON_V1_NAME in exchange_name:
            callables.extend(
                (
                    contract.events.StrategyCreated,
                    contract.events.StrategyUpdated,
                    contract.events.StrategyDeleted,
                )
            )
        return callables

    def get_event_filters(self, exchange_name: [str], contract: Contract, latest_block_for_exchange: int) -> Optional[List[Dict[str, Any]]]:
        """
        Creates a _filter for the relevant event for a given exchange

        Parameters
        ----------
        exchange_name: [str]
            The name of the exchange
        contract: Contract
            The exchange
        latest_block_for_exchange: int
            The latest block for the exchange

        Returns
        -------
        filters: [Dict[str, Any]]
            The list of filters for the relevant events
        """
        return [
            {
                "exchange": exchange_name,
                "filter": callable.createFilter(
                    fromBlock=latest_block_for_exchange, toBlock="latest"
                ),
            } for callable in self.get_filters_from_contract_and_exchange(exchange_name, contract)
        ]


