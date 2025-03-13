
class Wallet:
    def __init__(self, name: str):
        self.balance = 0.0
        self.address = None
        self.name = name
        self.watch = None


    def link_to_watch(self, watch):
        if self.watch is not None and self in self.watch.wallets:
            self.watch.wallets.remove(self)
        self.watch = watch
        if watch is not None and self not in watch.wallets:
            watch.wallets.append(self)
            
            
            