import json

class Metric:
    def __init__(self, asc, dt, name, units):
        self.asc = asc
        self.datatype = dt
        self.name = name
        self.units = units

class Source:
    def __init__(self, name):
        self.name = name
        self.metrics = []

class Group:
    def __init__(self, class_, name):
        self.classification = class_
        self.name = name
        self.sources = []

aa = Group(1, 2, 3)

print(aa.a, aa.b, aa.c)