from copy import copy

"""
    Recursively converts Python objects to JSON objects
    JSON objects are required to send clean data over the internet
    Private methods (starting with '_') are not included in the conversion
"""

class DictSerializer:
    def getDict(self):
        objCopy = copy(self)
        objDict = vars(objCopy)

        for key in list(objDict.keys()):
            if key.startswith('_'):
                del objDict[key]

        for key, value in objDict.items():
            try:
                if isinstance(value, list):
                    listCopy = copy(value)
                    for index, listValue in enumerate(listCopy):
                        listCopy[index] = listValue.getDict()
                    objDict[key] = listCopy
                else:
                    objDict[key] = value.getDict()
            except AttributeError:
                pass
        return objDict