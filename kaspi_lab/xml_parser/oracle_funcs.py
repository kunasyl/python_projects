import cx_Oracle

# connecting to xepdb1 as connie
conn = cx_Oracle.connect("connie/connie@localhost/xepdb1")


# get column names from table
def get_columns(table_name):
    cur = conn.cursor()

    cur.execute(f"""SELECT COLUMN_NAME
                   FROM USER_TAB_COLUMNS
                   WHERE TABLE_NAME = '{table_name.upper()}'"""
                .format(table_name=table_name))

    columns = cur.fetchall()
    cur.close()
    return columns


# inserting
def sql_insert(table_name, records):
    cur = conn.cursor()
    cur.execute(f"select * from {table_name}")
    bind_names = ",".join(":" + str(i + 1) \
                          for i in range(len(cur.description)))
    cur.close()

    insert_query = '''
        INSERT INTO {table_name}
        values ({bind_names})
    '''.format(table_name=table_name, bind_names=bind_names)

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
        conn.close()