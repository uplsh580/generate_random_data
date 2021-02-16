import os 
import json
import csv
from operator import itemgetter

from utils.col import *

def set_col(column_info):
    if column_info["type"] == "int":
        return COL_INT(column_info)
    elif column_info["type"] == "date":
        pass
    elif column_info["type"] == "time":
        pass
    elif column_info["type"] == "list":
        return COL_LIST(column_info)

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

    return col_names, cols, order_key

def csv_output(n:int, col_names:list, cols:list, output_path:str, file_name:str, with_header:bool=True,  order_key:str=None) -> None:
    if output_path != '' and output_path[-1] != '/':
        output_path += '/'

    if len(col_names) != len(cols):
        raise Exception(f'Schema Error: "col_names(:{len(col_names)})" len different from "cols" len(:{len(cols)})')
    if order_key != None and order_key not in col_names:
        raise Exception(f'Order Key Error: "order_key(:{order_key})" is not in "col_names(:{col_names})"')

    with open(output_path+file_name,'w', newline='') as outcsv:
        rows = []
        for i in range(n):
            rows.append(list(map(lambda col : col.gen_data(), cols)))
        
        if order_key != None:
            order_index = col_names.index(order_key)
            rows = sorted(rows, key=itemgetter(order_index))

        wr = csv.writer(outcsv)

        if with_header:
            wr.writerow(col_names)

        for row in rows:
            wr.writerow(row)

    outcsv.close()

if __name__ == '__main__':
    path = "./configs/example.json"
    abs_path = os.path.abspath(path)
    
    col_names, cols, order_key = parser(abs_path)
    csv_output(10, col_names, cols, './output/', 'example.csv', order_key='user_id')
    pass
