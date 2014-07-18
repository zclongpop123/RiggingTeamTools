#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
#=============================================
import os, inspect
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def getModulesPath(moudle):
    '''
    return dir for imported moudle..
    '''
    moduleFile = inspect.getfile(moudle)
    modulePath = os.path.dirname(moduleFile)
    return modulePath




def getScriptPath():
    '''
    return dir path for used script..
    '''
    scriptPath = getModulesPath(inspect.currentframe().f_back)
    return scriptPath





def arrayRemoveDuplicates(Array):
    '''
    [1,1,2,2,3,3,4,5,5,6,6,6,6] -> [1,2,3,4,5,6]
    '''
    if not type(Array) is list:
        return Array
    return [x for i, x in enumerate(Array) if x not in Array[:i]]





def openMultiarray(Array):
    '''
    [1, [2, [3, 4], 5], 6] -> [1, 2, 3, 4, 5, 6]
    (1, (2, (3, 4), 5), 6) -> (1, 2, 3, 4, 5, 6)
    '''
    L = []
    for Item in Array:
        if isinstance(Item, (tuple, list)):
            for i in openMultiarray(Item):
                L.append(i)
        else:
            L.append(Item)
    return L