import hashlib
import time
import random
import rsa

class Transaction:
    def __init__(self, sender_id, receiver_id, amount, sender_signature):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        # self.transaction_id = transaction_id
        self.sender_signature = sender_signature
    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "product_id": self.product_id,
            "status": self.status,
        }
    def test(self):
        print("heyy")

class Block:
    def __init__(self,prev_hash, merkle_root,transactions, timestamp=None, validator=None):
        self.block_hash = self.calculate_hash()
        self.prev_hash = prev_hash
        self.merkle_root = merkle_root
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = (str(self.timestamp) +
                str(self.transactions) +
                self.prev_hash +
                (self.validator.public_key if self.validator else ""))
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.hash = self.calculate_hash()
    
    def merkle_root(self):
        root = str(self.transactions)
        return hashlib.sha256(root.encode()).hexdigest()

# class Product:
#     def __init__(self):

class Node:
    def __init__(self,node_id, stake,deposit = 100):
        (self.pubkey, self.__privkey) = rsa.newkeys(512)
        self.node_id = node_id
        self.stake = stake  - deposit
        self.deposit = deposit
    def signature_by_sender(self,receiver_id,amount):
         message = (str(self.node_id+receiver_id) + str(amount))
         signature = rsa.sign(message.encode(), self.__privkey, 'SHA-1')
         return signature

class Product:
    def __init__(self, Product_id, amount):
        self.Product_id = Product_id
        self.amount = amount


class Blockchain:
    def __init__(self, difficulty=2, reward=10):
        self.chain = [self.create_genesis_block()]
        self.Transactions_list = []
        self.Product_list = {}
        self.difficulty = difficulty
        self.pending_transactions = []
        self.validators_list = []
        self.mining_reward = reward
        self.lie_detection_contract = LieDetectionContract()
    
    def create_user(self):
        Node_id= int(input("Enter Node id : "))
        stake = int(input("Enter Initial deposit : "))
        while stake <= 100:
            stake = int(input("The entered amount is less than required deposit. Please re-enter the amount"))
        blockchain.validators_list.append(Node(Node_id,stake))

    def create_transaction(self):
        sender_id= int(input("Enter your id : "))
        receiver_id= input("Enter receiver id : ")
        amount = input("Enter amount : ")
        Product_id = input("Enter Product_id : ")
        if (not self.validate_transaction(sender_id, receiver_id, Product_id,amount)):
            print("Transaction is not valid")
            return
        print("The transaction is valid and added") 
        self.Transactions_list.append(Transaction(sender_id,receiver_id,amount,Product_id))   
        signature = nodes[sender_id].signature_by_sender(receiver_id,amount,)
        blockchain.create_transaction(sender_id, receiver_id, amount, Product_id)
        blockchain.create_verification_request(sender_id, receiver_id, "Dispatch")
        verification_result = True  # Set to True for successful verification
        blockchain.verify_action(sender_id,receiver_id ,"Dispatch", verification_result)
        selected_validator = blockchain.select_validator()


    def create_verification_request(self, requester, target, action):
        self.lie_detection_contract.request_verification(requester, target, action)

    def verify_action(self, requester, target, action, verification_result):
        self.lie_detection_contract.verify(requester, target, action, verification_result)

    def create_genesis_block(self):
        return Block(calculate_hash(self),"0", [], timestamp=0)

    def get_last_block(self):
        return self.chain[-1]

    def add_validator(self, validator):
        self.validators.append(validator)

    def get_total_stake(self):
        return sum(validator.stake for validator in self.validators)

    def select_validator(self):
        random.seed()
        total_stake = self.get_total_stake()
        max_stake_node = None
        max_stake_stake = 0
        for validator in self.validators:
            rand_value = random.uniform(0, total_stake)
            if validator.stake + rand_value > max_stake_stake:
                max_stake_node = validator
                max_stake_stake = validator.stake + rand_value
        return max_stake_node

    def mine_pending_transactions(self, miner):
        if not self.pending_transactions:
            return False
        prev_block = self.get_last_block()
        new_block = Block(prev_block.block_hash, self.pending_transactions, validator=miner, difficulty=self.difficulty)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = [Transaction(None, miner.public_key, self.mining_reward)]
        return True

    # def create_transaction(self, sender, receiver, amount,signature):
    #     if sender == receiver:
    #         return False

    #     sender_balance = self.get_balance(sender)
    #     if sender_balance < amount:
    #         return False

    #     transaction = Transaction(sender, receiver, amount,signature)
    #     self.pending_transactions.append(transaction)
    #     return True

    # def get_balance(self, address):
    #     balance = 0
    #     for block in self.chain:
    #         for transaction in block.transactions:
    #             if transaction.sender == address:
    #                 balance -= transaction.amount
    #             if transaction.receiver == address:
    #                 balance += transaction.amount
    #     return balance

