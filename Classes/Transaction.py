

class Transaction():
    def __init__(self, distributor, receiver, timestamp, amount):
        self.distributor = distributor
        self.receiver = receiver
        self.timestamp = timestamp
        self.amount = amount

    