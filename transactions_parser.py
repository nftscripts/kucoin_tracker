from kucoin.exceptions import KucoinAPIException
from requests import get
from time import sleep
from loguru import logger
from coin_buyer import BuyProcess


class Process:
    def __init__(self,
                 start_time: float,
                 etherscan_api: str,
                 api_key: str,
                 api_secret: str,
                 api_passphrase: str,
                 qty: float) -> None:

        self.start_time = start_time
        self.etherscan_api = etherscan_api
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.qty = qty
        self.base_url = 'https://api.etherscan.io/api'
        self.address = '0x3Aec3113a09627Af7C9039954D8592fF0bC20c25'
        self.abi_selector = '0xb0d3ec4d'
        self.bought = False

    def make_api_url(self, module: str, action: str, address: str, **kwargs) -> str:
        url = self.base_url + f'?module={module}&action={action}&address={address}&apikey={self.etherscan_api}'

        for key, value in kwargs.items():
            url += f'&{key}={value}'

        return url

    def get_transactions(self) -> None:
        get_transactions_url = self.make_api_url('account', 'txlist', self.address, startblock=0, endblock=99999999999,
                                                 page=1,
                                                 offset=10000, sort='asc')
        response = get(get_transactions_url)
        data = response.json()['result']

        for tx in data:
            selector = tx['input']
            selector = selector[:len(self.abi_selector)]
            time = tx['timeStamp']
            tx_hash = tx['hash']
            if selector == self.abi_selector and self.start_time < float(time):
                logger.info('Found transaction')
                logger.info('txHash:', tx_hash)
                token_buyer = BuyProcess(self.api_key, self.api_secret, self.api_passphrase, self.qty)
                token_buyer.buy_tokens()
                self.bought = True

    def run(self) -> None:
        logger.info('Waiting for transaction...')
        while not self.bought:
            try:
                self.get_transactions()
                sleep(1)
            except KucoinAPIException as ex:
                logger.error(f'Invalid API data | {ex}')
                break
            except Exception as ex:
                print(ex)
                sleep(1)
                continue
