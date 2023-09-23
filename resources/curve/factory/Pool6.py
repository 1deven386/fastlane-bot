from .Pool import Pool

class Pool6(Pool):
    abi = [
        {"name":"coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"int128","name":""}],"stateMutability":"view","type":"function"},
        {"name":"balances","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"int128","name":""}],"stateMutability":"view","type":"function"}
    ]

    def _sync(self, coins: list[any]):
        self.coins = [coins[n](self.contract.functions.coins(n).call()) for n in range(len(coins))]
        self.balances = [self.contract.functions.balances(n).call() for n in range(len(coins))]

    def _get_factors(self, default: int) -> list[int]:
        return [getattr(coin, 'exchangeRateCurrent', default) for coin in self.coins]

    A_PREC = 1
    D_FLAG = 0
    Y_FLAG = 1
    P_FLAG = 1
