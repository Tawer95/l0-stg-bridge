import time
from termcolor import cprint

from web3 import Account, Web3
from bridge.eth_bridge import swap_eth_arbitrum_optimism, swap_eth_optimism_arbitrum, get_balance_eth_arbitrum, get_balance_eth_optimism


def main(tr):
    with open('keys.txt', 'r') as keys_file:
        accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
        count = 0
        for _ in range(0, tr):
            count += 1
            cprint(f'\n=============== start :  {count} round ===============', 'white')
            for account in accounts:
                cprint(f'\n=============== start : {account.address} wallet ===============', 'white')

                arbitrum_balance = get_balance_eth_arbitrum(account.address)
                optimism_balance = get_balance_eth_optimism(account.address)

                if arbitrum_balance + optimism_balance < Web3.to_wei(0.01, 'ether'):
                    continue

                if arbitrum_balance > optimism_balance:
                    print("Swapping ETH from Arbitrum to Optimism...")
                    arbitrum_to_optimism_txs_hash = swap_eth_arbitrum_optimism(account=account, amount=arbitrum_balance - Web3.to_wei(0.005, 'ether'))
                    print("Waiting for the swap to complete...")
                    time.sleep(20)
                    print(f"Transaction: https://arbiscan.io/tx/{arbitrum_to_optimism_txs_hash.hex()}")
                else:
                    print("Swapping ETH from Optimism to Arbitrum...")
                    optimism_to_arbitrum_txs_hash = swap_eth_optimism_arbitrum(account=account, amount=optimism_balance - Web3.to_wei(0.005, 'ether'))
                    print("Waiting for the swap to complete...")
                    time.sleep(20)
                    print(f"Transaction: https://optimistic.etherscan.io/tx/{optimism_to_arbitrum_txs_hash.hex()}")

                print("Sleeping 60 seconds for the next account")
                time.sleep(60)

            print("Sleeping 60 seconds for the next cycle")
            time.sleep(60)


if __name__ == '__main__':
    
    cprint(f'\n============================================= Crypto-Selkie ===================================================', 'cyan')
    cprint(f'\n========================== !! Честно спиздил скрипт у скамера, пацаны, и переделал !! =========================', 'light_red')

    cprint(f'\n ------------------------------------- subscribe : https://t.me/tawer_crypt -------------------------------------', 'yellow')

    total_rounds = 1
    main(total_rounds)
    cprint(f'\n============================================= DONE ===================================================', 'green')
