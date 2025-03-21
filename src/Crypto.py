import datetime
from CryptoObserver import CryptoObserver

class Crypto(CryptoObserver):
    def __init__(self, crypto_id : str ):
        self.crypto_id = crypto_id
        self.name = None
        self.symbol = None
        self.image = None
        self.market_cap_rank = None
        self.current_price = None
        self.market_cap = None
        self.market_cap_change_24h = None
        self.market_cap_change_percentage_24h = None
        self.total_volume = None
        self.high_24h = None
        self.low_24h = None
        self.price_change_24h = None
        self.price_change_percentage_24h = None
        self.ath = None
        self.ath_change_percentage = None
        self.ath_date = None
        self.atl = None
        self.atl_change_percentage = None
        self.atl_date = None
        self.max_supply = None
        self.total_supply = None
        self.circulating_supply = None
        self.fully_diluted_valuation = None
        self.last_updated = None

    
    
    def update(self, crypto_id: str, crypto_data: dict):
        if self.crypto_id == crypto_id:
            self.name = crypto_data.get("name")
            self.symbol = crypto_data.get("symbol")
            self.image = crypto_data.get("image")
            self.market_cap_rank = crypto_data.get("market_cap_rank")
            self.current_price = crypto_data.get("current_price")
            self.market_cap = crypto_data.get("market_cap")
            self.market_cap_change_24h = crypto_data.get("market_cap_change_24h")
            self.market_cap_change_percentage_24h = crypto_data.get("market_cap_change_percentage_24h")
            self.total_volume = crypto_data.get("total_volume")
            self.high_24h = crypto_data.get("high_24h")
            self.low_24h = crypto_data.get("low_24h")
            self.price_change_24h = crypto_data.get("price_change_24h")
            self.price_change_percentage_24h = crypto_data.get("price_change_percentage_24h")
            self.ath = crypto_data.get("ath")
            self.ath_change_percentage = crypto_data.get("ath_change_percentage")
            self.ath_date = crypto_data.get("ath_date")
            self.atl = crypto_data.get("atl")
            self.atl_change_percentage = crypto_data.get("atl_change_percentage")
            self.atl_date = crypto_data.get("atl_date")
            self.max_supply = crypto_data.get("max_supply")
            self.total_supply = crypto_data.get("total_supply")
            self.circulating_supply = crypto_data.get("circulating_supply")
            self.fully_diluted_valuation = crypto_data.get("fully_diluted_valuation")
            self.last_updated = crypto_data.get("last_updated")
            
            
            
        
        
        
        
