# Imports
import os
import requests
from dotenv import load_dotenv
load_dotenv()
from bip44 import Wallet
from web3 import Web3, middleware,Account
from web3.gas_strategies.time_based import medium_gas_price_strategy

web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Creating Account Instatnce
def generate_account(web3):
    mnemonic = os.getenv("MNEMONIC")
    wallet = Wallet(mnemonic)
    private, public = wallet.derive_account("eth")
    account = Account.privateKeyToAccount(private)
    return account

# Creating ether balance 
def get_balance(w3, address):
    wei_balance = w3.eth.get_balance(address)
    ether = w3.fromWei(wei_balance, "ether")
    return ether

# Sending Transaction
def send_transaction(w3, account, to, wage):
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
    value = w3.toWei(wage, "ether")
    gasEstimate = w3.eth.estimateGas(
        {"to": to, "from": account.address, "value": value}
    )
    raw_tx = {
        "to": to,
        "from": account.address,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": 0,
        "nonce": w3.eth.getTransactionCount(account.address),
    }
    signed_tx = account.signTransaction(raw_tx)
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)