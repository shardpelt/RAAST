from copy import copy

"""
    This class contains methods which converts objects to dictionaries. 
    Conversion is needed to convert them to JSON and send them with our communication protocols.
"""

class ObjectToDictHelper:
    @staticmethod
    def route(route):
        d = vars(copy(route))
        del d["data"]

        for k, v in d.items():
            if k == "waypoints":
                d[k] = [vars(wp) for wp in v]
            elif k == "finish":
                x = vars(copy(v))
                for k2, v2 in x.items():
                    x[k2] = vars(v2)
                d[k] = x
            elif k == "boarders":
                d[k] = vars(v)

        return d

    @staticmethod
    def data(data):
        d = vars(copy(data))
        del d["angleHelper"]
        del d["image"]

        for k, v in d.items():
            try:
                d[k] = vars(v)
            except:
                pass

        return d

    @staticmethod
    def course(course):
        d = vars(copy(course))

        del d["data"]
        del d["angleHelper"]

        return d