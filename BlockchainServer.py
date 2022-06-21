from _thread import *
import threading
import time
import datetime
import socket
import _thread
import json
from Blockchain import Blockchain
from Transaction import Transaction
import hashlib
from sys import argv

IP = "127.0.0.1" # '' -> localhost
mutex = threading.Lock()

# this variable can be used in case of avoiding deadlock
counter = 0
cc = ""

# this variable stores the new proof computed by miner
new_proof = 0


class BlockchainServer(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.id2port = self.args[0]
        self.PORT = list(self.id2port.values())[0]
        self.blockchain = args[1]

    def serverHandler(self, c , addr):

        while(True):
            global counter
            global cc
            global new_proof

            counter += 1

            data_rev = c.recv(1024)
            dataString = data_rev.decode('utf-8')
            typeRequest = dataString[:2]
            clientData = ""

            # Handle tx request
            if typeRequest == 'tx':
                # print("Server receives the tx request from the client.")
                transaction = Transaction()
                transactionContent = transaction.validateTransaction(dataString)
                if transactionContent != None:
                    self.blockchain.addTransaction(transactionContent)
                    clientData = "Accepted"
                else:
                    clientData = "Rejected"

            # Handle pb request
            elif typeRequest == 'pb':
                # print("Server receives the pb request from the client.")
                # print(json.dumps(self.blockchain.blockchain, indent=1, sort_keys=False))
                clientData = str(self.blockchain.blockchain)

            # Handle cc request
            elif typeRequest == 'cc':
                cc = 'cc'
                clientData = "Connection closed!"

            # Handle gp request
            elif typeRequest == 'gp':
                # print("Server has received the gp request.")
                clientData = str(self.blockchain.lastBlock()['proof'])
                # print(clientData)

            # Handle up request (Do it later)
            elif typeRequest == 'up':
                # print("Server receives update.")
                # print(dataString)
                proof_from_miner = int(dataString.split("|")[1])
                # validate the proof from miner and update new_proof
                hash_str = str(proof_from_miner**2 - self.blockchain.lastBlock()['proof']**2).encode()
                if hashlib.sha256(hash_str).hexdigest()[:2] == '00':
                    new_proof = proof_from_miner
                    clientData = "Reward"

                else:
                    clientData = "No reward"

            # Handle hb request
            elif typeRequest == 'hb':
                clientData = str(self.blockchain.blockchain)

            # create a new block if #transactions > 5 and new proof has been updated
            # if transactions > 5 but the new_proof is still the same as the proof of the last block,
            # do nothing, cuz in this case the miner hasn't completed the proof computation yet.
            hash_str = str(new_proof**2 - self.blockchain.lastBlock()['proof']**2).encode()
            if (len(self.blockchain.pool) >= self.blockchain.block_size and 
            hashlib.sha256(hash_str).hexdigest()[:2] == '00'):
                self.blockchain.newBlock(new_proof)

            clientData = bytes(clientData, encoding='utf-8')
            c.sendall(clientData)

            if typeRequest == 'cc':
                break

        c.close()
        return

    def run(self):
        global counter
        global cc
        # try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # print("Blockchain Server start")
            # print("Blockchain Server host names: ", IP, "Port: ",self.PORT)
            s.bind((IP, self.PORT)) # Bind to the port
            s.listen(5)
            while True:
                # to avoid deadlock, counter can be used here: if counter == 6 or cc = 'cc':
                if cc == 'cc':
                    break
                mutex.acquire()
                try:
                    c, addr = s.accept()
                    _thread.start_new_thread(self.serverHandler,(c, addr))
                except error as e:
                    print(e)
                finally:
                    mutex.release()
            s.close()
            return
        # except:
        #     print("Can't connect to the Socket")
