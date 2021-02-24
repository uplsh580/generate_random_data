# GRD: Generate Random Data
![GitHub release (latest by date)](https://img.shields.io/github/v/release/uplsh580/generate_random_data?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/uplsh580/generate_random_data?style=for-the-badge)
<br>
Generate random data and saves it as .csv file.
<hr>

## Installation
* Clone this repo. and enter it
    ```
    git clone https://github.com/uplsh580/generate_random_data.git
    cd generate_random_data
    ```
* Set up the environment using one of the following options:
    * Option1. Manually with pip
        1. Set up a **Python3** 
            * Recommended Version: `python 3.7.*`
        2. Install packages:
            ```
            pip install -r requirement.txt
            ```
    * Option2. Using Docker
        1. run `drun.sh` shell script.
            ```
            ./drun.sh --run
            ```
<hr>

## Quick Start
* Run `gen_data.py`
    ```
    python gen_data.py -n 10 -f configs/example.yaml
    ```
* Check the result csv file. (`./output/example.csv`) <br>
    * You can find csv file like below.
        ```
        datetime,user_id,count,event,score
        2020-01-01 00:05:31,USER7896,1000,event2,23.6367
        2020-01-09 12:45:43,USER0517,0,event3,0.5963
        2020-01-11 20:12:32,USER6713,0,event3,85.2828
        2020-01-14 17:43:28,USER3086,4000,event3,69.829
        2020-01-27 22:49:21,USER4707,8500,event3,7.31
        2020-02-02 01:26:51,USER5346,2500,event3,40.2701
        2020-02-14 13:00:45,USER4050,7500,event3,71.3598
        2020-02-15 18:28:33,USER5319,4500,event3,28.7195
        2020-02-16 17:32:08,USER2759,3500,event2,65.7312
        2020-03-02 04:38:44,USER8396,2500,event3,56.5897
        ```
<hr>

## Arguments and Options
* Arguments
    * `-n`: Number of data row to generate
    * `-f`: config file path
    * `-o`: **(Optional)** Output File Directory (Default : `output/`)
* Options
    * `--noheader`: **(Optional)** Remove the header from the csv file to be output.


<hr>

## How to Write config file?
### Layout of YAML
```
version: 1
order_by: [column_name]
columns:
    [column_name]:
        type: [type]
        ...
    ...
```
* `version`: Config File Interpretation Version 
    * Currently, only `1` is available.
* `order_by`: (**Optional**) Column name to be sorted at the output. 
    * Must exist in columns.
* `columns`: The column info to be output. 
    * The columns are printed in the order in which were written.

### Available Column Types
#### **INT**
* Format
    ```
    [column_name]:
        type: int
        min: 
        max:
        unit:
    ```
    * `min`: Min number of range
    * `max`: Max number of range
    * `unit`: (**Optional**) Unit of number (*e.g unit is 500 : 500, 1000, 1500, ...*)
* Example
    ```
    count:
        type: int
        min: 0
        max: 10000
        unit: 500
    ```
#### **REGEX**
* Format
    ```
    [column_name]:
        type: regex
        regex:
    ```
    * `regex`: A regular expression to randomly generate. <br>
    Regular Expression Language - Quick Reference ([Link](https://docs.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference))
* Example
    ```
    user_id:
        type: regex
        regex: USER\d\d\d\d
    ```
#### **LIST**
* Format
    ```
    [column_name]:
        type: list
        list:
        ratio:
    ```
    * `list`: The list to enter randomly.
    * `ratio`: (**Optional**) Random rate. 
        * Write it in an integer format in the **same order** as the list.
        * Default : Fair
* Example
    ```
    event:
        type: list
        list: ["event1", "event2", "event3"]
        ratio: [2,3,10]
    ```
#### **DATETIME**
* Format
    ```
    [column_name]:
        type: datetime
        start_dt:
        end_dt:
        output_format:
    ```
    * `start_dt`: Start date. 
        * Write in **YYYY-MM-DD HH:MM:SS** format. (*e.g 2021-02-20 08:38:23*)
    * `end_dt`: End date.
        * Write in **YYYY-MM-DD HH:MM:SS** format. (*e.g 2021-01-20 08:38:23*)
    * `output_format`: (**Optional**) The output format for datetime.
        * Enclose in **quotation marks (" ")**.
        * The format follows the python `datetime` ([Link](https://www.w3schools.com/python/python_datetime.asp))
        * Default format : "%Y-%m-%d %H:%M:%S"
* Example
    ```
    datetime:
        type: datetime
        start_dt: 2020-01-01 00:00:00
        end_dt: 2020-03-04 00:00:00
        output_format: "%Y-%m-%d %H:%M:%S"
    ```

#### **DECIMAL**
* Format
    ```
    [column_name]:
        type: decimal
        min:
        max:
        point_move:
        decimal_len:
    ```
    * `min`: Min number of range
        * Input Range: -1 ~ 1
    * `max`: Max number of range
        * Input Range: -1 ~ 1
    * `point_move`: (**Optional**) Move the point. If the input number is positive, move the integer direction and the other is the negative decimal direction.
        * Input Range: -16 ~ 16
        * Default : 0
    * `decimal_len`: (**Optional**) Enter the length of the decimal part.
        * Input Range: 0 ~ 16
        * Default : 4

* Example
    ```
    score:
        type: decimal
        min: -0.1
        max: 0.9
        point_move: 2
        decimal_len: 4
    ```
