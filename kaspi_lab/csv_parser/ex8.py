
import pandas as pd
    import cx_Oracle
from concurrent.futures import ThreadPoolExecutor
import time

# Connecting to xepdb1 as connie

conn = cx_Oracle.connect(
    user="connie",
    password="connie",
    dsn="localhost/xepdb1"
)

# Test connection

cur = conn.cursor()
cur.execute("SELECT table_name FROM user_tables ORDER BY table_name ASC")
res = cur.fetchall()
for row in res:
    print(row)
cur.close()


# Importing csv files

in_v = pd.read_csv('D:\kaspi_lab_2021\\3. Python\Урок 8\INvideos.csv')
kr_v = pd.read_csv('D:\kaspi_lab_2021\Python\Урок 8\KRvideos.csv')


# Formatting

def format_df(df):
    df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')
    df['trending_date'] = df['trending_date'].dt.strftime('%d.%m.%y')

    df['publish_time'] = pd.to_datetime(df['publish_time'])

    for col in ['comments_disabled', 'ratings_disabled', 'video_error_or_removed']:
        df[col] = df[col].astype(int)

    df['description'].fillna('', inplace=True)

    df_rec = df.values.tolist()
    return df_rec


in_v_rec = format_df(in_v)
kr_v_rec = format_df(kr_v)


# SQL insert using threads

def sql_insert(table_name, records):
    insert_query = '''
        INSERT INTO {table_name}
        VALUES (:1, TO_DATE(:2,'DD-MM-YY'),:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16)
    '''.format(table_name=table_name)

    cursor = conn.cursor()
    try:
        cursor.executemany(insert_query, records)
        conn.commit()
    except cx_Oracle.IntegrityError as e:
        error_obj, = e.args
        return f"Error message: , {error_obj.message}"
    else:
        return f"{cursor.rowcount}, rows successfully inserted"
    finally:
        cursor.close()


args = [('in_videos', in_v_rec), ('kr_videos', kr_v_rec)]
t1 = time.perf_counter()
with ThreadPoolExecutor() as exe:
    exe.map(lambda p: sql_insert(*p), args)
t2 = time.perf_counter()

print(f'MultiThreaded Code Took:{t2 - t1} seconds')

conn.close()