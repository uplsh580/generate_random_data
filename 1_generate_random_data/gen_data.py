import os 
import json

from utils.col import *

def set_col(columns_info):
    if columns_info["type"] == "int":
        return COL_INT(columns_info)
    elif columns_info["type"] == "date":
        pass
    elif columns_info["type"] == "time":
        pass
    elif columns_info["type"] == "list":
        return COL_LIST(columns_info)

def parser(path):
    with open(path) as json_file:
        schema_info = json.load(json_file)
    
    order_key = None
    if "order_by" in schema_info:
        order_key = schema_info["order_by"]
    
    col_names = []
    cols = []
    for c_name, c_info in schema_info["columns"].items():
        col = set_col(c_info)

        if col is None:
            continue

        cols.append(col)
        col_names.append(c_name)
    
    for i, col in enumerate(cols):
        print(col_names[i], ":", col.gen_data())

if __name__ == '__main__':
    path = "./configs/example.json"
    abs_path = os.path.abspath(path)
    
    parser(abs_path)
    pass
