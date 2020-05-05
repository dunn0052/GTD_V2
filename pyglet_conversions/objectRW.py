import dill

import os
import ntpath

def saveObject(obj, filename):
    if isPkl(filename):
        path, file = ntpath.split(filename)
        makePath(path)
        with open(filename, 'wb') as output:  # Overwrites any existing file.
            dill.dump(obj, output, dill.HIGHEST_PROTOCOL)
    else:
        print("file must end with .pkl")

def loadObject(filename):
    if isPkl(filename):
        try:
            with open(filename, 'rb') as obj:
                return dill.load(obj)
        except:
            print("Could not open", filename)
    else:
        print("file must end with .pkl")

def makePath(path):
    os.makedirs(path) if not os.path.exists(path) else True

def isPkl(path):
    return path.endswith('.pkl')
