# ------------------------------------------------------------
# Auto generated test file `test_020_E2ETenderly.py`
# ------------------------------------------------------------
# source file   = NBTest_020_E2ETenderly.py
# test id       = 020
# test comment  = E2ETenderly
# ------------------------------------------------------------



from fastlane_bot import Config, ConfigDB, ConfigNetwork, ConfigProvider
from fastlane_bot.bot import CarbonBot
from fastlane_bot.tools.cpc import ConstantProductCurve as CPC, CPCContainer, T
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(CPC))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(CarbonBot))
from fastlane_bot.testing import *
plt.style.use('seaborn-dark')
plt.rcParams['figure.figsize'] = [12,6]
from fastlane_bot import __VERSION__
require("3.0", __VERSION__)




# ------------------------------------------------------------
# Test      020
# File      test_020_E2ETenderly.py
# Segment   Execution [NOTEST]
# ------------------------------------------------------------
def notest_execution():
# ------------------------------------------------------------
    
    # ### Configuration
    #
    # - `flt`: flashloanable tokens
    # - `loglevel`: `LL_DEBUG` , `LL_INFO` `LL_WARN` `LL_ERR`
    
    flt = [T.USDC]
    C = Config.new(config=Config.CONFIG_TENDERLY, loglevel=Config.LL_INFO)
    
    bot = CarbonBot(ConfigObj=C)
    
    # ### Database update [Tenderly specific]
    
    # provided here for convenience; must be commented out for tests
    bot.update(drop_tables=True, top_n=10, only_carbon=False)
    
    # ### Execution
    
    bot.run(flashloan_tokens=flt, mode=bot.RUN_SINGLE)
    

# ------------------------------------------------------------
# Test      020
# File      test_020_E2ETenderly.py
# Segment   Execution analysis [NOTEST]
# ------------------------------------------------------------
def notest_execution_analysis():
# ------------------------------------------------------------
    
    CCm = bot.get_curves()
    
    # ### Arbitrage opportunities
    
    ops = bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_ARBOPPS)
    ops
    
    # ### Route struct
    
    try:
        route_struct = bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_ROUTE)
    except bot.NoArbAvailable as e:
        print(f"[NoArbAvailable] {e}")
        route_struct = None
    route_struct
    
    # ### Orderering info
    
    try:
        ordinfo = bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_ORDINFO)
        flashloan_amount = ordinfo[1]
        flashloan_token_address = ordinfo[2]
        print(f"Flashloan: {flashloan_amount} [{flashloan_token_address}]")
    except bot.NoArbAvailable as e:
        print(f"[NoArbAvailable] {e}")
        ordinfo = None
    ordinfo
    

# ------------------------------------------------------------
# Test      020
# File      test_020_E2ETenderly.py
# Segment   Market analysis [NOTEST]
# ------------------------------------------------------------
def notest_market_analysis():
# ------------------------------------------------------------
    
    # ### Overall market
    
    exch0 = {c.P("exchange") for c in CCm}
    print("Number of curves:", len(CCm))
    print("Number of tokens:", len(CCm.tokens()))
    #print("Exchanges:", exch0)
    print("---")
    for xc in exch0:
        print(f"{xc+':':16} {len(CCm.byparams(exchange=xc)):4}")
    
    # ### Pair
    
    pair = f"{T.ECO}/{T.USDC}"
    
    CCp = CCm.bypairs(pair)
    exch = {c.P("exchange") for c in CCp}
    print("pair:           ", pair)
    print("curves:         ", len(CCp))
    print("exchanges:      ", exch)
    for xc in exch:
        c = CCp.byparams(exchange=xc)[0]
        print(f"{xc+':':16} {c.p:.4f} {1/c.p:.4f}")
    

# ------------------------------------------------------------
# Test      020
# File      test_020_E2ETenderly.py
# Segment   Technical [NOTEST]
# ------------------------------------------------------------
def notest_technical():
# ------------------------------------------------------------
    
    # ### Validation and assertions
    
    assert C.DATABASE == C.DATABASE_POSTGRES
    assert C.POSTGRES_DB == "tenderly"
    assert C.NETWORK == C.NETWORK_TENDERLY
    assert C.PROVIDER == C.PROVIDER_TENDERLY
    assert str(type(bot.db)) == "<class 'fastlane_bot.db.manager.DatabaseManager'>"
    assert C.w3.provider.endpoint_uri.startswith("https://rpc.tenderly.co/fork/")
    assert bot.db.carbon_controller.address == '0xC537e898CD774e2dCBa3B14Ea6f34C93d5eA45e1'
    
    # ### Tenderly shell commands
    #
    # Run those commands in a shell if there are Tenderly connection issues
    
    C_nw = ConfigNetwork.new(network=ConfigNetwork.NETWORK_TENDERLY)
    c1, c2 = C_nw.shellcommand().splitlines()
    print(c1)
    print(c2)
    # !{c1}
    # !{c2}
    
    
    
    