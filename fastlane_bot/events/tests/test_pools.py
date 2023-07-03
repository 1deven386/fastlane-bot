import pytest

from ..pools import SushiswapPool, UniswapV2Pool, UniswapV3Pool, BancorV3Pool, CarbonV1Pool


# Use pytest's fixtures to setup data for tests
@pytest.fixture
def setup_data():
    # The setup data here is the event data you provided
    return {
        "uniswap_v2_event": {'args': {'reserve0': 10941658708636, 'reserve1': 10971030461349}, 'event': 'Sync', 'logIndex': 255, 'transactionIndex': 115, 'transactionHash': '0xecca41359219ee5a0e73652d1bea48bdc73216f294e865416da3f27232fee6e8', 'address': '0x3041CbD36888bECc7bbCBc0045E3B1f144466f5f', 'blockHash': '0x859b0803d75c861baa46e4e02be794187fd9a28a048f19ca148ff7f22e80c8ff', 'blockNumber': 17613636},
        "sushiswap_v2_event": {'args': {'reserve0': 6543521908014628725401090, 'reserve1': 2535973648121313922634}, 'event': 'Sync', 'logIndex': 93, 'transactionIndex': 38, 'transactionHash': '0xc7c0560a8829fb43e05003ef07de8ce682167bb8a16a5e73d832a6a15513dace', 'address': '0x4A86C01d67965f8cB3d0AAA2c655705E64097C31', 'blockHash': '0xefc338e7672291a889029a206f93a50feba92ba7be9e1210f382d79cf2fc9972', 'blockNumber': 17613685},
        "uniswap_v3_event": {'args': {'sender': '0x0000000000a84D1a9B0063A910315C7fFA9Cd248', 'recipient': '0x0000000000a84D1a9B0063A910315C7fFA9Cd248', 'amount0': 1001531661949054480779, 'amount1': -1560777208046492502, 'sqrtPriceX96': 3141136922601321808510033604, 'liquidity': 27271279776041947233926, 'tick': -64559}, 'event': 'Swap', 'logIndex': 48, 'transactionIndex': 4, 'transactionHash': '0x2063e741127ec1a61b03f5c1e01a5ba83c695606e56b8b705b69f0218c6433f4', 'address': '0xcBcC3cBaD991eC59204be2963b4a87951E4d292B', 'blockHash': '0xc4c2ffbf7e0a2b94721eee92a8acaed343d2f332bcd83bf0b66d63b826d78cf6', 'blockNumber': 17613637},
        "bancor_v3_event": {'args': {'pool': '0x4691937a7508860F876c9c0a2a617E7d9E945D4B', 'tkn_address': '0x4691937a7508860F876c9c0a2a617E7d9E945D4B', 'prevLiquidity': 2969054758119920810356648, 'newLiquidity': 2981332708522538339515032}, 'event': 'TradingLiquidityUpdated', 'logIndex': 35, 'transactionIndex': 4, 'transactionHash': '0x2063e741127ec1a61b03f5c1e01a5ba83c695606e56b8b705b69f0218c6433f4', 'address': '0xB67d563287D12B1F41579cB687b04988Ad564C6C', 'blockHash': '0xc4c2ffbf7e0a2b94721eee92a8acaed343d2f332bcd83bf0b66d63b826d78cf6', 'blockNumber': 17613637},

        "carbon_v1_event_create_for_update": {"args": {"owner": "0x11B1785D9Ac81480c03210e89F1508c8c115888E", "id": 340282366920938463463374607431768211699, "token0": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", "token1": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "order0": [0, 0, 0, 0], "order1": [0, 0, 0, 0]}, "event": "StrategyCreated", "logIndex": 378, "transactionIndex": 157, "transactionHash": "0x78aeca0f0f6263a93b5f6208241e302a1994ad614968fa161ca072727b9a5f4b", "address": "0xC537e898CD774e2dCBa3B14Ea6f34C93d5eA45e1", "blockHash": "0x5d9484d50eaf69a1c5715e0a52b58a3d362bce09ff5517bc43ff6fe2cfa2965f", "blockNumber": 17613884},
        "carbon_v1_event_create_for_delete": {'args': {'owner': '0x1f660f4C9e0c833520eEfE7e207249B3Fa7DB92F', 'token0': '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', 'token1': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'id': 1701411834604692317316873037158841057369, 'order0': (250000000000000000, 250000000000000000, 0, 4414201427359729), 'order1': (446009466, 446009466, 0, 10901478971)}, 'event': 'StrategyCreated', 'logIndex': 454, 'transactionIndex': 158, 'transactionHash': '0x6e2ee77bb751644a1f0f693f4e7b2547be495d5473b378b36b58a8c72ba92421', 'address': '0xC537e898CD774e2dCBa3B14Ea6f34C93d5eA45e1', 'blockHash': '0x898cd767e25952ae0a2de3714efb6406846702815bb8f77cdbea5824a0e1d6ff', 'blockNumber': 17614185},

        "carbon_v1_event_update": {"args": {"id": 340282366920938463463374607431768211699, "token0": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", "token1": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "order0": [22815419571180453234, 30000000000000000000, 80181217415, 6293971818901], "order1": [64052264601120813405051, 64052264601120813405051, 164724635005760, 1875443170982464], "reason": 1}, "event": "StrategyUpdated", "logIndex": 378, "transactionIndex": 157, "transactionHash": "0x78aeca0f0f6263a93b5f6208241e302a1994ad614968fa161ca072727b9a5f4b", "address": "0xC537e898CD774e2dCBa3B14Ea6f34C93d5eA45e1", "blockHash": "0x5d9484d50eaf69a1c5715e0a52b58a3d362bce09ff5517bc43ff6fe2cfa2965f", "blockNumber": 17613884},

        "carbon_v1_event_delete": {'args': {'owner': '0x1f660f4C9e0c833520eEfE7e207249B3Fa7DB92F', 'token0': '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', 'token1': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'id': 1701411834604692317316873037158841057369, 'order0': (250000000000000000, 250000000000000000, 0, 4414201427359729), 'order1': (446009466, 446009466, 0, 10901478971)}, 'event': 'StrategyDeleted', 'logIndex': 454, 'transactionIndex': 158, 'transactionHash': '0x6e2ee77bb751644a1f0f693f4e7b2547be495d5473b378b36b58a8c72ba92421', 'address': '0xC537e898CD774e2dCBa3B14Ea6f34C93d5eA45e1', 'blockHash': '0x898cd767e25952ae0a2de3714efb6406846702815bb8f77cdbea5824a0e1d6ff', 'blockNumber': 17614185},
        "carbon_v1_event_create": {"args": {"owner": "0x11B1785D9Ac81480c03210e89F1508c8c115888E", "token0": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", "token1": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "id": 1701411834604692317316873037158841057529, "order0": [0, 0, 3041871764463936, 4414201427359729], "order1": [383896420, 383896420, 235894417, 11805182669]}, "event": "StrategyCreated", "logIndex": 227, "transactionIndex": 89, "transactionHash": "0x8f6ee587bd72cfa8a1a3faf165825c528df8a587827f182f099deed71c998b75", "address": "0xC537e898CD774e2dCBa3B14Ea6f34C93d5eA45e1", "blockHash": "0x7fcc4a119651992df2fd94d7d8c33f895c2076480badf5ccc6b08e78e053f8fe", "blockNumber": 17599450}
    }

def test_uniswap_v2_pool(setup_data):
    uniswap_v2_pool = UniswapV2Pool()
    uniswap_v2_pool.update_from_event(setup_data["uniswap_v2_event"], {'cid': '0x', 'fee': '0.000', 'fee_float': 0.0, 'exchange_name': 'sushiswap_v2', 'reserve0': setup_data["uniswap_v2_event"]["args"]["reserve0"],
                                                                       'reserve1': setup_data["uniswap_v2_event"]["args"]["reserve1"], 'tkn0_symbol': 'tkn0', 'tkn1_symbol': 'tkn1'})
    assert uniswap_v2_pool.state["tkn0_balance"] == setup_data["uniswap_v2_event"]["args"]["reserve0"]
    assert uniswap_v2_pool.state["tkn1_balance"] == setup_data["uniswap_v2_event"]["args"]["reserve1"]

def test_sushiswap_v2_pool(setup_data):
    sushiswap_v2_pool = SushiswapPool()
    sushiswap_v2_pool.update_from_event(setup_data["sushiswap_v2_event"], {'cid': '0x', 'fee': '0.000', 'fee_float': 0.0, 'exchange_name': 'uniswap_v2', 'reserve0': setup_data["uniswap_v2_event"]["args"]["reserve0"],
                                                                       'reserve1': setup_data["uniswap_v2_event"]["args"]["reserve1"], 'tkn0_symbol': 'tkn0', 'tkn1_symbol': 'tkn1'})
    assert sushiswap_v2_pool.state["tkn0_balance"] == setup_data["sushiswap_v2_event"]["args"]["reserve0"]
    assert sushiswap_v2_pool.state["tkn1_balance"] == setup_data["sushiswap_v2_event"]["args"]["reserve1"]

def test_uniswap_v3_pool(setup_data):
    uniswap_v3_pool = UniswapV3Pool()
    uniswap_v3_pool.update_from_event(setup_data["uniswap_v3_event"], {'cid': '0x', 'fee': '0.000', 'fee_float': 0.0, 'exchange_name': 'uniswap_v3', 'liquidity': setup_data["uniswap_v3_event"]["args"]["liquidity"],
                                                                       'sqrtPriceX96': setup_data["uniswap_v3_event"]["args"]["sqrtPriceX96"], 'tick': setup_data["uniswap_v3_event"]["args"]["tick"], 'tkn0_symbol': 'tkn0', 'tkn1_symbol': 'tkn1'})
    assert uniswap_v3_pool.state["liquidity"] == setup_data["uniswap_v3_event"]["args"]["liquidity"]
    assert uniswap_v3_pool.state["sqrt_price_q96"] == setup_data["uniswap_v3_event"]["args"]["sqrtPriceX96"]
    assert uniswap_v3_pool.state["tick"] == setup_data["uniswap_v3_event"]["args"]["tick"]

def test_bancor_v3_pool(setup_data):
    bancor_v3_pool = BancorV3Pool()
    bancor_v3_pool.update_from_event(setup_data["bancor_v3_event"], {'cid': '0x', 'fee': '0.000', 'fee_float': 0.0, 'exchange_name': 'bancor_v3', 'tkn0_balance': setup_data["bancor_v3_event"]["args"]["newLiquidity"], 'tkn1_balance': 0, 'tkn0_symbol': 'tkn0', 'tkn1_symbol': 'tkn1'})
    assert bancor_v3_pool.state["tkn0_balance"] == setup_data["bancor_v3_event"]["args"]["newLiquidity"]

def test_carbon_v1_pool_update(setup_data):
    carbon_v1_pool = CarbonV1Pool()

    # assert that the strategy already exists and has 0 balances
    carbon_v1_pool.update_from_event(setup_data["carbon_v1_event_create_for_update"], {})
    assert setup_data["carbon_v1_event_update"]["args"]["id"] == carbon_v1_pool.state["cid"]
    assert carbon_v1_pool.state["y_0"] == 0
    assert carbon_v1_pool.state["z_0"] == 0
    assert carbon_v1_pool.state["A_0"] == 0
    assert carbon_v1_pool.state["B_0"] == 0
    assert carbon_v1_pool.state["y_1"] == 0
    assert carbon_v1_pool.state["z_1"] == 0
    assert carbon_v1_pool.state["A_1"] == 0
    assert carbon_v1_pool.state["B_1"] == 0

    # update the strategy with new balances
    carbon_v1_pool.update_from_event(setup_data["carbon_v1_event_update"], {})
    assert carbon_v1_pool.state["y_0"] == setup_data["carbon_v1_event_update"]["args"]["order0"][0]
    assert carbon_v1_pool.state["z_0"] == setup_data["carbon_v1_event_update"]["args"]["order0"][1]
    assert carbon_v1_pool.state["A_0"] == setup_data["carbon_v1_event_update"]["args"]["order0"][2]
    assert carbon_v1_pool.state["B_0"] == setup_data["carbon_v1_event_update"]["args"]["order0"][3]
    assert carbon_v1_pool.state["y_1"] == setup_data["carbon_v1_event_update"]["args"]["order1"][0]
    assert carbon_v1_pool.state["z_1"] == setup_data["carbon_v1_event_update"]["args"]["order1"][1]
    assert carbon_v1_pool.state["A_1"] == setup_data["carbon_v1_event_update"]["args"]["order1"][2]
    assert carbon_v1_pool.state["B_1"] == setup_data["carbon_v1_event_update"]["args"]["order1"][3]

def test_carbon_v1_pool_delete(setup_data):
    carbon_v1_pool = CarbonV1Pool()

    # assert that the strategy already exists and has non-zero balances
    carbon_v1_pool.update_from_event(setup_data["carbon_v1_event_create_for_delete"], {})
    assert setup_data["carbon_v1_event_delete"]["args"]["id"] == carbon_v1_pool.state["cid"]
    assert carbon_v1_pool.state["y_0"] == setup_data["carbon_v1_event_delete"]["args"]["order0"][0]
    assert carbon_v1_pool.state["z_0"] == setup_data["carbon_v1_event_delete"]["args"]["order0"][1]
    assert carbon_v1_pool.state["A_0"] == setup_data["carbon_v1_event_delete"]["args"]["order0"][2]
    assert carbon_v1_pool.state["B_0"] == setup_data["carbon_v1_event_delete"]["args"]["order0"][3]
    assert carbon_v1_pool.state["y_1"] == setup_data["carbon_v1_event_delete"]["args"]["order1"][0]
    assert carbon_v1_pool.state["z_1"] == setup_data["carbon_v1_event_delete"]["args"]["order1"][1]
    assert carbon_v1_pool.state["A_1"] == setup_data["carbon_v1_event_delete"]["args"]["order1"][2]
    assert carbon_v1_pool.state["B_1"] == setup_data["carbon_v1_event_delete"]["args"]["order1"][3]

    # delete the strategy
    carbon_v1_pool.update_from_event(setup_data["carbon_v1_event_delete"], {})
    assert carbon_v1_pool.state["y_0"] == 0
    assert carbon_v1_pool.state["z_0"] == 0
    assert carbon_v1_pool.state["A_0"] == 0
    assert carbon_v1_pool.state["B_0"] == 0
    assert carbon_v1_pool.state["y_1"] == 0
    assert carbon_v1_pool.state["z_1"] == 0
    assert carbon_v1_pool.state["A_1"] == 0
    assert carbon_v1_pool.state["B_1"] == 0
