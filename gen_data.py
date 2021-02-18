import os
from typing import DefaultDict 
import yaml
import csv
import argparse

from operator import itemgetter

from utils.col import *

parser = argparse.ArgumentParser(description='')
parser.add_argument('-n', required=True, dest='row_number', type=int, help='Number of rows')
parser.add_argument('-f', required=True, dest='file_path', type=str, help='config file(YAML) path')
parser.add_argument('-o', dest='outpath', type=str, help='output path')
parser.add_argument('--noheader', action='store_true', help='remove header line in output csv file')
args = parser.parse_args()

def set_col(column_info):
    if column_info["type"] == "int":
        return COL_INT(column_info)
    elif column_info["type"] == "list":
        return COL_LIST(column_info)
    elif column_info["type"] == "regex":
        return COL_REGEX(column_info)

def parser(path):
    with open(path) as yaml_file:
        schema_info = yaml.load(yaml_file, Loader=yaml.FullLoader)

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

def csv_output(n:int, col_names:list, cols:list, outfile_path:str, with_header:bool=True,  order_key:str=None) -> None:
    if len(col_names) != len(cols):
        raise Exception(f'[Schema Error] "col_names(:{len(col_names)})" len different from "cols" len(:{len(cols)})')
    if order_key != None and order_key not in col_names:
        raise Exception(f'[Config Error] "order_key(:{order_key})" is not in "col_names(:{col_names})"')

    with open(outfile_path,'w', newline='') as outcsv:
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
    outfile_path="./output/"+os.path.basename(args.file_path).replace(".yaml",".csv").replace(".yml",".csv")
    if args.outpath != None:
        outfile_path = args.outpath

    # for TEST
    path = "./configs/example.yaml"
    abs_path = os.path.abspath(path)
    
    col_names, cols, order_key = parser(abs_path)
    csv_output(10, col_names, cols, outfile_path, order_key='count')
    pass
