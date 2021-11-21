from web3 import Web3
from web3.exceptions import TransactionNotFound
from web3.middleware import geth_poa_middleware
import time
import json

def wait_receipt(web3, tx, retries=10, timeout=5):
    for _ in range(0, retries):
        try:
            receipt = web3.eth.getTransactionReceipt(tx)
        except TransactionNotFound:
            receipt = None
        if receipt is not None:
            return receipt
        time.sleep(timeout)  # pragma: no cover
    raise TransactionNotFound(f"Transaction with hash: {tx} not found.")


api_url = "https://eth-goerli.alchemyapi.io/v2/<redacted>"


w3 = Web3(Web3.HTTPProvider(api_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

account = "0x63aA45A9b95c49Ff8E2ffB9E8dC65A48f377c4A5"
priv_key = "<redacted>"
bank_address = "0x046D90F1614C3732Ce04D866bc9Ef0ae1Cdda509" # Blockbusters
HAKToken_address = "0xBefeeD4CB8c6DD190793b1c97B72B60272f3EA6C"
HAKToken_abi = json.loads("""[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"STARTING_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]""")
HAKToken = w3.eth.contract(
	address = HAKToken_address,
	abi = HAKToken_abi
)
bank_abi = json.loads("""[{"inputs":[{"internalType":"address","name":"_priceOracle","type":"address"},{"internalType":"address","name":"_hakToken","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newCollateralRatio","type":"uint256"}],"name":"Borrow","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"liquidator","type":"address"},{"indexed":true,"internalType":"address","name":"accountLiquidated","type":"address"},{"indexed":true,"internalType":"address","name":"collateralToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountOfCollateral","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountSentBack","type":"uint256"}],"name":"Liquidate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"remainingDebt","type":"uint256"}],"name":"Repay","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"authorizedFlashloanUser","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"borrow","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"}],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"address","name":"_account","type":"address"}],"name":"getCollateralRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"hakToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"address","name":"_account","type":"address"}],"name":"liquidate","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"priceOracle","outputs":[{"internalType":"contract IPriceOracle","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"repay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"requestFlashloan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"},{"internalType":"bool","name":"_authorized","type":"bool"}],"name":"setFlashloanUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]""")
bank = w3.eth.contract(
	address = bank_address,
	abi = bank_abi
)

print(w3.isConnected())

print(bank.functions.getBalance(HAKToken_address).call())

threshold = 300 * 10 ** 18
max = 200
amount = 20 * 10**18 # Has to be more than our interest

nonce = w3.eth.get_transaction_count(account)
gasPrice = int(w3.eth.gasPrice * 2)
tx = HAKToken.functions.approve(bank_address, amount*max).buildTransaction({
	'gas': 200000,
	'gasPrice': gasPrice,
	'from': account,
	'nonce': nonce
})  

signed_tx = w3.eth.account.signTransaction(tx, private_key=priv_key)
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

last_block = w3.eth.blockNumber
print("approve() called on block", w3.eth.blockNumber, ".")

receipt = wait_receipt(w3, tx_hash)
print(receipt)


counter = 0

while HAKToken.functions.balanceOf(bank_address).call() > threshold and counter < max:
	nonce = w3.eth.get_transaction_count(account)
	gasPrice = int(w3.eth.gasPrice * 2)
	tx = bank.functions.withdraw(HAKToken_address, amount).buildTransaction({
		'gas': 200000,
		'gasPrice': gasPrice,
		'from': account,
		'nonce': nonce
    })  
	
	signed_tx = w3.eth.account.signTransaction(tx, private_key=priv_key)
	tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
	
	last_block = w3.eth.blockNumber
	print("withdraw() called on block", w3.eth.blockNumber, ".")
	
	receipt = wait_receipt(w3, tx_hash)
	print(receipt)
	
	
	nonce = w3.eth.get_transaction_count(account)
	gasPrice = int(w3.eth.gasPrice * 2)
	tx = bank.functions.deposit(HAKToken_address, amount).buildTransaction({
		'gas': 200000,
		'gasPrice': gasPrice,
		'from': account,
		'nonce': nonce
    })
	signed_tx = w3.eth.account.signTransaction(tx, private_key=priv_key)
	tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

	print("deposit() called on block", w3.eth.blockNumber, ".")
	
	receipt = wait_receipt(w3, tx_hash)
	print(receipt)
	
	time.sleep(45)
	counter += 1
