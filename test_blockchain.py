import unittest
from BlockChain import Blockchain


class BlockchainTestCase(unittest.TestCase):

    def test_blockchain(self):
        blockchain = Blockchain()
        blockchain.add_new_transaction("Test Data")
        self.assertEqual(blockchain.mine(), True)
        self.assertEqual(blockchain.chain_valid(blockchain.chain), True)
        self.assertEqual(len(blockchain.chain), 2)


if __name__ == '__main__':
    unittest.main()
