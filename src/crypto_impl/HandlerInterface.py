import abc


class HandlerInterface(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def create_wallet(self):
        pass