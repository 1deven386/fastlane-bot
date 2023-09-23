from .Pool import Pool

class Pool2(Pool):
    abi = [
        {"name":"coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"uint256","name":""}],"stateMutability":"view","type":"function"},
        {"name":"admin_balances","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":""}],"stateMutability":"view","type":"function"}
    ]

    def _sync(self, coins: list[any]):
        self.coins = [coins[n](self.contract.functions.coins(n).call(), self.contract.address) for n in range(len(coins))]
        self.admin_balances = [self.contract.functions.admin_balances(n).call() for n in range(len(coins))]

    def _get_balances(self) -> list[int]:
        return [coin.pool_balance - admin_balance for coin, admin_balance in zip(self.coins, self.admin_balances)]

    A_PREC = 100
    D_FLAG = 1
    Y_FLAG = 1
    P_FLAG = 1