class LieDetectionContract:
    def __init__(self):
        self.verifications = {}

    def request_verification(self, requester, target, action):
        self.verifications[(requester, target, action)] = None

    def verify(self, requester, target, action, verification_result):
        if (requester, target, action) in self.verifications:
            self.verifications[(requester, target, action)] = verification_result

# Starting Point
if __name__ == '__main__':
    # nodes:dict[int,Node]={}
    # nodes:list[Node]=[]
    # Transactions:list[Transaction]=[]
    blockchain = Blockchain()
    while True:
        print("1. Create a new user")
        print("2. Create a new transaction")
        print("3. Print the blockchain")
        print("4. Print the product status")
        print("5. Print the users")
        print("6. Validate Block")
        print("7. Exit")
        task_no = input()
        if task_no==1:
            blockchain.create_user()
        
        elif task_no == 2:
            blockchain.create_transaction()

        elif task_no == 3:
            client_id = input("Enter your ID")
            flag = False
            for transaction in blockchain.pending_transactions:
                if transaction == client_id:
                    # signature taken of client
                    blockchain.pending_transactions.remove(transaction)
                    flag = True
                    break
            if not flag:
                print(f"No transaction pending for this {client_id}")
            else:
                print("Product received by Client")
        elif task_no == 4:


            
if _name_ == '_main_':
    mine = Land_Blockchain()
    while True:
        print("1. Create a new user")
        print("2. Create a new transaction")
        print("3. Print the blockchain")
        print("4. Print the property history")
        print("5. Print the users")
        print("6. Validate Blockchain")
        print("7. Exit")
        choice = int(input("Enter your choice: "))
        if (choice == 1):
#             mine.create_user()
#         elif (choice == 2):
#             mine.create_transaction()
#         elif (choice == 3):
#             mine.print_blockchain()
#         elif (choice == 4):
#             pid = int(input("Enter the property ID: "))
#             mine.print_property_history(pid)
#         elif (choice == 5):
#             mine.print_nodes()
#         elif (choice == 6):
#             if (mine.validate_chain()):
#                 print("\nThe Blockchain is valid!\n")
#             else:
#                 print("\nThe Blockchain is not valid!\n")
#         elif (choice == 7):
#             print("Hope you had a blast using LAND MINE!!")
#             break
#         else:
#             print("Invalid choice")
                




    
    # blockchain.create_transaction("Node2", "Node3", 300)

    # Request verification
    # blockchain.create_verification_request("Node1", "Node2", "Dispatch")
    # blockchain.create_verification_request("Node2", "Node3", "Dispatch")

    # Simulate verification
    # verification_result = True  # Set to True for successful verification
    # blockchain.verify_action("Node1", "Node2", "Dispatch", verification_result)
    # blockchain.verify_action("Node2", "Node3", "Dispatch", verification_result)

    # Mine a block
    selected_validator = blockchain.select_validator()
    if selected_validator:
        print(f"Selected validator: {selected_validator.public_key}")
        if blockchain.mine_pending_transactions(selected_validator):
            print("Block mined successfully!")
        else:
            print("No pending transactions to mine.")
    else:
        print("No validator selected.")
    print(validator1.stake)
    # Print the blockchain
    for block in blockchain.chain:
        print(f"Block Hash: {block.hash}")




