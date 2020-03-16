from Order import Order, Side
from sortedcontainers import SortedList
from typing import List
from time import time
from Trade import Trade
from Order import OrderType

class Orderbook(object):
	"""
	An orderbook.
	-------------

	It can store and process orders.
	"""
	def __init__(self):
		self.bids: SortedList[Order] = SortedList()
		self.asks: SortedList[Order] = SortedList()
		self.trades = []

	def processOrder(self, incomingOrder: Order):
		"""
		Processes an order

		Depending on the type of order the following can happen:
		- Limit Order
		- Cancel Order
		"""

		if incomingOrder.orderType == OrderType.CANCEL:
			if incomingOrder.side == Side.BUY:
				for order in self.bids:
					if incomingOrder.order_id == order.order_id:
						self.bids.discard(order)
						break
			else:
				for order in self.asks:
					if incomingOrder.order_id == order.order_id:
						self.asks.discard(order)
						break
			return


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