from xml.etree.ElementTree import parse
import pandas as pd
import re
import oracle_funcs

# get columns from table
cols = oracle_funcs.get_columns('lab10_2')
col_names = [item.lower() for t in cols for item in t]


# parsing xml files
def xml_parser(xml_doc, sep='_'):
    doc_root = parse(xml_doc).getroot()
    obj = {}

    def recurse(root, parent_key='', obj_val=''):
        for child in root:
            children = list(root.iterfind(child.tag))
            end_str = sep + str(children.index(child)) + sep if len(children) > 1 else sep
            if child.tag == 'row':
                recurse(child, parent_key + child.tag + end_str + 'number' + sep, child.attrib['number'])
            if child.tag == 'value':
                recurse(child, parent_key + child.tag + sep + 'year' + sep + child.attrib['year'] + sep, child.text)
            recurse(child, child.tag + end_str if root == doc_root else parent_key + child.tag + end_str, child.text)

        obj[parent_key[:-1]] = obj_val

    recurse(doc_root)

    return obj


def get_formatted_data(doc):
    tables = {}
    rows = {}
    data = {}
    table_counter = 0
    row_counter = 0

    table_const_keys = ['table_name', 'table_number', 'table_data_row_number', 'table_data_row_number_label']
    table_const_vals = {}

    for k, v in doc.items():
        if 'year' in k:
            new_k = re.sub('_\d+', '', k, 2).replace('_row_number', '')
        else:
            new_k = re.sub('_\d+', '', k)
        if new_k not in col_names:
            continue

        # add values of tables
        if len(re.findall('\d+', k)) > 0:
            if int(re.findall('\d+', k)[0]) != table_counter:
                tables[table_counter] = {row_k: row_v for row_k, row_v in rows.items()}
                rows.clear()
                table_counter = int(table_const_vals['table_number'])

        # add values of rows
        if len(re.findall('\d+', k)) > 1:
            if int(re.findall('\d+', k)[1]) != row_counter:
                for table_k, table_v in table_const_vals.items():
                    data[table_k] = table_v
                rows[row_counter] = {data_k: data_v for data_k, data_v in data.items()}
                data.clear()
                row_counter = int(table_const_vals['table_data_row_number'])

        # add values of data
        # save table's constant data values
        if new_k in table_const_keys:
            table_const_vals[new_k] = v
        else:
            data[new_k] = v

    return tables


def get_records(data):
    rows = {}
    for table_k, table_v in data.items():
        for row_k, row_v in table_v.items():
            rows[row_k] = row_v
    df = pd.DataFrame.from_dict(rows, orient='index')
    df = df[col_names[2:] + col_names[:2]]
    df = df.where(pd.notnull(df), None)

    return df.values.tolist()














