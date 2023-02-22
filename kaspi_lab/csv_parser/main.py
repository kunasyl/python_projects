
import pandas as pd
import cx_Oracle

# Connecting to xepdb1 as connie

conn = cx_Oracle.connect(
    user = "connie",
    password = "connie",
    dsn = "localhost/xepdb1"
)


# Test connection

cur = conn.cursor()
cur.execute("SELECT table_name FROM user_tables ORDER BY table_name ASC")
res = cur.fetchall()
for row in res:
    print(row)
cur.close()


# Importing csv files

processed = pd.read_csv('D:\kaspi_lab_2021\Processed.csv')
data = pd.read_csv('D:\kaspi_lab_2021\Data.csv')
info = pd.read_csv('D:\kaspi_lab_2021\\Info.csv')


# Data formatting

processed.loc[max(processed.index)+1, :] = None
processed = processed.iloc[:].shift(1)
cols = [1,'HSI','1986-12-31',2568.300049, 2568.300049,
       2568.300049, 2568.300049, 2568.300049, 0, 333.87900637]
processed.iloc[0] = cols

data['key'] = data['key'].astype(float)
data = data.dropna()

processed_rec = processed.values.tolist()
data_rec = data.values.tolist()
info_rec = info.values.tolist()


# SQL insert scripts

processed_insert = '''
    INSERT INTO processed
    VALUES (:1,:2,TO_DATE(:3,'YYYY-MM-DD'),:4,:5,:6,:7,:8,:9,:10)
'''

data_insert = '''
    INSERT INTO data
    VALUES (:1,:2,TO_DATE(:3,'YYYY-MM-DD'),:4,:5,:6,:7,:8,:9)
'''

info_insert = '''
    INSERT INTO info
    VALUES (:1,:2,:3,:4)
'''


def sql_insert(sql_script, records):
    try:
        cursor = conn.cursor()
        cursor.executemany(sql_script, records)
        conn.commit()
    except cx_Oracle.IntegrityError as e:
        error_obj, = e.args
        print("Row ", cursor.rowcount, "has error")
        print("Error message: ", error_obj.message)
    else:
        print(cursor.rowcount, "rows successfully inserted")
    finally:
        cursor.close()


sql_insert(processed_insert, processed_rec)
sql_insert(data_insert, data_rec)
sql_insert(info_insert, info_rec)

conn.close()