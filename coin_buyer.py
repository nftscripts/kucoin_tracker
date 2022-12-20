from kucoin.client import Client
from loguru import logger


class BuyProcess:
    def __init__(self, api_key: str, api_secret: str, api_passphrase: str, qty: float) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.qty = qty
        self.client = Client(self.api_key, self.api_secret, self.api_passphrase)

    def buy_tokens(self) -> None:
        order = self.client.create_market_order(
            symbol=f'FT-USDT',
            side='buy',
            size=str(self.qty))
        order_id = order['orderId']
        self.check_history(order_id)

    def check_history(self, order_id: str) -> None:
        order = self.client.get_order(order_id)
        price = order['price']
        self.get_results(price)

    def get_results(self, price: float) -> None:
        logger.info(f'Bought {self.qty} tokens at a price {price} USDT')
