import logging
logging.basicConfig(level = logging.DEBUG)

def buy_order(size):
    """
    This function places the market bid-orders
    :param size: size of share
    :return: nothing
    """
    global order_id

    if len(ask_order) == 0:
        bid_order.append([order_id, float('inf'), size])
        bid_order.sort(key = bid_sort, reverse=True)

    # Iterate over ask_order to fulfill the bid_order
    index = 0
    while size > 0 and index < len(ask_order):
        ask_order_price = ask_order[index][1]
        ask_order_size = ask_order[index][2]
        temp = size
        size = size - ask_order_size
        ask_order[index][2] -= temp
        index += 1

    # If the bid_order isn't get fulfilled
    if size > 0:
        bid_order.append([order_id, float('inf'), size])
        bid_order.sort(key = bid_sort, reverse = True)

    # Check to price if any value from ask has become 0
    index = 0
    while index < len(ask_order):
        price = ask_order[index][2]
        if price <= 0:
            ask_order.pop(index)
        else:
            index += 1



def sell_order(size):
    """
    This function places the market sell-orders
    :param size: size of share
    :return: nothing
    """
    global order_id

    if len(bid_order) == 0:
        ask_order.append([order_id, float('-inf'), size])
        ask_order.sort(key=bid_sort)

    # Iterate over ask_order to fulfill the bid_order
    index = 0
    while size > 0 and index < len(bid_order):
        bid_order_price = bid_order[index][1]
        bid_order_size = bid_order[index][2]
        temp = size
        size = size - bid_order_size
        bid_order[index][2] -= temp
        index += 1

    # If the bid_order isn't get fulfilled
    if size > 0:
        ask_order.append([order_id, float('-inf'), size])
        ask_order.sort(key=bid_sort, reverse=True)

    # Check to price if any value from ask has become 0
    index = 0
    while index < len(bid_order):
        price = bid_order[index][2]
        if price <= 0:
            bid_order.pop(index)
        else:
            index += 1

def place_order():
    """
    This function takes the input for placing the market order
    :return: nothing
    """
    print("In Place Order")
    action = int(input("\n What order you want to place? \n 1. Buy \n 2. Sell \n"))

    if action == 1:
        size = int(input("Enter the size of Share : "))
        buy_order(size)
    elif action == 2:
        size = int(input("Enter the size of Share : "))
        sell_order(size)
    else:
        logging.warning("Number is incorrect. Please enter the number between 1 and 2")

def sort_values(e):
    """
    Sorts the value based on price of shares
    :param e: Individual tuple from list
    :return: price of that individual tuple
    """
    return e[1]

def buy_limit_order(price, size):
    """
    This function places the limit bid-orders
    :param price: Price of the share
    :param size: Size of the Share
    :return: Nothing
    """
    # Check whether if there exist any seller in order book
    global order_id

    if len(ask_order) == 0:
        bid_order.append([order_id, price, size])
        bid_order.sort(key=sort_values, reverse=True)
        return

    # Iterate over ask_order to fulfill the bid_order
    index = 0
    while size > 0 and index < len(ask_order):
        ask_order_price = ask_order[index][1]
        ask_order_size = ask_order[index][2]

        if price >= ask_order_price:
            temp = size
            size = size - ask_order_size
            ask_order[index][2] -= temp
        index += 1

    # If the bid_order isn't get fulfilled
    if size > 0:
        bid_order.append([order_id, price, size])
        bid_order.sort(key = sort_values, reverse = True)

    # Check to price if any value from ask has become 0
    index = 0
    while index < len(ask_order):
        price = ask_order[index][2]
        if price <= 0:
            ask_order.pop(index)
        else:
            index += 1

def sell_limit_order(price, size):
    """
    This function places the limit ask-orders
    :param price: Price of the Share
    :param size: Size of the Share
    :return:
    """
    # Check whether if there exist any seller in order book
    global order_id
    if len(bid_order) == 0:
        ask_order.append([order_id, price, size])
        ask_order.sort(key = sort_values)
        return

    # Iterate over ask_order to fulfill the bid_order
    index = 0
    while size > 0 and index < len(bid_order):
        bid_order_price = bid_order[index][1]
        bid_order_size = bid_order[index][2]

        if price <= bid_order_price:
            temp = size
            size = size - bid_order_size
            bid_order[index][2] -= temp
        index += 1

    # If the sell_order isn't get fulfilled
    if size > 0:
        ask_order.append([order_id, price, size])
        ask_order.sort(key = sort_values)

    # Check to price if any value from bid  has become 0
    index = 0
    while index < len(bid_order):
        price = bid_order[index][2]
        if price <= 0:
            bid_order.pop(index)
        else:
            index += 1


def limit_order():
    """
    Takes the input for limit order
    :return: nothing
    """
    action = int(input("\n What order you want to place? \n 1. Buy \n 2. Sell \n"))
    if action == 1:
        price, size = list(map(float,input("Enter the price at which you want to Buy and Size : ").split(" ")))
        buy_limit_order(price, int(size))
    elif action == 2:
        price, size = list(map(float,input("Enter the price at which you want to Sell and Size : ").split(" ")))
        sell_limit_order(price, int(size))
    else:
        logging.warning("Number is incorrect. Please enter the number between 1 and 2")

def cancel_order(arr, order_id):
    """
    Canel the particular order from ask and bid orders
    :param arr: Ask or Bid array
    :param order_id: unique order no of order
    :return:
    """
    for index, val in enumerate(arr):
        if val[0] == order_id:
            arr.pop(index)
            return
    logging.error("This order_id doesn't exist \n")


def helper_cancel_order():
    """
    Helper function for cancelling the order
    :return:
    """
    print("Enter the order_id of your Order : ")
    order_no = int(input())
    print("Enter the Order Type i.e Buy or Sell ? ")
    order_type = input().lower()
    if order_type == 'buy':
        cancel_order(bid_order, order_no)
    elif order_type == 'sell':
        cancel_order(ask_order, order_no)
    else:
        logging.warning("Please enter the type between Buy or Sell ")


def numbers_to_string(argument):
    """
    Acts as switch case
    :param argument: Choosed option
    :return: Function call to respective function
    """
    switcher = {
        1 : place_order,
        2 : limit_order,
        3 : helper_cancel_order
    }

    return switcher.get(argument, 'Number is incorrect. Please enter number between 1 and 3')()


order_id = 0
ask_order = []
bid_order = []

while True:
    print("\nWhat do you want to perform\n 1. Place Market Order\n 2. Place Limit Order\n 3. Cancel Particular Order\n")
    action = int(input("Enter the number of what you want to perform: "))
    order_id += 1
    numbers_to_string(action)
    print("Ask Order = ",ask_order)
    print("Bid Order", bid_order)
