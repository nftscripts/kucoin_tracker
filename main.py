from transactions_parser import Process
from json import load
from time import time

# Created by https://t.me/cryptoscripts

with open('config.json', 'r', encoding='utf-8-sig') as file:
    config = load(file)


def main() -> None:
    start_time = time()
    coin_buyer = Process(start_time, config['etherscan_api'], config['api_key'], config['api_secret'],
                         config['api_passphrase'], config['qty'])
    coin_buyer.run()


if __name__ == '__main__':
    main()
