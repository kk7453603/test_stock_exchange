import time
import random
import unittest


class Order:
    def __init__(self, orderid, timestamp, ordertype, quantity, price):
        self.orderid = orderid
        self.timestamp = timestamp
        self.ordertype = ordertype
        self.quantity = quantity
        self.price = price


class OrderBook:
    def __init__(self):
        self.buy_orders = []  # список заказов на покупку
        self.sell_orders = []  # список заказов на продажу

    def add_order(self, order):
        if order.ordertype == "buy":
            self.buy_orders.append(order)
        elif order.ordertype == "sell":
            self.sell_orders.append(order)

    def update_order(self, orderid, ordertype, quantity, price=None):
        if ordertype == "buy":
            for order in self.buy_orders:
                if order.orderid == orderid:
                    order.quantity = quantity
                    if price:
                        order.price = price
                        break
        elif ordertype == "sell":
            for order in self.sell_orders:
                if order.orderid == orderid:
                    order.quantity = quantity
                    if price:
                        order.price = price
                        break

    def remove_order(self, orderid, ordertype):
        if ordertype == "buy":
            for order in self.buy_orders:
                if order.orderid == orderid:
                    self.buy_orders.remove(order)
                    break

        elif ordertype == "sell":
            for order in self.sell_orders:
                if order.orderid == orderid:
                    self.sell_orders.remove(order)
                    break

    def match_orders(self):
        buy_orders_sorted = sorted(self.buy_orders, key=lambda x: x.price, reverse=True)
        sell_orders_sorted = sorted(self.sell_orders, key=lambda x: x.price)
        matches = []

        for buy_order in buy_orders_sorted:
            match_found = False
            for sell_order in sell_orders_sorted:
                if buy_order.price >= sell_order.price and buy_order.quantity > 0 and sell_order.quantity > 0:
                    quantity = min(buy_order.quantity, sell_order.quantity)
                    match = (buy_order.orderid, sell_order.orderid, quantity, sell_order.price)
                    matches.append(match)
                    buy_order.quantity -= quantity
                    sell_order.quantity -= quantity
                    match_found = True
                    break

            if not match_found:
                self.buy_orders.append(buy_order)

        return matches


class TestOrderBook(unittest.TestCase):
    def test_add_order(self):
        orderbook = OrderBook()
        order = Order(1, 1600000000, "buy", 1, 100)
        orderbook.add_order(order)
        self.assertEqual(len(orderbook.buy_orders), 1)

    def test_update_order(self):
        orderbook = OrderBook()
        order = Order(1, 1600000000, "buy", 1, 100)
        orderbook.add_order(order)
        orderbook.update_order(1, "buy", 10)
        self.assertEqual(order.quantity, 10)

    def test_remove_order(self):
        order_book = OrderBook()
        order1 = Order(1, 1600000000, "buy", 1, 100)
        order2 = Order(2, 1600000000, "sell", 1, 100)
        order_book.add_order(order1)
        order_book.add_order(order2)
        order_book.remove_order(1, "buy")
        self.assertEqual(len(order_book.buy_orders), 0)

    def test_match_orders(self):
        order_book = OrderBook()
        order1 = Order(1, 1600000000, "buy", 2, 100)
        order2 = Order(2, 1600000000, "sell", 1, 100)
        order3 = Order(3, 1600000000, "sell", 3, 120)
        order_book.add_order(order1)
        order_book.add_order(order2)
        order_book.add_order(order3)
        matches = order_book.match_orders()
        self.assertEqual(matches, [(1, 2, 1, 100)])


def simulate_market(orderbook):
    while True:
        orderid = random.randint(1, 100)
        timestamp = int(time.time())
        ordertype = random.choice(["buy", "sell"])
        quantity = random.randint(1, 10)
        price = random.randint(1, 100)
        order = Order(orderid, timestamp, ordertype, quantity, price)

        orderbook.add_order(order)

        matches = orderbook.match_orders()
        for match in matches:
            print(f"Match: {match[0]} (Buy) <-> {match[1]} (Sell), Quantity: {match[2]}, Price: {match[3]}")

        time.sleep(1)


if __name__ == '__main__':
    unittest.main(exit=False)
    order_book = OrderBook()
    simulate_market(order_book)
