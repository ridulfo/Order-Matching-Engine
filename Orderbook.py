import enum
from Order import Order, Side
from sortedcontainers import SortedList
from typing import List

def get_timestamp():
	""" Microsecond timestamp """
	return int(1e6 * time.time())


class Trade(object):
	def __init__(self, incoming_side: Side, price: float, trade_size: int, incoming_order_id: str, book_order_id: str):
		self.side = incoming_side
		self.price = price
		self.size = trade_size
		self.incoming_order_id = incoming_order_id
		self.book_order_id = book_order_id

	def __repr__(self):
		return 'Executed: {0} {1} units at {2}'.format(self.side, self.size, self.price)


class Orderbook(object):
	def __init__(self):
		self.bids: SortedList[Order] = SortedList()
		self.asks: SortedList[Order] = SortedList()
		self.trades = []

	def processOrder(self, incomingOrder: Order):
		"""
		Takes an order and tries to fill it with the orders on the market
		1. For ev
		"""
		def whileClause():
			if incomingOrder.side==Side.BUY:
				return len(self.asks) > 0 and incomingOrder.price >= self.asks[0].price
			else:
				return len(self.bids) > 0 and incomingOrder.price <= self.bids[0].price

		# while there are orders
		while whileClause():
			bookOrder = None
			if incomingOrder.side==Side.BUY:
				bookOrder = self.asks.pop(0)
			else:
				bookOrder = self.bids.pop(0)

			if incomingOrder.RemainingToFill == bookOrder.RemainingToFill:  # if the same volume
				volume = incomingOrder.RemainingToFill
				incomingOrder.RemainingToFill -= volume
				bookOrder.RemainingToFill -= volume
				self.trades.append(Trade(
					incomingOrder.side, bookOrder.price, volume, incomingOrder.order_id, bookOrder.order_id))
				break

			elif incomingOrder.RemainingToFill > bookOrder.RemainingToFill:  # incoming has greater volume
				volume = bookOrder.RemainingToFill
				incomingOrder.RemainingToFill -= volume
				bookOrder.RemainingToFill -= volume
				self.trades.append(Trade(
					incomingOrder.side, bookOrder.price, volume, incomingOrder.order_id, bookOrder.order_id))

			elif incomingOrder.RemainingToFill < bookOrder.RemainingToFill:  # book has greater volume
				volume = incomingOrder.RemainingToFill
				incomingOrder.RemainingToFill -= volume
				bookOrder.RemainingToFill -= volume
				self.trades.append(Trade(
					incomingOrder.side, bookOrder.price, volume, incomingOrder.order_id, bookOrder.order_id))

				if bookOrder.side==Side.SELL:
					self.asks.add(bookOrder)
				else:
					self.bids.add(bookOrder)
				break

		if incomingOrder.RemainingToFill > 0:
			if incomingOrder.side == Side.BUY:
				self.bids.add(incomingOrder)
			else:
				self.asks.add(incomingOrder)

	def getBid(self): return self.bids[0].price if len(self.bids)>0 else None
	def getAsk(self): return self.asks[0].price if len(self.asks)>0 else None

	def __repr__(self):
		lines = []
		lines.append("-"*5 + "OrderBook" + "-"*5)

		lines.append("\nAsks:")
		asks = self.asks.copy()
		while len(asks) > 0:
			lines.append(str(asks.pop()))

		lines.append("\t"*3 + "Bids:")
		bids = list(reversed(self.bids.copy()))
		while len(bids) > 0:
			lines.append("\t"*3 + str(bids.pop()))

		lines.append("-"*20)
		return "\n".join(lines)


