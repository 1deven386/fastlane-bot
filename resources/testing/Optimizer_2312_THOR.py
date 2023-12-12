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

# +
import numpy as np
import matplotlib.pyplot as plt

from tools.cpc import ConstantProductCurve as CPC, CPCContainer, T, CPCInverter, Pair
from tools.optimizer import CPCArbOptimizer, F, MargPOptimizer, PairOptimizer
from tools.analyzer import CPCAnalyzer
#print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(Pair))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(CPC))
#print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(CPCArbOptimizer))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(MargPOptimizer))
#print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(PairOptimizer))

plt.style.use('seaborn-v0_8-dark')
plt.rcParams['figure.figsize'] = [12,6]
# -

# # Optimizer Testing [202312a-THOR Triangle]
#
# **IMPORTANT NOTE** 
#
# For the above imports to work, you must create a symlink to the `tools` module here, running
#
#     ln -s ../../fastlane_bot/tools tools
#     
# Don't forget to add a local `.gitignore` file in this case!

# ## Reading input data
#
# Set `curves_as_dicts` to the output of `CPCContainer.as_dicts`. The use `CPCContainer.from_dicts` to recreate a container.

curves_as_dicts = [{'k': 4.3078885616238194e+24,
  'x': 1250505254484.4102,
  'x_act': 0,
  'y_act': 344491.8061533139,
  'alpha': 0.5,
  'pair': 'USDC-eB48/THOR-8044',
  'cid': '74181555988764585035015664420125470098056-1',
  'fee': 2000.0,
  'descr': 'carbon_v1 THOR-8044/USDC-eB48 2000',
  'constr': 'carb',
  'params': {'exchange': 'carbon_v1',
   'tknx_dec': 18,
   'tkny_dec': 6,
   'tknx_addr': '0xa5f2211B9b8170F694421f2046281775E8468044',
   'tkny_addr': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
   'blocklud': 18758319,
   'y': 344491.8061533139,
   'yint': 344491.8061533139,
   'A': 0,
   'B': 1.659765242784964,
   'pa': 2.754820936639097,
   'pb': 2.754820936639097}},
 {'k': 1106096356.8039548,
  'x': 2619874.8519412754,
  'x_act': 2619874.8519412754,
  'y_act': 422.1943487049999,
  'alpha': 0.5,
  'pair': 'THOR-8044/WETH-6Cc2',
  'cid': '0xbf1875da0431343b56ec6295f706e257dbe85696e5270a5bdad005d37cc2fd9c',
  'fee': 0.003,
  'descr': 'sushiswap_v2 THOR-8044/WETH-6Cc2 0.003',
  'constr': 'uv2',
  'params': {'exchange': 'sushiswap_v2',
   'tknx_dec': 18,
   'tkny_dec': 18,
   'tknx_addr': '0xa5f2211B9b8170F694421f2046281775E8468044',
   'tkny_addr': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
   'blocklud': 18758340}},
 {'k': 1233376864385.0625,
  'x': 54102579.539405,
  'x_act': 54102579.539405,
  'y_act': 22797.00662861641,
  'alpha': 0.5,
  'pair': 'USDC-eB48/WETH-6Cc2',
  'cid': '0x68bd2250b4b44996e193e9e001f74a5e5a31b31fbd0bb7df34c66eb8da7e6be2',
  'fee': 3000.0,
  'descr': 'uniswap_v2 USDC-eB48/WETH-6Cc2 0.003',
  'constr': 'uv2',
  'params': {'exchange': 'uniswap_v2',
   'tknx_dec': 6,
   'tkny_dec': 18,
   'tknx_addr': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
   'tkny_addr': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
   'blocklud': 18758413}}]

CC = CPCContainer.from_dicts(curves_as_dicts)
len(CC), len(curves_as_dicts)

# ## Analyzis and visualization
#
# Note: THOR ~ 30c

# ### Visualization

CC.plot()

# ### Analysis

sgn = [1,-1,-1]
price = dict()
quote = dict()
for c,s in zip(CC, sgn):
    price[c.pair] = c.p
    quotep = f"{c.tkny} per {c.tknx}" if s > 0 else f"{c.tknx} per {c.tkny}"
    print(f"{c.pair} {s} {(c.p)**s} {quotep}")

price

# ### Carbon curve
#
# Below is the Carbon curve. It **sells THOR** and **buys USDC** at a rate of **0.36 USDC per THOR** (ignoring fees).

p0 = 1/(price["USDC-eB48/THOR-8044"])
p0

print(CC[0].description())

# Ignoring slippage and fees, it is possible to buy and sell THOR AT 0.38 USDC per THOR via the two provided curves.

p1 = 1/(price["USDC-eB48/WETH-6Cc2"] / price["THOR-8044/WETH-6Cc2"])
p1

# That's an arbitrage opportunity (Buy THOR against USDC on Carbon, sell into the arb) of about 5% meaning that at least in small size (ie before slippage) it should work

p1/p0-1

# ### Triangle curves
#
# The triangle curves are the following
#
# - **THOR/WETH** has 422 ETH and 2.6m THOR at a price of 6205 THOR per ETH
# - **WETH/USDC** has 23k ETH and 50m USDC at a price of 2373 USDC per ETH
#
# The implied **THOR** price is 0.382 USDC (memo: on Carbon it is 0.362, and the THOR loading is 344k, ie ~15% of the THOR available on the arb curve)

p1, p0, p1/p0-1, 344/2600

print(CC[1].description())

1/0.0001611505787737007

print(CC[2].description())

1/0.00042136635300378734

# ## Optimizer

