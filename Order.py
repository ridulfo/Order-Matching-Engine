import enum


class Side(enum.Enum):
    BUY = 0
    SELL = 1


class Order(object):
    def __init__(self, side, price: float, size: int, timestamp: int = None, order_id=None):
        self.side = side  # Side.BUY or Side.Sell
        self.price = price # Price
        self.size = self.RemainingToFill = size # size = initial size, filled = how much is left to fill
        self.timestamp = timestamp # timestamp in microseconds
        self.order_id = order_id

    def __lt__(self, other):
        if self.price != other.price:
            return self.price > other.price

        # elif self.timestamp != other.timestamp:
        #     return self.timestamp < other.timestamp

        elif self.size != other.size:
            self.size < other.size
    
    def __repr__(self):
        return '{0}: {1} units at {2}'.format(
                "BUY" if self.side == Side.BUY else "Sell",
                self.RemainingToFill, self.price)
