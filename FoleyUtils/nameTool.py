#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
#=============================================
import re, os, string
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def compileWindowsFileName(fullPath):
    '''
    build a not exists windows file name...
    Exp:  
        D:/text         -> D:/text(1)         -> D:/text(2)         -> D:/text(3) ... D:/text(n+1)
        E:/Document.txt -> E:/Document(1).txt -> E:/Document(2).txt -> E:/Document(3).txt ... E:/Document(n+1).txt
    '''
    if not os.path.isfile(fullPath) and not os.path.isdir(fullPath):
        return fullPath
    
    fname, fextension = os.path.splitext(fullPath)
    res = re.search('\(\d+\)$', fname)
    if res:
        index = string.zfill(int(res.group()[1:-1]) + 1, len(res.group()) - 2)
        fname  = re.sub('\(\d+\)$', '(%s)'%index, fname)
    else:
        fname      = '%s(1)'%fname
    fullName = fname + fextension
    
    return compileWindowsFileName(fullName)





def compileMayaObjectName(objectName):
    '''
    build a not exists maya object name...
    Exp: 
        pCube  -> pCube1  -> pCube2  -> pCube3  -> pCube4 ...  pCuben+1
        pSphere -> pSphere1 -> pSphere2 -> pSphere3 -> pSphere4 ... pSpheren+1
    '''
    if not mc.objExists(objectName):
        return objectName
    
    res = re.search('\d+$', objectName)
    if res:
        index = string.zfill(int(res.group()) + 1, len(res.group()))
        result   = re.sub('\d+$', index, objectName)    
    else:
        result   = '%s1'%(objectName)
    
    return compileMayaObjectName(result)





def SerializationObjectNames(objectList, nameFormat='Temp*', padding=3):
    '''
    objectList must is a list or a tuple
    nameFormat mutst have one " * "
    Exp:
            [pCulbe,  pCulbe1, pCulbe2, pCulbe3, pCulbe4] -> temp*
        ->  [temp000, temp001, temp002, temp003, temp004] 
    
            [pCulbe,  pCulbe1, pCulbe2, pCulbe3, pCulbe4] -> C_temp*_geo_0
        ->  [C_temp000_geo_0, C_temp001_geo_0, C_temp002_geo_0, C_temp003_geo_0, C_temp004_geo_0] 
    '''
    if not isinstance(objectList, (list, tuple)):
        return
    
    if nameFormat.count('*') != 1:
        return objectList
    
    newNameList = []
    for i, obj in enumerate(objectList):
        newName = compileMayaObjectName(nameFormat.replace('*', string.zfill(i, padding)))
        newNameList.append(newName)
    return newNameList