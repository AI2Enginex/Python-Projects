from hashlib import sha256

# Function to concatenate arguments and compute SHA-256 hash
def updatehash(*args):
    text = ''
    for arg in args:
        text += str(arg)
    hashing_text = sha256(text.encode('ascii')).hexdigest()
    return hashing_text

# Class representing a block in the blockchain
class Block:
    data = None  # Data stored in the block
    previous_hash = '0' * 64  # Hash of the previous block
    nonce = 0  # Nonce used for proof of work

    # Constructor to initialize the block
    def __init__(self, data, number=0):
        self.data = data
        self.number = number

    # Function to compute the hash of the block
    def hash(self):
        return updatehash(
            self.previous_hash,
            self.number,
            self.data,
            self.nonce
        )

    # Function to return string representation of the block
    def __str__(self):
        return str("block no : %s\nHash : %s\nprevious hash : %s\nData : %s\nnonce : %s\n" % (
            self.number, self.hash(), self.previous_hash, self.data, self.nonce))


# Class representing a blockchain
class Blockchain:
    difficulty = 4  # Difficulty level for proof of work

    # Constructor to initialize the blockchain with optional initial chain
    def __init__(self, chain=[]):
        self.chain = chain

    # Function to add a block to the blockchain
    def add(self, block):
        self.chain.append(block)

    # Function to mine a block and add it to the blockchain
    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass
        # Proof of work: Find nonce such that hash starts with required number of zeros
        while True:
            if block.hash()[:4] == '0' * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

# Main function to create and mine blocks with given data
def main(data=None):
    blockchain = Blockchain()  # Create a new blockchain instance
    database = data  # Data to be stored in the blockchain
    num = 0  # Initialize block number
    # Mine blocks for each data entry
    for data in database:
        num = num + 1  # Increment block number
        blockchain.mine(Block(data, num))  # Mine block with given data and block number
    # Print each block in the blockchain
    for block in blockchain.chain:
        print(block)

# Entry point of the program
if __name__ == '__main__':
    main(data=["hello world", "what's up", "hello"])  # Call main function with sample data
