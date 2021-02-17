from abc import *
import random

class COL(metaclass=ABCMeta):
    @abstractmethod
    def gen_data(self):
        pass

class COL_INT(COL):
    def __init__(self, info:dict):
        if "min" not in info:
            raise Exception('[Config Error] "min" is missing from json file')
        if "max" not in info:
            raise Exception('[Config Error] "max" is missing from json file')

        self.min = info["min"]
        self.max = info["max"]
        self.unit = info["unit"]
        if self.min > self.max:
            raise Exception('[Config Error] "max" is less than "min"')
        if self.unit > self.max:
            raise Exception('[Config Error] "unit" is less than "min"')

    def gen_data(self):
        super().gen_data()
        return random.randrange(self.min, self.max+1, self.unit)

class COL_LIST(COL):
    def __init__(self, info:dict):
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
