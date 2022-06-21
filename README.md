This is a **P2P Blockchain System in Python** for **COMP3221 Assignment 2**, developed by Group16.

---

## Pre-requisites
1. Python 3.x installed

## Instructions to run
1. Unzip this file and cd to the directory of the corresponding folder.

2. Under the project directory, open at least 3 terminal windows. At each window, type this command to initialize a new peer in the network:

    python3 BlockchainPeer.py {Peer-id} {Port-no} {Peer-config-file}

An example of this looks like 'python3 BlockchainPeer.py A 6000 config_A.txt', note that the Peer-id, Port-no and Peer-config-file of a peer are fixed and are given in the Peer-config-files. In this case, each window corresponds to the client interface of a peer in the blockchain network.

3. Send requests through command line interfaces (e.g. pb, tx, cc), make sure to send 'cc' to close the connection to a peer at the end.

4. type the following command to terminate the whole blockchain network:

    kill -9 $(ps -A | grep python | awk '{print $1}')

## Remark
You can modify the network by modifying config files, but to run the default network defined by the 4 default config files, you should open 4 differnet windows and in each window, type one of the following 4 commands:

    python3 BlockchainPeer.py A 6000 config_A.txt
    python3 BlockchainPeer.py B 6001 config_B.txt
    python3 BlockchainPeer.py C 6002 config_C.txt
    python3 BlockchainPeer.py D 6003 config_D.txt

## Developers
- Scarlett Hu
- Jiamin Lin
