from _thread import *
import threading
import socket
import _thread
import sys
import json
import hashlib
from time import sleep

HOST = "127.0.0.1"
mutex = threading.Lock()


class BlockchainMiner(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.id2port = self.args[0]
        self.PORT = list(self.id2port.values())[0]
        self.previous_proof = None

    def run(self):
        # global previous_proof
        mutex.acquire()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, self.PORT))
                # print("Blockchain Miner start")
                while(True):

                    sleep(1)
                    # send gp to server every 1 sec
                    msg = bytes('gp', encoding= 'utf-8')
                    s.sendall(msg)
                    # Parse response from blockchain server
                    # should be the proof of the last block
                    data_rev = s.recv(1024)
                    dataString = data_rev.decode('utf-8')
                    # print("Miner receives msg from server")

                    if not data_rev:
                        print("Miner didn't get data")
                    
                    if not dataString.isdigit():
                        continue

                    # If the proof of the last block is changed
                    # the miner immediately run the algorithm to find a new proof
                    # and send the new proof to the server
                    if self.previous_proof != int(dataString):
                        # print("Print dataString:", int(dataString))
                        # print(int(dataString))
                        self.previous_proof = int(dataString)
                        new_proof = self.proof_of_work(int(dataString))
                        proof_msg = bytes("up|"+str(new_proof), encoding= 'utf-8')
                        s.sendall(proof_msg)
                s.close()
        except error as e:
            print(e)
        finally:
            mutex.release()

    # find a new proof
    def proof_of_work(self, previous_proof):
        new_proof = 0
        # print("Miner starts proving.")
        while(1):
            hash_str = str(new_proof**2 - previous_proof**2).encode()
            # print("hash_str successed")
            hexHash = hashlib.sha256(hash_str).hexdigest()
            # print("hexHash successed")
            if hexHash[:2] != '00':
                new_proof += 1
                continue
            else:
                break
        # print("Miner has found the new proof.")
        return new_proof
