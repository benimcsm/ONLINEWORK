import threading
import time
from web3 import Web3

rpc_provider = "https://eth-mainnet.rpcfast.com?api_key=LWjUac1dHfJ65VELcqWkyyYFX32SomDNj2GM5B3f7WFNbGdhYG9aUwyTaWT6Up45"
w3 = Web3(Web3.HTTPProvider(rpc_provider))

private_key = "8db522ede4d99313125e1cbc04872b2b3380b4716ae57862325e1cd62d0c6933"
pub_key = "0xEB08d9B6b0df98D858244e9b518D43e2D39e2082"
recipient_pub_key = "0xE1ed80c934e38eEAbcE9369c257641205D1975B2"

def loop(w3_instance):
    while True:
        balance = w3_instance.eth.get_balance(pub_key)
        print()
        print(f"Balance: {balance}")

        # Dynamically get the current gas price
        gas_price = w3_instance.eth.gas_price
        print(f"Current Gas Price: {w3_instance.from_wei(gas_price, 'gwei')} Gwei")

        gas_limit = 21000
        nonce = w3_instance.eth.get_transaction_count(pub_key)

        tx = {
            'chainId': 1,
            'nonce': nonce,
            'to': recipient_pub_key,
            'value': balance - gas_limit * gas_price,
            'gas': gas_limit,
            'gasPrice': gas_price
        }

        try:
            if balance > 0:
                signed_tx = w3_instance.eth.account.sign_transaction(tx, private_key)
                tx_hash = w3_instance.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"Transaction Hash: {w3_instance.toHex(tx_hash)}")
        except:
            print("Insufficient funds or error in transaction")

        # Introduce a delay (sleep) between iterations
        time.sleep(0.01)  

threading.Thread(target=loop, args=(w3,), daemon=True).start()
input('Press Enter to exit.')

