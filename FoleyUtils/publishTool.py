#=============================================
# author: changlong.zang                     
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
#=============================================
import string, os, re
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

VERSION_PADDING = 3

def conformFilePath(path, MSC='maya'):
    '''
       maya: E:/a\b/c\qq.ma -> E:/a/b/c/qq.ma 
    windows: E:/a\b/c\qq.ma -> E:\a\b\c\qq.ma 
    '''
    if MSC == 'maya':
        newPath = path.replace('\\', '/')
    else:
        newPath = path.replace('/', '\\')
    return newPath




def getVersionsFiles(path, fextension=''):
    '''
    get files dictionary..
    '''
    fileDict = {}
    if not os.path.isdir(path):
        return fileDict
    
    files = re.findall('([^\|]+((?<=v)\d+(?=\.%s))[^\|]+)'%fextension, string.join(os.listdir(path), '|'))
    for f, v in files:
        fileDict[v] = conformFilePath(os.path.join(path, f))
    
    return fileDict




def getVersions(path, fextension=''):
    '''
    get all of versions..
    '''
    versions = getVersionsFiles(path, fextension).keys()
    versions.sort()
    return versions





def getLastVersion(path, fextension=''):
    '''
    get the last version..
    '''
    versions = getVersions(path, fextension)
    versions.insert(0, 0)
    
    lastVersion = max([int(v) for v in versions])
    lastVersion = string.zfill(lastVersion, VERSION_PADDING)
    return lastVersion




def getNewVersion(path, fextension=''):
    '''
    get the new version..
    '''
    lastVersion = int(getLastVersion(path, fextension))
    newVersion = string.zfill(lastVersion+1, VERSION_PADDING)
    return newVersion




def getVersiondFile(path, version, fextension=''):
    '''
    get the last file fullpath by input version..
    '''
    fileDict = getVersionsFiles(path, fextension)
    filePath = fileDict.get(version, '')
    return filePath




def getLastFile(path, fextension=''):
    '''
    get the last file fullpath..
    '''
    lastVersion = getLastVersion(path, fextension)
    lastFile    = getVersiondFile(path, lastVersion, fextension)
    return lastFile




def getNewFile(path, fname_format='name_v*', fextension=''):
    '''
    build a new version file...
    '''
    filePath = ''
    lastFile = getLastFile(path, fextension)
    if not os.path.isfile(lastFile):
        filePath = conformFilePath(os.path.join(path, fname_format.replace('*', string.zfill(1, VERSION_PADDING))))
  
    else:
        lastVersion = getLastVersion(path, fextension)
        newVersion  = getNewVersion(path, fextension)

        fname, fextension = os.path.splitext(lastFile)
        filePath = re.sub('%s$'%lastVersion, newVersion, fname) + fextension
    
    return filePath




def getSize(path):
    '''
    return a file or a dir size by bytes...
    '''
    size = 0
    if os.path.isfile(path):
        size = os.path.getsize(path)
    
    elif os.path.isdir(path):
        for p, d, fs in os.walk(path):
            for f in fs:
                size += os.path.getsize(os.path.join(p, f))
    return size