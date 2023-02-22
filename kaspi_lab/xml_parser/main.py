
import task_1
import task_2
import oracle_funcs

if __name__ == '__main__':
    # task 1
    task_1_recs = task_1.xml_to_records('HW_10_task_1/')
    # execute insertion into lab10 table
    oracle_funcs.sql_insert('lab10', task_1_recs)

    # task 2
    doc = task_2.xml_parser('HW_10_task_2/AEO 2011 Final.xml')
    res = task_2.get_formatted_data(doc)
    recs = task_2.get_records(res)
    oracle_funcs.sql_insert('lab10_2', recs)




