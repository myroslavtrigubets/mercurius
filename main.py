import json
import datetime
from exmo3 import ExmoAPI


array_json = open("settings.json", "r").read()
settings = json.loads(array_json)

ExmoAPI_instance = ExmoAPI(settings["APIkey"], settings["APIsecret"])
user_info = ExmoAPI_instance.api_query('user_info')
print("XRP",user_info["balances"]["XRP"]," ","USD",user_info["balances"]["USD"])
print("UAH",user_info["balances"]["UAH"]," ","BTC",user_info["balances"]["BTC"])

while True:
    print("[1] - account balance")
    print("[2] - open orders")
    print("[3] - create a purchase order")
    print("[4] - create a sale order")
    print("[5] - trades deals")
    print("[6] - сounting the purchase price")
    print("[7] - addresses for the deposit")
    print("")
    command = str(input(">>> "))
    if command == "exit":
        break

    elif int(command) == 1:
        user_info = ExmoAPI_instance.api_query('user_info')
        print("XRP",user_info["balances"]["XRP"]," ","USD",user_info["balances"]["USD"])
        print("UAH",user_info["balances"]["UAH"]," ","BTC",user_info["balances"]["BTC"])
        print("")

    elif int(command) == 2:
        print(" pair "," order_id " "    datetime    ", "  type ", " quantity  ", " price  ", " amount  ")

        user_open_orders = ExmoAPI_instance.api_query('user_open_orders')
        for keys,values in user_open_orders.items():
            for i in range(len(values)):
                print(keys, values[i]['order_id'], datetime.datetime.fromtimestamp(values[i]['created']).strftime('%Y-%m-%d %H:%M:%S'),\
                values[i]['type'], values[i]['quantity'], values[i]['price'], values[i]['amount'])
        print("")

    elif int(command) == 3:
        print("Pairs", "1 - XRP_USD","2 - USD_XRP")
        print("Type","1 - buy","2 - sell")
        print("example: pair quantity price type")
        order = input()
        if order == "exit":
            continue
        order = order.split(" ")
        pairs = ["XRP_USD","USD_XRP"]
        types = ["buy","sell"]

        pair = pairs[int(order[0]) - 1]
        quantity = float(order[1])
        price = float(order[2])
        type = types[int(order[3]) - 1]

        order_create = ExmoAPI_instance.api_query('order_create',{"pair":pair, "quantity":quantity, "price":price, "type":type})
        print("result",order_create['result'], "order_id", order_create['order_id'])
        print("")

    elif int(command) == 4:
        user_open_orders = ExmoAPI_instance.api_query('user_open_orders',{"pair":"XRP_BTC,XRP_USD,USD_XRP"})
        print(" pair ", " order_id ", " type ", " price "," quantity " " amount ")
        for keys,values in user_open_orders.items():
            for i in range(len(values)):
                print(keys, values[i]['order_id'], values[i]['type'], values[i]['price'], values[i]['quantity'], values[i]['amount'])
        order_id = input("select the order_id to cancel >>> ")
        if order_id == "exit":
            continue
        order_id = int(order_id)
        order_cancel = ExmoAPI_instance.api_query('order_cancel',{"order_id":order_id})
        print("result",order_create['result'])
        print("")

    elif int(command) == 5:
        user_trades = ExmoAPI_instance.api_query('user_trades',{"pair":"XRP_BTC,XRP_USD,USD_XRP"})
        print(" pair ", "     datetime     ", "  type ", " quantity  ", " price  ", " amount  ")
        for keys,values in user_trades.items():
            for i in range(len(values)):
                print(keys,datetime.datetime.fromtimestamp(values[i]['date']).strftime('%Y-%m-%d %H:%M:%S'),\
                values[i]['type'], values[i]['quantity'], values[i]['price'], values[i]['amount'])
        print("")

    elif int(command) == 6:
        print("1 - XRP_USD","2 - USD_XRP")
        print("example: pair quantity")
        amount = input()
        if amount == "exit":
            continue
        amount = amount.split(" ")
        pairs = ["XRP_USD","USD_XRP"]

        pair = pairs[int(amount[0]) - 1]
        quantity = int(amount[1])

        required_amount = ExmoAPI_instance.api_query('required_amount',{"pair":pair, "quantity":quantity})
        print("quantity =",required_amount['quantity'],"amount =",required_amount['amount'],"avg price =",required_amount['avg_price'], )
        print("")

    elif int(command) == 7:
        deposit_address = ExmoAPI_instance.api_query('deposit_address')
        for keys,values in deposit_address.items():
            print(keys,values)
        print("")
