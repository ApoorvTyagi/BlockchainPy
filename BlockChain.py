import logging
import time
import json
from hashlib import sha256

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block = json.dumps(self.__dict__, sort_keys=True).encode()
        return sha256(block).hexdigest()


class Blockchain:
    difficulty = 2  # difficulty of our PoW algorithm

    def __init__(self):
        self.new_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "This is the first block of the chain.", time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def last_block(self):
        return self.chain[-1]

    def add_new_transaction(self, transaction):
        self.new_transactions.append(transaction)

    def chain_valid(self, chain):
        logger.info('Checking if the chain is valid...')
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            # Checking Previous Hash is Valid or not
            block = chain[block_index]
            if block.previous_hash != previous_block.hash:
                return False

            # Checking Validity of Proof of work
            proof = block.hash
            if not self.is_valid_proof(block, proof):
                return False

            previous_block = block
            block_index += 1

        return True

    # This is the function for proof of work
    # and used to successfully mine the block
    @staticmethod
    def find_proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block().hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    @staticmethod
    def is_valid_proof(block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return block_hash.startswith('0' * Blockchain.difficulty)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.new_transactions:
            return False

        for transaction in self.new_transactions:
            last_block = self.last_block()
            new_block = Block(last_block.index + 1, transaction, time.time(), last_block.hash)
            proof = self.find_proof_of_work(new_block)
            self.add_block(new_block, proof)

        self.new_transactions = []
        return True
