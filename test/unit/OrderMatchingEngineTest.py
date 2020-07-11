from OrderMatchingEngine import *
import unittest

class OrderbookTest(unittest.TestCase):
    def initialState(self):
        book = Orderbook()

        #Book should be empty to begin with
        self.assertEqual(len(book), 0)
        self.assertEqual(book.getBid(), None)
        self.assertEqual(book.getAsk(), None)
        
    def testInsert(self):
        book = Orderbook()
        order = LimitOrder(0, Side.BUY, 10, 10)
        book.processOrder(order)
        self.assertEqual(len(book), 1)
        self.assertEqual(book.getBid(), 10)
        self.assertEqual(book.getAsk(), None)
    
    def testExecution(self):
        book = Orderbook()
        order = LimitOrder(0, Side.BUY, 10, 10)
        book.processOrder(order)
        order = LimitOrder(1, Side.SELL, 10, 10)
        book.processOrder(order)

        self.assertEqual(len(book), 0)
        self.assertEqual(book.getBid(), None)
        self.assertEqual(book.getAsk(), None)
    
    

# To run: python -m unittest test/unit/OrderMatchingEngineTest.py
if __name__ == "__main__":
    unittest.main()