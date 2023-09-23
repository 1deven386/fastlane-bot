from .Pool import Pool

class Pool4(Pool):
    abi = [
        {"name":"coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"uint256","name":""}],"stateMutability":"view","type":"function"},
        {"name":"balances","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":""}],"stateMutability":"view","type":"function"}
    ]

    def _sync(self, coins: list[any]):
        self.coins = [coins[n](self.contract.functions.coins(n).call()) for n in range(len(coins))]
        self.balances = [self.contract.functions.balances(n).call() for n in range(len(coins))]

    A_PREC = 100
    D_FLAG = 0
    Y_FLAG = 1
    P_FLAG = 0
