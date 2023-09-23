import hashlib

class Block():
    def __init__(self, timestamp, merkle_root, prev_hash):
        self.hash = hashlib.sha256()
        self.timestamp = timestamp
        self.merkle_root = merkle_root
        self.prev_hash = prev_hash
        self.transaction_count = 0
        self.transaction = []


def 

    

        
