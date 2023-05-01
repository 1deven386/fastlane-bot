# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from fastlane_bot import Config, ConfigDB, ConfigNetwork, ConfigProvider, Bot
from fastlane_bot.tools.cpc import ConstantProductCurve as CPC, CPCContainer
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(CPC))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(Bot))
from fastlane_bot.testing import *
plt.style.use('seaborn-dark')
plt.rcParams['figure.figsize'] = [12,6]
from fastlane_bot import __VERSION__
require("2.0", __VERSION__)

# # Testing the _run functions [NBTest011]

# ## Mainnet Alchemy Configuration

# ### Set up the bot

C = Config.new(config=Config.CONFIG_MAINNET)
assert C.DATABASE == C.DATABASE_POSTGRES
assert C.POSTGRES_DB == "mainnet"
assert C.NETWORK == C.NETWORK_MAINNET
assert C.PROVIDER == C.PROVIDER_ALCHEMY
bot = Bot(ConfigObj=C)
assert str(type(bot.db)) == "<class 'fastlane_bot.db.manager.DatabaseManager'>"

# ### Set up the curves

cc1 = CPC.from_carbon(pair="ETH-EEeE/USDC-eB48", tkny="ETH-EEeE", yint=10, y=10, pa=1/2000, pb=1/2010, cid="c-1")
assert iseq(1/2000, cc1.p, cc1.p_max)
assert iseq(1/2010, cc1.p_min)
assert cc1.p_convention() == 'ETH per USDC'
assert cc1.p_min < cc1.p_max
cc1

cu1 = CPC.from_univ3(pair="ETH-EEeE/USDC-eB48", Pmarg=2100, uniPa=2000, uniPb=2200, 
                     uniL=200*m.sqrt(2100*2100), fee=0, cid="uni1", descr="")
assert iseq(cu1.p, 2100)
assert iseq(cu1.p_min, 2000)
assert iseq(cu1.p_max, 2200)
assert cu1.p_convention() == 'USDC per ETH'
assert cu1.p_min < cu1.p_max
cu1

cu1.p, cc1.p

CCm = CPCContainer([cu1, cc1])
#CCm.plot()

# ### Run `_find_arbitrage_opportunities}`

# #### AO_TOKENS

flt = ['USDC-eB48']
r=bot._find_arbitrage_opportunities(flashloan_tokens=flt, CCm=CCm, result=bot.AO_TOKENS)
r

assert r[0] == {'ETH-EEeE', 'USDC-eB48'}
assert r[1] == [('ETH-EEeE', 'USDC-eB48')]

# #### AO_CANDIDATES [ETH]





flt = ['ETH-EEeE']
r = bot._find_arbitrage_opportunities(flashloan_tokens=flt, CCm=CCm, result=bot.AO_CANDIDATES)
#assert len(r) == 1
#r0, r1, r2, r3, r4 = r[0]

# #### AO_CANDIDATES [USDC]

flt = ['USDC-eB48']
r = bot._find_arbitrage_opportunities(flashloan_tokens=flt, CCm=CCm, result=bot.AO_CANDIDATES)
assert len(r) == 1
r0, r1, r2, r3, r4 = r[0]

assert r0 > 100
r0

assert r1.loc["TOTAL NET"]["ETH-EEeE"] < 1e-5
assert r1.loc["TOTAL NET"]["USDC-eB48"] < -100
r1

r2

assert r3 == flt[0]
r3

r4

# #### Full

r = bot._find_arbitrage_opportunities(flashloan_tokens=flt, CCm=CCm)

r[4]

# ### Run `_run`

# #### XS_ARBOPPS

bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_ARBOPPS)

# #### XS_TI

bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_TI)

# #### XS_ORDSCAL

bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_ORDSCAL)

# #### XS_AGGTI

bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_AGGTI)

# #### XS_ORDTI

bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_ORDTI)

# #### XS_ENCTI

bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_ENCTI)

# #### XS_ROUTE

bot._run(flashloan_tokens=flt, CCm=CCm, result=bot.XS_ROUTE)

