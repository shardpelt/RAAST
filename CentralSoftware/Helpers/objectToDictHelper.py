import sys
sys.path.append("..")

import copy as cp
import enum as en
import Communication.base_io as ba

"""
    Recursively converts Python objects to JSON objects
    JSON objects are required to send clean data over the internet
    Private methods (starting with '_') are not included in the conversion
"""

class DictSerializer:
    @staticmethod
    def getDict(objIn):
        objCopy = cp.copy(objIn)

        if isinstance(objCopy, (list, tuple)):
            for index, listValue in enumerate(objCopy):
                objCopy[index] = DictSerializer.getDict(listValue)
            return objCopy

        elif isinstance(objCopy, en.Enum):
            return objCopy.name

        elif isinstance(objCopy, ba.BaseIO):
            return type(objCopy).__name__

        else:
            try:
                objDict = vars(objCopy)

                for key in list(objDict.keys()):
                    if key.startswith('_'):
                        del objDict[key]

                for key, value in objDict.items():
                    objDict[key] = DictSerializer.getDict(value)

                return objDict

            except TypeError:
                return objIn