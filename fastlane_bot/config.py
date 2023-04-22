"""
Config file for FastLane project

(c) Copyright Bprotocol foundation 2023.
Licensed under MIT
"""
import logging
import os
from decimal import Decimal

from brownie import Contract
from dotenv import load_dotenv

from fastlane_bot.abi import (
    BANCOR_V3_NETWORK_INFO_ABI,
    CARBON_CONTROLLER_ABI,
    FAST_LANE_CONTRACT_ABI,
)
from fastlane_bot.networks import EthereumNetwork

load_dotenv()

# DEFAULT VALUES SECTION
#######################################################################################
DEFAULT_NETWORK = "mainnet"
DEFAULT_NETWORK_NAME = "Mainnet (Tenderly)"
DEFAULT_NETWORK_PROVIDER = "alchemy"
BACKEND = "postgres"  # "sqlite" or "postgres"
DEFAULT_EXECUTE_MODE = "continuous"  # "continuous" or "single"
PROJECT_PATH = os.path.normpath(f"{os.getcwd()}")
DATABASE_SEED_FILE = os.path.normpath(
    f"{PROJECT_PATH}/fastlane_bot/data/seed_token_pairs.csv"
)
TENDERLY_FORK = (
    "c0d1f990-c095-476f-80a9-72ac65092aae"  # leave blank or fill with your own fork
)
UNIV3_FEE_LIST = [100, 500, 3000, 10000]
MIN_BNT_LIQUIDITY = 2_000_000_000_000_000_000
DEFAULT_GAS = 950_000
DEFAULT_GAS_PRICE = 0
DEFAULT_GAS_PRICE_OFFSET = 1.05
DEFAULT_GAS_SAFETY_OFFSET = 25_000
VERBOSE = "INFO"
DEFAULT_BLOCKTIME_DEVIATION = 13 * 500  # 10 block time deviation
DEFAULT_MIN_PROFIT = Decimal("1")
DEFAULT_MAX_SLIPPAGE = Decimal("1")  # 1%
DEFAULT_CURVES_DATAFILE = os.path.normpath(f"{PROJECT_PATH}/carbon/data/curves.csv.gz")
CARBON_STRATEGY_CHUNK_SIZE = 200
Q96 = Decimal("2") ** Decimal("96")
DEFAULT_TIMEOUT = 60
CARBON_FEE = Decimal("0.002")
BANCOR_V3_FEE = Decimal("0.0")
DEFAULT_REWARD_PERCENT = Decimal("0.5")

# COMMONLY USED TOKEN ADDRESSES SECTION
#######################################################################################
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
MKR_ADDRESS = "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2"
LINK_ADDRESS = "0x514910771AF9Ca656af840dff83E8264EcF986CA"
WBTC_ADDRESS = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
ETH_ADDRESS = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
BNT_ADDRESS = "0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C"
WETH_ADDRESS = WETH9_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

# FACTORY, CONVERTER, AND CONTROLLER ADDRESSES
#######################################################################################
BANCOR_V3_NETWORK_INFO_ADDRESS = "0x8E303D296851B320e6a697bAcB979d13c9D6E760"
UNISWAP_V2_FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
UNISWAP_V2_ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
SUSHISWAP_FACTORY_ADDRESS = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
UNISWAP_V3_FACTORY_ADDRESS = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
BANCOR_V3_POOL_COLLECTOR_ADDRESS = "0xB67d563287D12B1F41579cB687b04988Ad564C6C"
BANCOR_V2_CONVERTER_REGISTRY_ADDRESS = "0xC0205e203F423Bcd8B2a4d6f8C8A154b0Aa60F19"
FASTLANE_CONTRACT_ADDRESS = "0x41Eeba3355d7D6FF628B7982F3F9D055c39488cB"
CARBON_CONTROLLER_ADDRESS = "0xC537e898CD774e2dCBa3B14Ea6f34C93d5eA45e1"
CABON_CONTROLLER_VOUCHER = "0x3660F04B79751e31128f6378eAC70807e38f554E"
MULTICALL_CONTRACT_ADDRESS: str = "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696"

# ACCOUNTS SECTION
#######################################################################################
BINANCE8_WALLET_ADDRESS = "0xF977814e90dA44bFA03b6295A0616a897441aceC"
BINANCE14_WALLET_ADDRESS = "0x28c6c06298d514db089934071355e5743bf21d60"

# ETHEREUM MAINNET CONFIGURATION SECTION
#######################################################################################
PRODUCTION_NETWORK = "mainnet"
PRODUCTION_NETWORK_NAME = "Mainnet (Alchemy)"
ETHERSCAN_TOKEN = os.environ.get("ETHERSCAN_TOKEN")
WEB3_ALCHEMY_PROJECT_ID = os.environ.get("WEB3_ALCHEMY_PROJECT_ID")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
ETH_PRIVATE_KEY_BE_CAREFUL = os.environ.get("ETH_PRIVATE_KEY_BE_CAREFUL")

