import datetime
import hashlib
import json
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


class Blockchain:

    # This function is created
    # to create the very first
    # block and set it's hash to "0"
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        logger.info('Creating new block...')
        block = {
            "index": len(self.chain),
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        return block

    def print_previous_block(self):
        return self.chain[-1]

    # This is the function for proof of work
    # and used to successfully mine the block
    @staticmethod
    def proof_of_work(previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()
            if hash_operation[:4] == "00000":
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        logger.info('Checking if the chain is valid...')
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            # Checking Previous Hash is Valid or not
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False

            # Checking Validity of Proof of work
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()

            if hash_operation[:4] != "00000":
                return False

            previous_block = block
            block_index += 1

        return True
