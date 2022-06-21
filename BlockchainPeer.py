import errno
from operator import imod
from Blockchain import Blockchain
from Transaction import Transaction
from BlockchainServer import BlockchainServer
from BlockchainClient import BlockchainClient
from BlockchainMiner import BlockchainMiner
from socket import error as socket_error
from time import sleep
from sys import argv
import socket
import _thread
import json

HOST = "127.0.0.1"


class BlockchainPeer():
    def __init__(self, *args):
        self.cc = False
        self.args = args
        self.id2port = args[0]
        self.blockchain = Blockchain()
        self.transaction = Transaction()
        self.blockchainServer = BlockchainServer(self.id2port, self.blockchain)
        self.blockchainClient = BlockchainClient(self.id2port, self.blockchain)
        self.blockchainMiner = BlockchainMiner(self.id2port)

    def run(self):
        self.blockchainServer.start()
        sleep(0.1)
        self.blockchainMiner.start()
        sleep(0.1)
        self.blockchainClient.start()

        self.hb()

        print('peer terminated!')
        exit()

    def hb(self):
        while(self.blockchainClient.is_alive()):
            #print('hb') 
            for port in list(self.id2port.values())[1:]:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((HOST, port))
                        mess_data = bytes('hb', encoding= 'utf-8')
                        s.sendall(mess_data)
                        rcv_bc_str = s.recv(8192).decode('utf-8')
                        # convert string to list object
                        rcv_bc_str = rcv_bc_str.replace("'", '"')
                        rcv_bc_str = rcv_bc_str.replace('None', 'null')
                        rcv_bc_obj = json.loads(rcv_bc_str)
                        # accept the longest blockchain, if all chains are at the same length
                        # accept the one with earliest last block's timestamp
                        ts_self_last_block = self.blockchain.blockchain[-1]['timestamp']
                        ts_incoming_last_block = rcv_bc_obj[-1]['timestamp']
                        if( (len(rcv_bc_obj) > len(self.blockchain.blockchain)) or 
                        ((len(rcv_bc_obj) == len(self.blockchain.blockchain)) and 
                        ts_incoming_last_block < ts_self_last_block) ):
                            #print(f'blockchain replaced! {len(rcv_bc_obj)} <= {len(self.blockchain.blockchain)}')
                            self.blockchain.blockchain = rcv_bc_obj
                        s.close()
                except socket_error as e:
                    #print(e)
                    pass
            sleep(5)

# read comment line arguments according to the following format: COMP3221_DiVR.py <node-id> <port-id> <node-config-file>
id = argv[1]
no = int(argv[2])
config_file = open(argv[3])

id2port = {id:no} # A: 6000
num_of_peers = int(config_file.readline().strip())
for i in range(num_of_peers):
    line = config_file.readline().split()
    id2port[line[0]] = int(line[1])
config_file.close()

# print(list(id2port.values()))

blockchainPeer = BlockchainPeer(id2port)
blockchainPeer.run()
