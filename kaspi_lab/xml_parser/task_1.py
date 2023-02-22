import glob
import os
from xml.etree.ElementTree import parse
import pandas as pd
import oracle_funcs

# get columns from table
cols = oracle_funcs.get_columns('lab10')
col_names = [item.lower() for t in cols for item in t]


# parsing xml files
def xml_parser(xml_doc, sep='_'):
    doc_root = parse(xml_doc).getroot()
    obj = {}

    def recurse(root, parent_key=''):
        for child in root:
            children = list(root.iterfind(child.tag))
            end_str = sep + str(children.index(child) + 1) + sep if len(children) > 1 else sep
            recurse(child, child.tag + end_str if root == doc_root else parent_key + child.tag + end_str)
        obj_key = parent_key[:-1] if parent_key[:-1] in col_names else parent_key.replace('_1', '')[:-1]
        if obj_key in col_names:
            obj[obj_key] = root.text

    recurse(doc_root)

    return obj


def xml_to_records(path):
    xml_dict = {}
    for i, filename in enumerate(glob.glob(os.path.join(path, "*.xml"))):
        with open(filename, 'r', encoding="utf-8") as content:
            xml_dict[i] = xml_parser(content)

    df = pd.DataFrame.from_dict(xml_dict, orient='index')
    df = df[col_names]
    df = df.where(pd.notnull(df), None)

    return df.values.tolist()

