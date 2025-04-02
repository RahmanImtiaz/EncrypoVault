from enum import Enum

class WalletType(Enum):
    BITCOIN = 1
    ETHEREUM = 2
    UNKNOWN = 999

    @staticmethod
    def from_str(string: str) -> "WalletType":
        match string:
            case "BITCOIN" | "BTC":
                return WalletType.BITCOIN
            case "ETHEREUM" | "ETH":
                return WalletType.ETHEREUM
            case _:
                return WalletType.UNKNOWN

    def __str__(self):
        match self.value:
            case 1:
                return "BTC"
            case 2:
                return "ETH"
            case _:
                return "UNKNOWN"