# ### Raw run
#
# This is the actual run, using USDC as the arbitrage token. This run does not converge; rather the THOR/USDC price oscillates between 0.38ish and 0.29ish. Note that this is way out of the (imputed) price range for the Carbon range which is very tightly centered around `p0~0.36`
#
# (uncomment the below code to see the debug run)

O = MargPOptimizer(CC)
r = O.optimize("USDC-eB48", params=dict(verbose=False, debug=False))
#O.optimize("USDC-eB48", params=dict(verbose=True, debug=True))
r

# +
#r = O.optimize("USDC-eB48", params=dict(verbose=True, debug=True))
#r
# -

# ### Better prices estimates
#
# We set the initial price for THOR/USD squat into the Carbon range to see whether thise works better. 
#
# TLDR -- it does not. Shame.

price_est = {
    "USDC-eB48": 1,
    "WETH-6Cc2": 2373.2,
    "THOR-8044": p0,
}
price_est

O = MargPOptimizer(CC)
r = O.optimize("USDC-eB48", params=dict(pstart=price_est, verbose=False, debug=False))
#O.optimize("USDC-eB48", params=dict(pstart=price_est, verbose=True, debug=True))
r

# ### Adding a regularization curve
#
# The issue with the convergence is that the Carbon range is very thin, and the gradients from the other curves just jump across it. Unfortunately this happens both ways so we always jump from one side of the curve to the other, without ever converging.
#
# One way to solve this is to add a Uni v2 style curve with the same characteristics (price, mostly) as the Carbon curve. This curve should guide the algo more smoothly back into the Carbon range (provided the v2 curve is big enough to affect the gradient, and not too big to distort the result).
#
# Note the following convergence properties with respect to the `SCALING` parameter (note: both x and y of the initial curve are divided by this factor)
#
# - `SCALING = 60` converges
# - `SCALING = 65` does not converge
#
# **HOWEVER CONVERGENCE DOES NOT LEAD TO THE CORRECT POINT; D_TOKEN [THOR] IS STILL NOT ZERO**

SCALING = 50

c0d = curves_as_dicts[0]
c0d

c0 = CC[0]
c0

c0r = CPC.from_xy(x=c0.x/SCALING, y=c0.y/SCALING, pair=c0.pair)
c0r

1/c0.p, 1/c0r.p

CCr = CPCContainer.from_dicts(curves_as_dicts)
CCr += c0r

CCr.plot()

O = MargPOptimizer(CCr)
r = O.optimize("USDC-eB48", params=dict(verbose=False, debug=False))
#O.optimize("USDC-eB48", params=dict(verbose=True, debug=True))
r

p2 = r.p_optimal["THOR-8044"]
p2

p2/p0-1

r.dtokens

# ### Removing the Carbon curve
#
# Here we check how it converges if we remove the Carbon curve and replace it with a constant product curve of the same (virtual) capacity. Unsurprisingly it does and all dtokens are zero.

c0 = CC[0]
c0b = CPC.from_xy(x=c0.x, y=c0.y, pair=c0.pair)
c0b

CCb = CPCContainer.from_dicts(curves_as_dicts[1:])
CCb += c0b
CCb.plot()

O = MargPOptimizer(CCb)
r = O.optimize("USDC-eB48", params=dict(verbose=False, debug=False))
#O.optimize("USDC-eB48", params=dict(verbose=True, debug=True))
r

r.dtokens


# ## Unit tests

# +
def iseq(arg0, *args, eps=1e-6):
    """checks whether all arguments are equal to arg0, within tolerance eps if numeric"""
    if not args:
        raise ValueError("Must provide at least one arg", args)
    try:
        arg0+1
        isnumeric = True
    except:
        isnumeric = False
    #if isinstance(arg0, int) or isinstance(arg0, float):
    if isnumeric:
        # numeric testing
        if arg0 == 0:
            for arg in args:
                if abs(arg) > eps: 
                    return False
                return True
        for arg in args:
            if abs(arg/arg0-1) > eps:
                return False
            return True
    else:
        for arg in args:
            if not arg == arg0:
                return False
        return True

def raises(func, *args, **kwargs):
    """
    returns exception message if func(*args, **kwargs) raises, else False

    USAGE

        assert raises(func, 1, 3, three=3), "func(1, 2, three=3) should raise"
    """
    try:
        func(*args, **kwargs)
        return False
    except Exception as e:
        return str(e)


# -

# ### min range width functionality

cdata = dict(y=100, yint=100, pa=100, pb=100, pair="WETH/USDC", tkny="USDC")
c  = CPC.from_carbon(**cdata)
c2 = CPC.from_carbon(**cdata, minrw=1e-2)
c4 = CPC.from_carbon(**cdata, minrw=1e-4)
c6 = CPC.from_carbon(**cdata, minrw=1e-6)
c

assert c2.params.minrw==0.01
assert c4.params.minrw==0.0001
assert c6.params.minrw==0.000001
assert c.params.minrw==0.000001

assert iseq(c2.p**2/100**2, 1.01)
assert iseq(c4.p**2/100**2, 1.0001)
assert iseq(c6.p**2/100**2, 1.000001)
assert iseq(c.p, c6.p)

assert iseq(c2.p-100, 0.49875621120, eps=1e-3)
assert iseq(c4.p-100, 0.00499987500, eps=1e-3)
assert iseq(c6.p-100, 0.00004999875, eps=1e-3)
assert iseq((c2.p-100)/(c4.p-100), 99.75373596136635, eps=1e-4)
assert iseq((c4.p-100)/(c6.p-100), 99.99752507444194, eps=1e-4)




