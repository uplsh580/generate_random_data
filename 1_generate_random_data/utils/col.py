from abc import *
import random

class COL(metaclass=ABCMeta):
    @abstractmethod
    def gen_data(self):
        pass


class COL_INT(COL):
    def __init__(self, info:dict):
        if "min" not in info:
            raise Exception('"min" is missing from json file')
        if "max" not in info:
            raise Exception('"max" is missing from json file')

        self.min = info["min"]
        self.max = info["max"]
        if self.min > self.max:
            raise Exception('"max" is less than "min"')

        self.digits = 0

        if "digits" in info:
            self.digits = info["digits"]
        if self.digits != 0 and len(str(self.max)) > self.digits:
            raise Exception('digits of "max" are more than "digits"')

        self.prefix = ""        
        if "prefix" in info:
            self.prefix = info["prefix"]

        self.postfix = ""
        if "postfix" in info:
            self.postfix = info["postfix"]

    def gen_data(self):
        super().gen_data()
        ret = str(random.randint(self.min, self.max+1))

        if self.digits != 0:
            ret = "0" * (self.digits - len(ret)) + ret

        ret = self.prefix + ret
        ret += self.postfix
        return ret

class COL_LIST(COL):
    def __init__(self, info:dict):
        self.list = info["list"]
        self.ratio = [1] * len(self.list)

        if "ratio" in info:
            if len(self.list) != len(info["ratio"]):
                raise Exception('"ratio" length is different from "list" length.')
            self.ratio = info["ratio"]

        for i, entity in enumerate(self.ratio):
            if entity <= 1:
                continue
            self.list += [self.list[i]] * (entity-1)

        random.shuffle(self.list)
        self.len = len(self.list)

    def gen_data(self):
        super().gen_data()
        return str(random.choice(self.list))
