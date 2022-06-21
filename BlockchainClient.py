from _thread import *
import threading
from time import sleep
import socket
from socket import error as socket_error
import _thread
from sys import argv
import json

HOST = "127.0.0.1"
mutex = threading.Lock()


class BlockchainClient(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.id2port = self.args[0]
        self.PORT = list(self.id2port.values())[0]
        self.timer = None
        self.blockchain = args[1]

    def run(self):
        mutex.acquire()

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Create a socket object
                s.connect((HOST, self.PORT))
                # print("Client connected")

                while(True):
                    # Parser for input command
                    commandContent = input("Please enter your command: ")
                    content = commandContent.split(" ")
                    commandType = content[0]

                    # Process command
                    if commandType == 'tx':
                        if len(content) != 3:
                            print("Invalid transaction!")
                            continue
                        else:
                            requestContent = f"tx|{str(content[1])}|{str(content[2])}"
                            # propagate tx request to the network
                            for port in list(self.id2port.values())[1:]:
                                try:
                                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                                        s2.connect((HOST, port))
                                        mess_data = bytes(requestContent, encoding= 'utf-8')
                                        s2.sendall(mess_data)
                                        # print("1")
                                        data_rev = s2.recv(1024)
                                        # print("2")
                                        dataString = data_rev.decode('utf-8')
                                        # print(dataString)
                                        s2.close()
                                except socket_error as e:
                                    continue

                            # print(requestContent)
                    elif commandType == 'pb':
                        if len(content) != 1:
                            print("Invalid arguments for pb request!")
                            continue
                        else:
                            requestContent = "pb"
                    elif commandType == 'cc':
                        if len(content) != 1:
                            print("Invalid arguments for cc request!")
                            continue
                        else:
                            requestContent = "cc"
                    else:
                        print("Please enter the supported request: ")
                        print("tx sender content -- [tx: command type of transaction] [sender of transaction] [content of transaction]")
                        print("pb -- [pb: command type of Print Blockchain]")
                        print("cc -- [cc: command type of Close Connection]")
                        continue

                    # Create message for sending to Blockchain server
                    mess_data = bytes(requestContent, encoding= 'utf-8')
                    s.sendall(mess_data)

                    # Parse response from blockchain server
                    data_rev = s.recv(8192)
                    dataString = data_rev.decode('utf-8')
                    if not data_rev:
                        print("didn't get data")
                    if commandType == 'pb':
                        print(json.dumps(dataString, indent=2, sort_keys=False))
                    elif commandType == 'cc':
                        print(dataString)
                        break
                    else:
                        print(dataString)

                s.close()
        except error as e:
            print(e)
            print("Can't connect to the Blockchain server")
        finally:
            mutex.release()
