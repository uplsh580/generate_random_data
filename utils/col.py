from abc import ABCMeta, abstractmethod
import random
import rstr


class COL(metaclass=ABCMeta):
    @abstractmethod
    def gen_data(self):
        pass


class COL_INT(COL):
    def __init__(self, info: dict):
        if "min" not in info:
            raise Exception('[Config Error] "min" is missing from config file.')
        if "max" not in info:
            raise Exception('[Config Error] "max" is missing from config file.')

        self.min = info["min"]
        self.max = info["max"]
        self.unit = info["unit"]
        if self.min > self.max:
            raise Exception('[Config Error] "max" is less than "min".')
        if self.unit > self.max:
            raise Exception('[Config Error] "unit" is less than "min".')

    def gen_data(self):
        super().gen_data()
        return random.randrange(self.min, self.max+1, self.unit)


class COL_LIST(COL):
    def __init__(self, info: dict):
        self.list = info["list"]
        self.ratio = [1] * len(self.list)

        if "ratio" in info:
            if len(self.list) != len(info["ratio"]):
                raise Exception('[Config Error] "ratio" length is different from "list" length.')
            self.ratio = info["ratio"]

        for i, entity in enumerate(self.ratio):
            if entity <= 1:
                continue
            self.list += [self.list[i]] * (entity-1)

        random.shuffle(self.list)
        self.len = len(self.list)

    def gen_data(self):
        super().gen_data()
        return random.choice(self.list)


class COL_REGEX(COL):
    def __init__(self, info: dict):
        self.regex = info["regex"]

    def gen_data(self):
        super().gen_data()
        return rstr.xeger(self.regex)


class COL_DATETIME(COL):
    def __init__(self, info: dict):
        if "start_dt" not in info:
            raise Exception('[Config Error] "start_dt" is missing from config file.')
        if "end_dt" not in info:
            raise Exception('[Config Error] "end_dt" is missing from config file.')

        self.start_dt = info['start_dt']
        self.end_dt = info["end_dt"]
        self.format = "%Y-%m-%d %H:%M:%S"
        if "format" in info:
            self.format = info["output_format"]

    def gen_data(self):
        super().gen_data()
        random_date = self.start_dt + (self.end_dt - self.start_dt) * random.random()
        return random_date.strftime(self.format)


class COL_DECIMAL(COL):
    def __init__(self, info: dict):
        if "min" not in info:
            raise Exception('[Config Error] "min" is missing from config file.')
        if "max" not in info:
            raise Exception('[Config Error] "max" is missing from config file.')

        self.min = info["min"]
        if self.min < -1 or self.min > 1:
            raise Exception(f'[Config Error] "min({self.min})" is not a range between -1 and 1.')

        self.max = info["max"]
        if self.max < -1 or self.max > 1:
            raise Exception(f'[Config Error] "max({self.max})" is not a range between -1 and 1.')

        if self.min > self.max:
            raise Exception(f'[Config Error] "max({self.max})" is less than "min({self.min})."')

        self.point_move = 1
        if "point_move" in info:
            self.point_move = info["point_move"]
        if self.point_move < -16 or self.point_move > 16:
            raise Exception(f'[Config Error] "point_move({self.point_move})" is not a range between -16 and 16.')
        
        self.decimal_len = 4
        if "decimal_len" in info:
            self.decimal_len = info["decimal_len"]
        if self.decimal_len < 0 or self.decimal_len > 16:
            raise Exception(f'[Config Error] "decimal_len({self.decimal_len})" is not a range between 0 and 16.')
        
    def gen_data(self):
        super().gen_data()
        return round(random.uniform(self.max, self.min) * pow(10, self.point_move), self.decimal_len)
