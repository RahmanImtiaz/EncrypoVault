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

