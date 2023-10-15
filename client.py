import binance

# import pandas
# import time

API_KEY = "aae31fbdda8ade4aa2b81e4aff617356ab45d0d671928d5eaf13574cad16f90b"
API_SECRET = "47979204b9fbb8b3ada61824a775d9777c963b64a5a70a50740903facb4850ee"

binance_client = binance.Client(
    api_key=API_KEY, api_secret=API_SECRET, tld="com", testnet=True
)
LONG = binance_client.SIDE_BUY
SHORT = binance_client.SIDE_SELL
SYMBOL = "BTCUSDT"
INITIAL_QUANTITY = 0.01
DECIMALS = 2
CYCLES = 1
INITIAL_DEVIATION = -1
STEP = 1.2
SAFETY_ORDERS = 6
VOLUME_MULTIPLIER = 1.5
LEVERAGE = 3

quantity = INITIAL_QUANTITY
direction = LONG


def get_balance():
    futures_account = binance_client.futures_account()
    # print(futures_account)
    # df = pandas.DataFrame(futures_account["assets"])
    print(futures_account["assets"])


def create_market_order(symbol, side, quantity, leverage=LEVERAGE):
    output = binance_client.futures_create_order(
        symbol=symbol,
        side=side,
        type=binance_client.FUTURE_ORDER_TYPE_MARKET,
        quantity=quantity,
        leverage=leverage,
    )
    print(output)


def create_buy_limit_order(symbol, quantity, price):
    output = binance_client.futures_create_order(
        symbol=symbol,
        side=binance_client.SIDE_BUY,
        type=binance_client.FUTURE_ORDER_TYPE_LIMIT,
        timeInForce=binance_client.TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=price,
    )
    print(output)


def create_sell_limit_order(symbol, quantity, price):
    output = binance_client.futures_create_order(
        symbol=symbol,
        side=binance_client.SIDE_SELL,
        type=binance_client.FUTURE_ORDER_TYPE_LIMIT,
        timeInForce=binance_client.TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=price,
    )
    print(output)


def place_take_profit(symbol, price, quantity, direction):
    try:
        if direction == binance_client.SIDE_BUY:
            create_sell_limit_order(symbol, quantity, price)
        else:
            create_buy_limit_order(symbol, quantity, price)
    except Exception as ex:
        print(ex)
        place_take_profit(symbol, price, quantity, direction)


def close_position(symbol, side):
    positions = binance_client.futures_get_open_orders(symbol=symbol)
    side_positions = [position for position in positions if position["side"] == side]
    for side_position in side_positions:
        binance_client.futures_cancel_order(
            symbol=symbol, orderId=side_position["orderId"]
        )


def _get_average_price(symbol):
    return binance_client.get_avg_price(symbol=symbol).get("price")


def get_market_price(symbol):
    return float(binance_client.get_symbol_ticker(symbol=symbol).get("price"))


def calculate_deviation(direction, initial_price, current_price):
    deviation = ((current_price - initial_price) / initial_price) * 100
    if direction == binance_client.SIDE_BUY:
        return deviation
    else:
        return -deviation


def calculate_total_profit(symbol, total_profit, decimals):
    position_info = binance_client.futures_position_information()
    quantity = position_info.get()


def run(symbol):
    for i in range(CYCLES):
        is_ok = True
        while is_ok:
            create_market_order(symbol, direction, quantity)
            initial_price = get_market_price(SYMBOL)


# print(get_market_price("BTCUSDT"))
# price1 = get_market_price("BTCUSDT")
# print(f"p1: {price1}")
# time.sleep(10)
# price2 = get_market_price("BTCUSDT")
# print(f"p2: {price1}")
# print(calculate_deviation(binance_client.SIDE_BUY, price1, price2))
# get_balance()
# create_order()
# get_balance()
symbol = SYMBOL
# create_market_order(symbol, LONG, quantity)
positions = binance_client.futures_position_information(symbol=symbol)
positions = [position for position in positions if float(position["positionAmt"]) > 0]
take_profit = 400
if positions:
    position = positions[0]
    position_amt = float(position["positionAmt"])
    entry_price = float(position["entryPrice"])
    leverage = float(position["leverage"])
    margin = entry_price * abs(position_amt / leverage)
    profit = margin * take_profit * 0.01
    price = round((profit * position_amt) + entry_price, DECIMALS)
    total_quantity = sum(map(lambda p: float(p["positionAmt"]), positions))
    print(price, margin, profit, position_amt, entry_price, total_quantity)
    # return price, total_quantity

print(positions)
