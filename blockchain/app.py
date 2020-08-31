from flask import Flask, render_template, request, redirect, url_for
from blockchain import Blockchain
import json
import uuid


# Creating the app node
app = Flask(__name__)

node_identifier = str(uuid.uuid4()).replace('-', '"')

# Initializing blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    """Mine for a new block"""

    # Get last block and last proof
    last_block = blockchain.last_block
    last_proof = blockchain.last_block['proof']

    # Get new proof based on last proof (This is the same as doing insane computations)
    proof = blockchain.proof_of_work(last_proof)

    # Reward the miner for his contributions
    blockchain.new_transaction(sender='0', recipient=node_identifier, amount=1)

    # Get the hash of the 'previous'/last block
    previous_hash = blockchain.hash(last_block)

    # Add this new block to the blockchain
    block = blockchain.new_block(proof, previous_hash)

    # Build API response
    response = {
        'message': "A new block has been forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return json.dumps(response), 200

@app.route('/transactions/new', methods = ['POST'])
def new_transaction():
    """Create new transaction"""

    # Accept values as a json
    values = request.get_json()

    print(f"values: {values}")

    # Define required params in the input json
    required_params = ['sender', 'reciepient', 'amount']

    # Return an error if not all required params are present
    if not all(k in values for k in required_params):
        return 'Missing values', 400

    # Add new transaction to the blockchain queue
    index = blockchain.new_transaction(values['sender'], values['reciepient'], values['amount'])
    response = {'message': f'Transaction is scheduled to be added to block #: {index}'}

    return json.dumps(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    """Return the full blockchain at the given moment"""
    
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return json.dumps(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)