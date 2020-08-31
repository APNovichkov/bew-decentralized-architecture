import json
import hashlib
from time import time


class Blockchain():
    """A very simple Blockchain Class"""

    def __init__(self):
        """Define the object parameters"""

        # Chain of blocks
        self.chain = []

        # Current transactions awaiting addition to a block
        self.current_transactions = []

        # An initial block to start the chain off
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """This function creates new blocks and then adds to the existing chain"""

        # Define the block
        block = {
            "index": len(self.chain) + 1,  # Index of the block (always starts at 1 in a Blockchain)
            "timestamp": time(),  # Time of block creation
            "proof": proof,  # Proof-of-work done to generate this block
            "transactions": self.current_transactions,  # All of the current transactions in the queueu
            "previous_hash": previous_hash or self.hash(self.last_block)  # A hash of the previous block, this keeps the integrity of the chain
        }

        # Reset current transaction queue to empty
        self.current_transactions = []

        # Append block to chain
        self.chain.append(block)

        # Return the block
        return block

    def new_transaction(self, sender, recipient, amount):
        """This function adds a new transaction to already existing transactions"""

        # Define a transaction
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }

        # Append new transaction to transaction queue
        self.current_transactions.append(transaction)

        # Return index of block that this transaction will be added to
        return self.last_block['index'] + 1


    def proof_of_work(self, last_proof):
        """A proof of work sample function"""
        proof = 0

        # Run in an infinite loop until valid proof is True
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        # Return this proof of work
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """A sample checker to see if proof of work is valid"""

        # Encode the guess
        guess = f"{last_proof}{proof}".encode()

        # Take hash of the guess
        guess_hash = hashlib.sha256(guess).hexdigest()

        # Return true (valid proof) if the last 4 characters of the hash are '0000'
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """Hash a block"""

        block_string = json.dumps(block, sort_keys=True).encode()
        hash = hashlib.sha256(block_string).hexdigest()

        return hash

    @property
    def last_block(self):
        """Calls and returns the last block of the chain"""

        return self.chain[-1]


if __name__ == '__main__':
    blockchain = Blockchain()
    t1 = blockchain.new_transaction("Satoshi", "Mike", '5 BTC')
    t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
    t3 = blockchain.new_transaction("Satoshi", "Hal", '5 BTC')
    blockchain.new_block(12345)

    t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
    t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
    t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
    blockchain.new_block(6789)

    print(f"Block Chain: ", blockchain.chain)

