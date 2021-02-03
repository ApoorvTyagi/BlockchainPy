import BlockChain
from flask import Flask, jsonify, request
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

# Creating the Web App using flask
app = Flask(__name__)

# Create the object of the class blockchain
blockchain = BlockChain.Blockchain()


# Mining a new block
@app.route("/mine", methods=["GET"])
def mine_block():
    response = {
        "message": "Failed to mine"
    }

    if blockchain.mine():
        response = {
            "message": "Pending transactions has been added to blockchain after mining new blocks"
        }

    return jsonify(response), 200


# Display blockchain in json format
@app.route("/get_chain", methods=["GET"])
def display_chain():
    if blockchain.chain:
        response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
        return jsonify(response), 200

    return jsonify({"message": "No Chain Found"}, 200)


# Check validity of blockchain
@app.route("/valid", methods=["GET"])
def is_valid():
    validity = blockchain.chain_valid(blockchain.chain)

    if validity:
        response = {"message": "The Blockchain is valid."}
    else:
        response = {"message": "The Blockchain is not valid."}
    return jsonify(response), 200


@app.route("/add", methods=["GET"])
def add_new_transaction():
    transaction_data = request.args.get('data')
    response = {
        "message": "Cannot find transaction data"
    }

    if transaction_data:
        blockchain.new_transactions.append(transaction_data)
        response = {
            "message": "Added new transaction"
        }

    return jsonify(response), 200


# Run the flask server on localhost
app.run(host="127.0.0.1", port=5000)
