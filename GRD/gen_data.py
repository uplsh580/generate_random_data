import os 
import json
import csv

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
  
    # # TEST
    # for i, col in enumerate(cols):
    #     print(col_names[i], ":", col.gen_data())
  
    return col_names, cols


def csv_output(rows:int, col_names:list, cols:list, output_path:str, file_name, with_header:bool=True) -> None:
    if output_path != '' and output_path[-1] != '/':
        output_path += '/'

    if len(col_names) != len(cols):
        raise Exception('Schema Error: "col_names" len different from "cols" len')
    with open(output_path+file_name,'w', newline='') as outcsv:
        wr = csv.writer(outcsv)

        if with_header:
            wr.writerow(col_names)
        
        for i in range(rows):
            row = map(lambda col : col.gen_data(), cols)
            wr.writerow(row)
    outcsv.close()


if __name__ == '__main__':
    path = "./configs/example.json"
    abs_path = os.path.abspath(path)
    
    col_names, cols = parser(abs_path)
    csv_output(10, col_names, cols, './output/', 'example.csv')
    pass