# URL SECTION
#######################################################################################
ALCHEMY_API_URL = f"https://eth-mainnet.g.alchemy.com/v2/{WEB3_ALCHEMY_PROJECT_ID}"
TENDERLY_FORK_RPC = f"https://rpc.tenderly.co/fork/{TENDERLY_FORK}"
ETHEREUM_MAINNET_PROVIDER = (
    f"https://eth-mainnet.alchemyapi.io/v2/{WEB3_ALCHEMY_PROJECT_ID}"
)
COINGECKO_URL = "https://tokens.coingecko.com/uniswap/all.json"

# EXCHANGE IDENTIFIERS SECTION
#######################################################################################
ETHEREUM_BLOCKCHAIN_NAME = "Ethereum"
BANCOR_V2_NAME = "bancor_v2"
BANCOR_V3_NAME = "bancor_v3"
UNISWAP_V2_NAME = "uniswap_v2"
UNISWAP_V3_NAME = "uniswap_v3"
SUSHISWAP_V2_NAME = "sushiswap_v2"
CARBON_V1_NAME = "carbon_v1"
EXCHANGE_IDS = {
    BANCOR_V2_NAME: 1,
    BANCOR_V3_NAME: 2,
    UNISWAP_V2_NAME: 3,
    UNISWAP_V3_NAME: 4,
    SUSHISWAP_V2_NAME: 5,
    CARBON_V1_NAME: 6,
}
UNIV2_FORKS = [UNISWAP_V2_NAME, SUSHISWAP_V2_NAME]
SUPPORTED_EXCHANGES = [
    BANCOR_V2_NAME,
    BANCOR_V3_NAME,
    UNISWAP_V2_NAME,
    UNISWAP_V3_NAME,
    SUSHISWAP_V2_NAME,
    CARBON_V1_NAME,
]

# SUPPORTED TOKENS SECTION
#######################################################################################
TEST_TOKENS = [
    "BNT",
    "USDC",
    "USDT",
    "DAI",
    "WBTC",
    "WETH",
    "LINK",
    "AAVE",
]

# TOKENS THAT CAN BE FLASHLOANED, DENOTED AS TICKER-ADDRESS(LAST 4 CHARS)
FLASHLOAN_TOKENS = [
    "BNT-FF1C",
    "USDC-EB48",
    "WETH-6CC2",
    "WBTC-C599",
    "USDT-1ec7",
    "DAI-1d0F",
    "LINK-86CA",
]

# CARBON EVENTS
#######################################################################################
CARBON_POOL_CREATED = f"{CARBON_V1_NAME}_PoolCreated"
CARBON_STRATEGY_CREATED = f"{CARBON_V1_NAME}_StrategyCreated"
CARBON_STRATEGY_DELETED = f"{CARBON_V1_NAME}_StrategyDeleted"
CARBON_STRATEGY_UPDATED = f"{CARBON_V1_NAME}_StrategyUpdated"
CARBON_TOKENS_TRADED = f"{CARBON_V1_NAME}_TokensTraded"

# ETHEREUM NETWORK CONNECTION SECTION
#######################################################################################
if DEFAULT_NETWORK == "mainnet":
    network_id = PRODUCTION_NETWORK
    network_name = PRODUCTION_NETWORK_NAME
    provider_url = ETHEREUM_MAINNET_PROVIDER
else:
    network_id = DEFAULT_NETWORK
    network_name = DEFAULT_NETWORK_NAME
    provider_url = TENDERLY_FORK_RPC

connection = EthereumNetwork(
    network_id=network_id,
    network_name=network_name,
    provider_url=provider_url,
    provider_name="alchemy",
)

connection.connect_network()
w3 = connection.web3

FASTLANE_CONTRACT_ADDRESS = w3.toChecksumAddress(FASTLANE_CONTRACT_ADDRESS)

# SMART CONTRACT INSTANTIATION SECTION
#######################################################################################
BANCOR_NETWORK_INFO_CONTRACT = Contract.from_abi(
    name=BANCOR_V3_NAME,
    address=BANCOR_V3_NETWORK_INFO_ADDRESS,
    abi=BANCOR_V3_NETWORK_INFO_ABI,
)
CARBON_CONTROLLER_CONTRACT = Contract.from_abi(
    name=CARBON_V1_NAME,
    address=CARBON_CONTROLLER_ADDRESS,
    abi=CARBON_CONTROLLER_ABI,
)
BANCOR_ARBITRAGE_CONTRACT = w3.eth.contract(
    address=w3.toChecksumAddress(FASTLANE_CONTRACT_ADDRESS),
    abi=FAST_LANE_CONTRACT_ABI,
)

# LOGGER SETUP SECTION
#######################################################################################
def get_logger(verbose: str = "INFO") -> logging.Logger:
    """
    Returns a logger with the specified logging level

    Args:
        verbose (str): The desired logging level. Defaults to "INFO".

    Returns:
        logging.Logger: A logger object with the specified logging level.
    """
    log_level = getattr(logging, verbose.upper())
    logger = logging.getLogger("fastlane")
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = get_logger(VERBOSE)
