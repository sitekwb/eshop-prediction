import json
from datetime import datetime

folder = 'data'

with open(folder + '/events.json') as file:
    events_list = json.load(file)

with open(folder + '/products.json') as file:
    products_list = json.load(file)

with open(folder + '/users.json') as file:
    users_list = json.load(file)

# CITY

cities = [user['city'] for user in users_list]
user_ids = [user['user_id'] for user in users_list]

import pandas as pd

one_hot_cities = pd.get_dummies(cities).values.tolist()
one_hot_cities = dict(zip(user_ids, one_hot_cities))

products = dict()

prices = dict()
categories = list()
product_ids = list()

for product in products_list:
    pr_id = product['product_id']
    prices[pr_id] = product['price']
    categories.append(product['category_path'])
    product_ids.append(pr_id)

one_hot_categories = pd.get_dummies(categories).values.tolist()
one_hot_categories = dict(zip(product_ids, one_hot_categories))

events = []
buys = []

last_session_id = -1

time = 0
last_datetime = datetime.now()

for event in events_list:
    # time

    if event['event_type'] == 'BUY_PRODUCT':
        buys[-1] = 1
        continue

    current_datetime = datetime.strptime(event['timestamp'], '%Y-%m-%dT%H:%M:%S')
    time = current_datetime - last_datetime
    last_datetime = current_datetime

    current_session_id = event["session_id"]
    if last_session_id != current_session_id:
        last_session_id = current_session_id
        time = current_datetime - current_datetime

    time = time.total_seconds()

    events_dict = {'session_id': event['session_id'],
                   'user_id': event['user_id'],
                   'time': time,
                   'price': prices[event['product_id']],
                   'discount': event["offered_discount"]
                   }

    # cities
    one_hot_cities_list = one_hot_cities[event['user_id']]
    i = 0
    for one_hot in one_hot_cities_list:
        events_dict['one_hot_city' + str(i)] = one_hot
        i += 1

    # TODO categories
    one_hot_categories_list = one_hot_categories[event['product_id']]
    i = 0
    for one_hot in one_hot_categories_list:
        events_dict['one_hot_category' + str(i)] = one_hot
        i += 1

    buys.append(0)
    events.append(events_dict)

with open('records2.json', 'w') as file:
    json.dump(events,
              file, indent=2)

with open('buys2.json', 'w') as file:
    json.dump(buys,
              file, indent=2)

print("Zapisano rekordy w pliku json")
