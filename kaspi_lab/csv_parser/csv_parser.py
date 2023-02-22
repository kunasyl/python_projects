
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

calendar = pd.read_csv('D:\kaspi_lab_2021\Урок 4\Calendar_Test_Data.csv')
calendar_rec = calendar.values.tolist()


# SQL insert scripts

calendar_insert = '''
    INSERT INTO calendar
    VALUES (TO_DATE(:1,'YYYY-MM-DD'),:2,:3,:4,:5,:6,:7,:8)
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
 

sql_insert(calendar_insert, calendar_rec)

conn.close()