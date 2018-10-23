import json
from web3 import Web3, HTTPProvider
from settings import *

class Contract:
    DEFAULT_GAS_PRICE = 21000000000
    DEFAULT_GAS = 1000000

    web3 = Web3(HTTPProvider(INFURA_LINK))

    def __init__(self):
        contractAddress = Web3.toChecksumAddress(CONTRACT_ADDRESS)
        with open('storage.json', 'r') as abiDefinition:
            abiStorage = json.load(abiDefinition)
        self.ethereumPublicKey = Web3.toChecksumAddress(PUBLIC_KEY)
        self.ethereumPrivateKey = PRIVATE_KEY
        self.contract = self.web3.eth.contract(
            address = contractAddress,
            abi = abiStorage
        )

    def _buildTx(self):
        tx = self.contract.buildTransaction({
            'gasPrice': self.DEFAULT_GAS_PRICE,
            'gas': self.DEFAULT_GAS,
            'nonce': self.web3.eth.getTransactionCount(self.ethereumPublicKey)
        })
        return tx

    def _ethTransaction(self, tx):
        signed = self.web3.eth.account.signTransaction(
            tx,
            private_key = self.ethereumPrivateKey
        )
        result = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = None
        while receipt == None:
            receipt = self.web3.eth.getTransactionReceipt(result)
        if receipt.get('status') == 1:
            return True
        else:
            return False
