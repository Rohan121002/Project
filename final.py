import hashlib
import json
import random
import time
import datetime
import merkle_tree
from uuid import uuid4
import pyqrcode
import png
from pyqrcode import QRCode
from progress.bar import Bar
from alive_progress import alive_bar
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import rsa

class Blockchain(object):
    # Constructor
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.users = {}
        self.product_history = {}
        self.node_id = 1
        self.prod_ctr = 1

    # Create user
    def create_user(self):
        print()
        self.mine = 0
        try:
            user_type = int(input("Enter 1 if user is Distributor or 2 if user is client"))
            uid = int(input("Enter the user id of user "))
            miner = str(input("Enter the name of the node: "))
            stake = int(input("Enter the amount which you want to stake")) 
            (pubkey, __privkey) = rsa.newkeys(1024)
            if not (len(self.users)== 0):
                for id in self.users:
                    if id==uid:
                        print("The user id already exist. Please try again!")
                        return
                    
            # prod_num = int(
            #     input("Enter the number of products owned by the node: "))
            prodcut = {}
            # for _ in range(prod_num):
            #     pid = int(input("Enter the Product id: "))
            #     pnum = int(input(f"Enter the number of product with pid {pid}: "))
            #     prodcut[pid]=pnum
            #     self.product_history[pid] = {
            #         'Owner': [uid],
            #         'History': []
            #     }
            self.users[uid] = {
                'ID': uid,
                'Type': user_type,
                'Name': miner,
                'Number of Products': 0,
                'Products owned': prodcut,
                # 'Time_received': timestamp,
                'Stake': stake,
                'Public_Key':pubkey,
                'Private_Key':__privkey,
                # (pubkey, privkey) : rsa.newkeys(512)
            }
            self.mine = 1
            print("The node was added to the blockchain\n")
            print(self.users[uid]['Name'] + "'s ID is " +
                  str(self.users[uid]['ID']) + "\n")
        except:
            print("Enter the correct format of data required to add a new node!\n")

    # Create New Block
    def create_new_block(self, previous_hash=None):
        mtree = merkle_tree.MerkleTree(self.hash(self.transactions[:3]))
        if (len(self.chain) == 0):
            block = {
                "Header": {
                    "Index": len(self.chain) + 1,
                    "Timestamp": datetime.datetime.now(),
                    "Merkle root": mtree.getRootHash(),
                    "previous_hash": 0,
                },
                "Transaction": self.transactions[:3]  # 3 transactions
            }
        else:
            block = {
                "Header": {
                    "Index": len(self.chain) + 1,
                    "Timestamp": datetime.datetime.now(),
                    "Merkle root": mtree.getRootHash(),
                    "previous_hash": self.hash(self.chain[-1]['Header']),
                },
                "Transaction": self.transactions[-3:]  # 3 transactions
            }
        self.chain.append(block)
        return block

    # Create transaction
    def create_transaction(self):
        try:
            seller = int(input("\nEnter the Seller ID: "))
            buyer = int(input("Enter the Receiver ID: "))
            pid = int(input("Enter the Property ID: "))
            Units = int(input(f"Enter number of products of {pid} you want to send : "))
            
            if (not self.validate_transaction(seller, buyer, pid,Units)):
                print("\nThis Transaction is not valid \n")
                return
            message = str(buyer) + str(pid*Units*100) +str(seller*10)
            message = message[:50]
            message = message.encode('utf8')
            
            send_time = time.strftime("%H:%M:%S", time.localtime())

            trans = {
                "Transaction_ID": str(uuid4()).replace('-', ''),
                "Time_send":send_time,
                "Time_received": None,
                "Seller Name":self.users[seller]['Name'],
                "Buyer Name":self.users[buyer]['Name'],
                "Seller ID": seller,
                "Buyer ID": buyer,
                "Product ID": pid,
                "Units": Units,
                "Sender_Signature":rsa.sign(message, self.users[seller]['Private_Key'], 'SHA-1'),
                "Receiver_Signature":None,
            }
            client_verdict = str(input(f"Type 'YES' if the Buyer - {self.users[buyer]['Name']} wants {Units} units of product with Product ID - {pid} else 'NO': "))
            if client_verdict == 'NO':
                print(f"\n The product has been rejected by you as per your request {self.users[buyer]['Name']}")
                # self.users[buyer]['Stake'] //= 3
                return

            receive_time = time.strftime("%H:%M:%S", time.localtime())
            trans['Time_received'] = receive_time
            message = "I recieved " + str(pid) + " product with " +str(Units) +  " units from " + str(buyer) + " at " + str(receive_time)
            message = message[:50]
            message = message.encode('utf8')
            trans['Receiver_Signature'] = rsa.sign(message, self.users[buyer]['Private_Key'], 'SHA-1')
            
            self.transactions.append(trans)
            self.product_history[pid]["Owner"].append(buyer)
            self.product_history[pid]["History"].append(trans)
            self.users[seller]['Products owned'][pid] -= Units
            if self.users[seller]['Products owned'][pid]==0:
                self.users[seller]['Products owned'].pop(pid)
                self.users[seller]['Number of Products'] = self.users[seller]['Number of Products'] - 1
                
            if pid in self.users[buyer]['Products owned']:
                self.users[buyer]['Products owned'][pid]  += Units
            else :
                self.users[buyer]['Products owned'][pid]=Units
                self.users[buyer]['Number of Products'] = self.users[buyer]['Number of Products'] + 1
                
            print("\nThis Transaction is added and validated\n")

            if (len(self.transactions) % 3 == 0):
                self.create_timer()
                print("\nCreating a new block\n")
        except:
            print("Enter the correct format of data required to add a new transaction!\n")

    def create_transaction_as_a_manufacture(self):
        try:
            buyer = int(input("Enter the Receiver ID: "))
            pid = int(input("Enter the Property ID: "))
            Units = int(input(f"Enter number of products of {pid} you want to send : "))
                
            send_time = time.strftime("%H:%M:%S", time.localtime())
            message = str(buyer) + str(pid*Units*100)
            message = message[:50]
            message = message.encode('utf8')
            # print(message) 
            trans = {
                "Transaction_ID": str(uuid4()).replace('-', ''),
                "Time_send":send_time,
                "Time_received": None,
                "Seller ID": 0,
                "Seller Name":"Manufacturer",
                "Buyer Name":self.users[buyer]['Name'],
                "Buyer ID": buyer,
                "Product ID": pid,
                "Units": Units,
                # "Sender_Signature":rsa.sign(message, 0, 'SHA-1'),
                "Receiver_Signature":None,
            }
            client_verdict = str(input(f"Type 'YES' if the Buyer - {self.users[buyer]['Name']} wants {Units} units of product with Product ID - {pid} else 'NO': "))
            if client_verdict == 'NO':
                print(f"\n The product has been rejected by you as per your request {self.users[buyer]['Name']}")
                # self.users[buyer]['Stake'] //= 3
                return
            receive_time = time.strftime("%H:%M:%S", time.localtime())
            trans['Time_received'] = receive_time
            message = "I recieved " + str(pid) + " product with " +str(Units) +  " units from " + str(buyer) + " at " + str(receive_time)
            message = message[:50]
            message = message.encode('utf8')
            trans['Receiver_Signature'] = rsa.sign(message, self.users[buyer]['Private_Key'], 'SHA-1')
            
            prodcut = {}
            prodcut[pid]=Units
            self.product_history[pid] = {
                'Owner': [buyer],
                'History': []
            }
            self.transactions.append(trans)
            self.product_history[pid]["Owner"].append(buyer)
            self.product_history[pid]["History"].append(trans)

            if pid in self.users[buyer]['Products owned']:
                self.users[buyer]['Products owned'][pid]  += Units
            else :
                self.users[buyer]['Products owned'][pid]=Units
                self.users[buyer]['Number of Products'] = self.users[buyer]['Number of Products'] + 1

            print("\nThis Transaction is added and validated\n")
            if (len(self.transactions) % 3 == 0):
                self.create_timer()
                print("\nCreating a new block\n")
        except:
            print("Enter the correct format of data required to add a new transaction!\n")


    # Validate Transaction
    def validate_transaction(self, seller, buyer, pid, pnum):
        if (seller == buyer):
            print("You cannot sell the product to yourself")
            return False
        if (self.users[seller]['Type']==2):
            print("You cannot sell the product as you are a client")
            return False
        if pid in self.product_history.keys():
            if seller in self.users.keys() and buyer in self.users.keys():
                for id in self.product_history[pid]['Owner']:
                    if id == seller:
                        if self.users[seller]['Products owned'][pid]>=pnum:
                            return True
                        else :
                            print("\nThe seller does not have enough units of product! Hence the seller is lying")
                            self.users[seller]['Stake'] //= 3
                            return False

                print("\nThe seller does not have this product!")
        return False

    # Validate Chain
    def validate_chain(self):
        if (len(self.chain) == 0):
            return False
        previous_block = self.chain[0]
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            print("\nHash of Header of Block " + str(i-1) + " : " +
                  str(self.hash(previous_block['Header'])))
            print("Hash of Previous Block's Header stored in Block " + str(i) + " : ",
                  current_block['Header']['previous_hash'])
            if (current_block['Header']['previous_hash'] != self.hash(previous_block['Header'])):
                return False
            previous_block = current_block
        return True

    # Print Blockchain
    def print_blockchain(self):
        print()
        if (len(self.chain) == 0):
            print("Blockchain is empty, please add more transactions :)\n")
            return
        for i in range(len(self.chain)):
            print("Block", i, ":")
            print("Header: ", self.chain[i]['Header'])
            print("Transactions: ")
            for j in range(len(self.chain[i]['Transaction'])):
                print(self.chain[i]['Transaction'][j])
            print()
        print()


    # Print Product History
    def print_product_history(self, pid):
        try:
            print()
            print("The transaction history of this Product is: ")
            for i in self.transactions:
                if i['Product ID'] == pid:
                    print(f"{i['Seller Name']} sent {i['Units']} units of {i['Product ID']} at: {i['Time_send']} to {i['Buyer Name']}")
                    print(f"{i['Buyer Name']} received at: {i['Time_received']}")
            
        except:
            print("\nPlease enter the correct inputs!\n")
            
            
    def generate_QR_Code(self, pid):
        try:
            print()
            prod_history = ""
            for i in self.transactions:
                if i['Product ID'] == pid:
                    prod_history += f"{i['Seller Name']} sent {i['Units']} units of {i['Product ID']} at: {i['Time_send']} to {i['Buyer Name']}\n"
                    prod_history += f"{i['Buyer Name']} received {i['Units']} units of {i['Product ID']} at: {i['Time_received']} from {i['Seller Name']}\n"
            url = pyqrcode.create(prod_history)
            url.svg("myqr.svg", scale = 8)
            url.png('myqr.png', scale = 6)
            print("\n Please scan the QR code for product history!\n")
            image_path = "myqr.png"
            image = mpimg.imread(image_path)
            plt.grid(False)
            plt.axis('off')
            plt.imshow(image)
            plt.show()
            
        except:
            print("\nPlease enter the correct inputs!\n")
    # Hash Function

    def hash(self, block):
        strg = json.dumps(block, sort_keys=True, default=str).encode()
        return hashlib.sha256(strg).hexdigest()

    # Create Timer for Achieving Consensus
    def create_timer(self):
        print("\n-------------------Acheiving consensus-------------------\n")
        with alive_bar(100) as bar:   # default setting
            for i in range(100):
                time.sleep(0.03)
                bar()  
        total_stake = 0
        total_user = 0
        for i in self.users:
            total_user += 1
            total_stake += 2*self.users[i]['Stake']
     
        total_stake//=total_user
        print()
        print()
        max_value = 0
        max_Node = None
        for i in self.users:
            random_num = random.randint(1,total_stake)
            if max_value < random_num + self.users[i]['Stake']:
                max_Node = i
                max_value = random_num + self.users[i]['Stake']
        print(str(
            self.users[max_Node]['Name']) + " is the miner for this round of consensus and will mine the block.\n")
        self.users[max_Node]['Stake'] += total_stake//total_user
        self.create_new_block()

    # Print Users
    def print_nodes(self):
        print()
        for i in self.users.keys():
            print("User ID: ", i)
            print("Name: ", self.users[i]['Name'])
            print("Number of product owned: ",self.users[i]['Number of Products'])
            print("Product IDs: ", self.users[i]['Products owned'])
            print("User's stake is: ", self.users[i]['Stake'])
            if self.users[i]['Type'] == 1:
                print(f"{self.users[i]['Name']} is a Distributor" )
            elif i == 0:
                print(f"User is the manufacturer")
            else:
                print(f"{self.users[i]['Name']} is a Client" )
        print()


if __name__ == '__main__':
    mine = Blockchain()
    while True:
        print("1. Create a new user")
        print("2. Create a new transaction as a manufacture")
        print("3. Create a new transaction")
        print("4. Print the blockchain")
        print("5. Print the product history")
        print("6. Generate QR for Product Status")
        print("7. Print the users")
        print("8. Validate Blockchain")
        print("9. Exit")
        choice = int(input("Enter your choice: "))
        if (choice == 1):
            mine.create_user()
        elif (choice == 2):
            mine.create_transaction_as_a_manufacture()
        elif (choice == 3):
            mine.create_transaction()
        elif (choice == 4):
            mine.print_blockchain()
        elif (choice == 5):
            pid = int(input("Enter the product ID: "))
            mine.print_product_history(pid)
        elif (choice == 6):
            pid = int(input("Enter the product ID: "))
            mine.generate_QR_Code(pid)
        elif (choice == 7):
            mine.print_nodes()
        elif (choice == 8):
            if (mine.validate_chain()):
                print("\nThe Blockchain is valid!\n")
            else:
                print("\nThe Blockchain is not valid!\n")
        elif (choice == 9):
            print("Hope you had a blast using LAND MINE!!")
            break
        else:
            print("Invalid choice")
