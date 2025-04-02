import abc


class HandlerInterface(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def create_wallet(self):
        pass

    @abc.abstractmethod
    def get_address(self):
        pass