import hashlib
import time
import random
import rsa

class Transaction:
    def __init__(self, sender_id, receiver_id, amount,transaction_id, reciever_signature,sender_signature):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.transaction_id = transaction_id
        self.reciever_signature = reciever_signature
        self.sender_signature = sender_signature
        
        
        

class Block:
    def __init__(self, block_hash, prev_hash, merkle_root,transactions, timestamp=None, validator=None):
        self.block_hash = block_hash
        self.prev_hash = prev_hash
        self.merkle_root = merkle_root
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = (str(self.timestamp) +
                str(self.transactions) +
                str(self.nonce) +
                self.prev_hash +
                (self.validator.public_key if self.validator else ""))
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Node:
    def __init__(self,node_id, stake,deposit = 100):
        (self.pubkey, self.__privkey) = rsa.newkeys(512)
        self.node_id = node_id
        self.stake = stake  - deposit
        self.deposit = deposit

class LieDetectionContract:
    def __init__(self):
        self.verifications = {}

    def request_verification(self, requester, target, action):
        self.verifications[(requester, target, action)] = None

    def verify(self, requester, target, action, verification_result):
        if (requester, target, action) in self.verifications:
            self.verifications[(requester, target, action)] = verification_result
def generate_random_number_and_sha256():
    # Generate a random number
        random_number = random.randint(1, 1000000000000000000)
        random_number_str = str(random_number)
        # Calculate the SHA-256 hash of the random number string
        sha256_hash = hashlib.sha256(random_number_str.encode()).hexdigest()
        return random_number, sha256_hash
    
class Blockchain:
    def __init__(self, difficulty=2, reward=10):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.validators = []
        self.mining_reward = reward
        self.lie_detection_contract = LieDetectionContract()
        
    def create_verification_request(self, requester, target, action):
        self.lie_detection_contract.request_verification(requester, target, action)

    def verify_action(self, requester, target, action, verification_result):
        self.lie_detection_contract.verify(requester, target, action, verification_result)

    def create_genesis_block(self):
        return Block("0", [], timestamp=0)

    def get_last_block(self):
        return self.chain[-1]

    def add_validator(self, validator):
        self.validators.append(validator)

    def get_total_stake(self):
        return sum(validator.stake for validator in self.validators)

    def select_validator(self):
        random.seed()
        rand_value = random.uniform(0, self.get_total_stake())
        cumulative_stake = 0
        for validator in self.validators:
            cumulative_stake += validator.stake
            if cumulative_stake >= rand_value:
                return validator
        return None

    def mine_pending_transactions(self, miner):
        if not self.pending_transactions:
            return False

        prev_block = self.get_last_block()
        new_block = Block(prev_block.hash, self.pending_transactions, validator=miner, difficulty=self.difficulty)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = [Transaction(None, miner.public_key, self.mining_reward)]
        return True

    def create_transaction(self, sender, receiver, amount):
        if sender == receiver:
            return False

        sender_balance = self.get_balance(sender)
        if sender_balance < amount:
            return False

        transaction = Transaction(sender, receiver, amount)
        self.pending_transactions.append(transaction)
        return True

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        return balance

if __name__ == '__main__':
    blockchain = Blockchain()
    task_no="sparsh"
    while task_no != 'exit':
        print("Enter 1 if you want to create a node: ")
        print("Enter 2 if you want to do a transaction: ")
        print("Enter 2 if you want to exit: ")
        task_no = input()
        if task_no==1:
            Node_id= input("Enter Node id : ")
            stake = input("Enter Initial deposit : ")
            Node(Node_id,stake)
        elif task_no == 2:
            sender_id= input("Enter your id : ")
            receiver_id= input("Enter receiver id : ")
            amount = input("Enter amount : ")
            Product_id = input("Enter Product_id : ")
            Transaction(sender_id,receiver_id,amount,Product_id)    


    # Register validators with stakes
    validator1 = Node("Node1", 1000)
    validator2 = Node("Node2", 1500)
    validator3 = Node("Node3", 2000)
    blockchain.add_validator(validator1)
    blockchain.add_validator(validator2)
    blockchain.add_validator(validator3)

    # Perform transactions
    blockchain.create_transaction("Node1", "Node2", 200)
    blockchain.create_transaction("Node2", "Node3", 300)

    # Request verification
    blockchain.create_verification_request("Node1", "Node2", "Dispatch")
    blockchain.create_verification_request("Node2", "Node3", "Dispatch")

    # Simulate verification
    verification_result = True  # Set to True for successful verification
    blockchain.verify_action("Node1", "Node2", "Dispatch", verification_result)
    blockchain.verify_action("Node2", "Node3", "Dispatch", verification_result)

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