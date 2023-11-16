from sys import argv
from decimal import Decimal
from factory import connect
from factory import make_pool
from factory import pool_names

if len(argv) > 1:
    connect(argv[1])
else:
    exit('HTTP Provider URL Required')

for pool_name in pool_names:
    print(f'{pool_name}:')
    pool = make_pool(pool_name, read_init=True)
    for s, t in [(s, t) for s in pool.coins for t in pool.coins if s != t]:
        s_amount = int(Decimal('123.456') * 10 ** s.decimals)
        t_amount = pool.swap_read(s.symbol, t.symbol, s_amount)
        s_output = f'{Decimal(s_amount) / 10 ** s.decimals} {s.symbol}'
        t_output = f'{Decimal(t_amount) / 10 ** t.decimals} {t.symbol}'
        print(f'- {s_output} --> {t_output}')
