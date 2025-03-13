import abc 

class CryptoObserver(abc.ABC):
    @abc.abstractmethod
    def update(self, crypto):
        pass
    
    
    
