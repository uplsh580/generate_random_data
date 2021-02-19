# GRD: Generate Random Data
Creates random data for a csv form.
## Installation
* Clone this repo. and enter it
    ```
    git clone https://github.com/uplsh580/generate_random_data.git
    cd generate_random_data
    ```
* Set up the environment using one of the following methids:
    * Manually with pip
        * Set up a Python3(recommendation version : 3.7.*) environment (e.g. virtenv)
        * Install packages:
            ```
            pip install -r requirement.txt
            ```
    * Using Docker
        ```
        ./drun.sh --run
        ```

## Quick Start
* Run `gen_data.py`
    ```
    python gen_data.py -n 10 -f configs/example.yaml
    ```
* Check the result csv file. (`./output/example.csv`) <br>
    You can find csv file like below.
    ```
    user_id,count,event
    USER0862,2000,event3
    USER3258,5500,event2
    USER4921,9000,event2
    USER5777,1000,event1
    USER6379,3500,event1
    USER6822,7500,event2
    USER8718,4500,event1
    USER8807,5500,event3
    USER8999,4000,event3
    USER9277,6500,event3
    ```

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
* `version`: Config File Interpretation Version (Currently, only `1` is available.)
* `order_by`: Column name to be sorted at output. (Must exist in columns.)
* `columns `: The column setting to be output. The columns are printed in the order in which were written.

### Available Column Types
* int
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
        * `unit`: (**Optional**) Unit of number (e.g unit is 500 : 500, 1000, 1500, ...)
    * Example
        ```
        count:
            type: int
            min: 0
            max: 10000
            unit: 500
        ```
* regex
    * Format
        ```
        [column_name]:
            type: regex
            regex:
        ```
        * `regex`: A regular expression to randomly generate. <br>
        Regular Expression Language - Quick Reference : [Link](https://docs.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference)
    * Example
        ```
        user_id:
            type: regex
            regex: USER\d\d\d\d
        ```
* list
    * Format
        ```
        [column_name]:
            type: list
            list:
            ratio:
        ```
        * `list`: The list to enter randomly.
        * `ratio`: (**Optional**) Random rate. Write it in an integer format in the same order as the list.
    * Example
        ```
        event:
            type: list
            list: ["event1", "event2", "event3"]
            ratio: [2,3,10]
        ```
* datetime
    * Format
        ```
        [column_name]:
            type: datetime
            start_dt:
            end_dt:
            output_format:
        ```
        * `start_dt`: Start date. Write in **YYYY-MM-DD HH:MM:SS** format.(e.g 2020-01-01 00:00:00)
        * `end_dt`: End date. Write in **YYYY-MM-DD HH:MM:SS** format.(e.g 2020-01-01 00:00:00)
        * `output_format`: (**Optional**) The output format. Write quotation marks together. Format can be found on [Link](https://www.w3schools.com/python/python_datetime.asp) <br>
        Default format : "%Y-%m-%d %H:%M:%S"
    * Example
        ```
        datetime:
            type: datetime
            start_dt: 2020-01-01 00:00:00
            end_dt: 2020-03-04 00:00:00
            output_format: "%Y-%m-%d %H:%M:%S"
        ```
