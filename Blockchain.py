import hashlib
import json
from time import time
from datetime import datetime

class Blockchain():
    def  __init__(self):
        self.blockchain = []
        self.pool = []
        self.block_size = 5
        self.poolLimit = 100
        self.newBlock(previousHash="genesis", proof=100)

    def newBlock(self, proof, previousHash = None):
        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': datetime.ctime(datetime.now()),
            'transaction': self.pool,
            'proof': proof,
            'previousHash': previousHash or self.calculateHash(self.blockchain[-1]),
            'currentHash': self.currentHash(self.pool[:self.block_size])
        }
        self.pool = self.pool[self.block_size:]
        self.blockchain.append(block)

    def lastBlock(self):
        return self.blockchain[-1]

    def calculateHash(self, block):
        blockObject = json.dumps(block, sort_keys=True)
        blockString = blockObject.encode()
        rawHash = hashlib.sha256(blockString)
        hexHash = rawHash.hexdigest()
        return hexHash

    def addTransaction(self, transaction):
        if len(self.pool) < self.poolLimit:
            self.pool.append(transaction)
        lastBlock = self.lastBlock()
        return lastBlock['index'] + 1

    def currentHash(self, pool):
        currentTransactions = ""
        if len(pool) > 0:
            previousHash = self.calculateHash(self.lastBlock())
            currentTransactions += previousHash
            for transaction in pool:
                currentTransactions += transaction
            return hashlib.sha256(currentTransactions.encode()).hexdigest()
