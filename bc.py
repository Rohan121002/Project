import hashlib
import time
import random

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

class Block:
    def __init__(self, prev_hash, transactions, timestamp=None, validator=None):
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.validator = validator
        self.nonce = 0
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

class Validator:
    def __init__(self, public_key, stake):
        self.public_key = public_key
        self.stake = stake

class LieDetectionContract:
    def __init__(self):
        self.verifications = {}

    def request_verification(self, requester, target, action):
        self.verifications[(requester, target, action)] = None

    def verify(self, requester, target, action, verification_result):
        if (requester, target, action) in self.verifications:
            self.verifications[(requester, target, action)] = verification_result

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

    # Register validators with stakes
    validator1 = Validator("Validator1", 1000)
    validator2 = Validator("Validator2", 1500)
    validator3 = Validator("Validator3", 2000)
    blockchain.add_validator(validator1)
    blockchain.add_validator(validator2)
    blockchain.add_validator(validator3)

    # Perform transactions
    blockchain.create_transaction("Validator1", "Validator2", 200)
    blockchain.create_transaction("Validator2", "Validator3", 300)

    # Request verification
    blockchain.create_verification_request("Validator1", "Validator2", "Dispatch")
    blockchain.create_verification_request("Validator2", "Validator3", "Dispatch")

    # Simulate verification
    verification_result = True  # Set to True for successful verification
    blockchain.verify_action("Validator1", "Validator2", "Dispatch", verification_result)
    blockchain.verify_action("Validator2", "Validator3", "Dispatch", verification_result)

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