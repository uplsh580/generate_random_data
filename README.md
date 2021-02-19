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
    datetime,user_id,count,event
    2020-01-01 10:08:28,USER4015,0,event1
    2020-01-01 17:59:15,USER5321,9000,event2
    2020-01-02 04:11:20,USER6996,3500,event3
    2020-01-02 05:35:06,USER1091,500,event3
    2020-01-02 10:01:16,USER6835,9500,event3
    2020-01-03 16:39:04,USER5979,3500,event2
    2020-01-03 22:16:21,USER2750,5500,event2
    2020-01-04 02:28:32,USER8625,7500,event1
    2020-01-04 07:20:42,USER9077,8500,event3
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
