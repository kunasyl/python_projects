import json
import pandas as pd
import re
import os
import cx_Oracle

f = open('file2.json', 'r')
# f = open('file1.json', 'r')
data = json.load(f)

cols = ['id', 'name', 'url', 'location_address', 'location_locality', 'location_city', 'location_city_id',
        'location_latitude', 'location_longitude', 'location_zipcode', 'location_country_id',
        'location_locality_verbose', 'switch_to_order_menu', 'cuisines', 'average_cost_for_two',
        'price_range', 'currency', 'thumb', 'user_rating_aggregate_rating', 'user_rating_rating_text',
        'user_rating_rating_color', 'user_rating_votes', 'photos_url', 'menu_url', 'featured_image',
        'has_online_delivery', 'is_delivering_now', 'deeplink', 'has_table_booking', 'events_url', 'book_url',
        'zomato_events_0_event_event_id', 'zomato_events_0_event_friendly_start_date',
        'zomato_events_0_event_friendly_end_date', 'zomato_events_1_event_friendly_start_date',
        'zomato_events_1_event_friendly_end_date', 'zomato_events_1_event_start_date',
        'zomato_events_1_event_end_date', 'zomato_events_1_event_disclaimer','zomato_events_2_event_title',
        'zomato_events_2_event_description']


def flatten(d, sep="_"):
    obj = {}

    def recurse(t, parent_key=""):
        if isinstance(t, list):
            for i in range(len(t)):
                recurse(t[i], parent_key + sep + str(i) if parent_key else str(i))
        elif isinstance(t, dict):
            for k, v in t.items():
                recurse(v, parent_key + sep + k if parent_key else k)
        else:
            if parent_key.find('restaurant') != -1:
                obj[parent_key] = t

    recurse(d)

    return obj


ready_data = flatten(data)
# print(ready_data)

def get_restaurants(data):
    prev = 0
    counter = 0
    rests = {}
    obj = {}
    for k, v in data.items():
        # get index of restaurant
        print(re.findall('\d+', k))
        i = int(re.findall("\d+", k)[1])
        # if we got next restaurant data
        if i != prev:
            # save current restaurant's data
            rests[counter] = dict(zip(obj.keys(), obj.values()))
            obj.clear()
            prev = i
            counter += 1
        obj_key = re.sub("\d+\_restaurants\_\d+\_restaurant\_", "", k)
        if obj_key in cols:
            obj[obj_key] = v

    return rests


rests = get_restaurants(ready_data)
print(rests)

rests_df = pd.DataFrame.from_dict(rests, orient='index')

# formatting dataframe
rests_df['zomato_events_0_event_event_id'].fillna(0, inplace=True)
rests_df['zomato_events_0_event_event_id'] = rests_df['zomato_events_0_event_event_id'].astype(int)
rests_df.fillna('', inplace=True)
num_cols = ['location_city_id', 'location_country_id', 'switch_to_order_menu', 'average_cost_for_two',
            'price_range', 'has_online_delivery', 'is_delivering_now', 'has_table_booking']
for col in num_cols:
    rests_df[col] = rests_df[col].astype(int)

# convert to records type
rests_rec = rests_df.values.tolist()


# connecting to xepdb1 as connie
conn = cx_Oracle.connect(
    user="connie",
    password="connie",
    dsn="localhost/xepdb1"
)

def sql_insert(table_name, records):
    insert_query = '''
        INSERT INTO {table_name}
        VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,
                :21,:22,:23,:24,:25,:26,:27,:28,:29,:30,:31,:32,:33,:34,:35,:36,:37,:38,:39,:40,:41)
    '''.format(table_name=table_name)

    cursor = conn.cursor()
    try:
        cursor.executemany(insert_query, records)
        conn.commit()
    except cx_Oracle.IntegrityError as e:
        error_obj, = e.args
        print(f"Error message: , {error_obj.message}")
    else:
        print(f"{cursor.rowcount}, rows successfully inserted")
    finally:
        cursor.close()

# execute insertion into rests table
sql_insert('rests', rests_rec)

conn.close()