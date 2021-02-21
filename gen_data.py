import os
import yaml
import csv
import argparse
from operator import itemgetter
from utils.col import COL_INT, COL_REGEX, COL_LIST, COL_DATETIME

parser = argparse.ArgumentParser(description='')
parser.add_argument('-n', required=True, dest='row_number', type=int,
                    help='Number of rows')
parser.add_argument('-f', required=True, dest='file_path', type=str,
                    help='config file(YAML) path')
parser.add_argument('-o', dest='outfile_dir', type=str, default="output/",
                    help='output file directory')
parser.add_argument('--noheader', action='store_true',
                    help='remove header line in output csv file')
args = parser.parse_args()


def set_col(column_info):
    if column_info["type"] == "int":
        return COL_INT(column_info)
    elif column_info["type"] == "regex":
        return COL_REGEX(column_info)
    elif column_info["type"] == "list":
        return COL_LIST(column_info)
    elif column_info["type"] == "datetime":
        return COL_DATETIME(column_info)

    raise Exception(f'[Config Error] "{column_info["type"]}" is not a supported type.')


def parser(path):
    with open(path) as yaml_file:
        schema_info = yaml.load(yaml_file, Loader=yaml.FullLoader)

    order_key = None
    if "order_by" in schema_info:
        order_key = schema_info["order_by"]

    col_names = []
    col_instances = []
    for c_name, c_info in schema_info["columns"].items():
        col = set_col(c_info)
        if col is None:
            continue
        col_instances.append(col)
        col_names.append(c_name)

    return col_names, col_instances, order_key


def csv_output(n: int, col_names: list, col_instances: list, outfile_path: str,
               with_header: bool = True,  order_key: str = None) -> None:
    if len(col_names) != len(col_instances):
        raise Exception(f'[Internal Error] "col_names({len(col_names)})" len different from "cols" len({len(col_instances)})')
    if order_key is not None and order_key not in col_names:
        raise Exception(f'[Config Error] "order_key({order_key})" is not in "col_names({col_names})"')

    with open(outfile_path, 'w', newline='') as outcsv:
        rows = []
        for i in range(n):
            rows.append(list(map(lambda col: col.gen_data(), col_instances)))

        if order_key is not None:
            order_index = col_names.index(order_key)
            rows = sorted(rows, key=itemgetter(order_index))

        wr = csv.writer(outcsv)
        if with_header:
            wr.writerow(col_names)
        for row in rows:
            wr.writerow(row)


if __name__ == '__main__':
    outfile_dir = os.path.abspath(args.outfile_dir)
    outfile_name = os.path.basename(args.file_path)
    outfile_name = outfile_name.replace(".yml", ".csv").replace(".yaml", ".csv")

    outfile_path_abs = outfile_dir + '/' + outfile_name

    config_path_abs = os.path.abspath(args.file_path)
    col_names, col_instances, order_key = parser(config_path_abs)

    csv_output(args.row_number, col_names, col_instances,
               outfile_path_abs, order_key=order_key)
