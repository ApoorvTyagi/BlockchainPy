import BlockChain
from flask import Flask, jsonify
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

# Creating the Web App using flask
app = Flask(__name__)

# Create the object of the class blockchain
blockchain = BlockChain.Blockchain()


# Mining a new block
@app.route("/mine_block", methods=["GET"])
def mine_block():
    logger.info("Mining new block...")
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {
        "message": "A block is MINED",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }

    return jsonify(response), 200


# Display blockchain in json format
@app.route("/get_chain", methods=["GET"])
def display_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return jsonify(response), 200


# Check validity of blockchain
@app.route("/valid", methods=["GET"])
def valid():
    validity = blockchain.chain_valid(blockchain.chain)

    if validity:
        response = {"message": "The Blockchain is valid."}
    else:
        response = {"message": "The Blockchain is not valid."}
    return jsonify(response), 200


# Run the flask server on localhost
app.run(host="127.0.0.1", port=5000)
