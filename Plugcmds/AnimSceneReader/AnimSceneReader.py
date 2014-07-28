#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Fri, 18 Jul 2014 11:24:35
#=============================================
import os, re, tempfile, shutil
import maya.cmds as mc
import maya.mel as mel
from PyQt4 import QtGui
from FoleyUtils import scriptTool, uiTool, publishTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

#===================================================================
ASSET_PATH = '//bjserver3/Tank/blinky_bill_movie/sequences'       #=
#===================================================================

def getNewVersionFile(path):
    lastVersion = publishTool.getLastVersion(path)
    newVersion  = publishTool.getNewVersion(path)
    
    lastFile = publishTool.getVersiondFile(path, lastVersion)
    if os.path.isfile(lastFile):
        newFile = re.sub('v%s\.'%lastVersion, 'v%s.'%newVersion, lastFile)
    else:
        newFile = tempfile.mktemp('.ma')
    return newFile

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'AnimSceneReader.ui')) 
class AnimSceneReaderUI(windowClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'AnimFileReader'):
            return                
        #--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        super(AnimSceneReaderUI, self).__init__(parent)
        self.setupUi(self)
        
        #-+
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(scriptTool.getScriptPath(), 'icons', 'map_pin.png')))
        self.btn_SelectPath.setIcon(icon)   
        
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(scriptTool.getScriptPath(), 'icons', 'fork.png')))
        self.btn_open.setIcon(icon)              
  
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(scriptTool.getScriptPath(), 'icons', 'cloud_upload.png')))
        self.btn_saveas.setIcon(icon)   
        

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(scriptTool.getScriptPath(), 'icons', 'blank_folder.png')))
        self.btn_OpenFolder.setIcon(icon)      
        

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(scriptTool.getScriptPath(), 'icons', 'light_on.png')))
        self.btn_light.setIcon(icon)
        
        #-+
        self.show()
        #--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    
    def __getValues(self):
        self.V_type      = str(self.LET_type.text())
        self.V_sc        = str(self.LET_scene.text())
        self.V_cam       = str(self.LET_camera.text())
        self.V_progress  = str(self.LET_progress.currentText())
        self.workpublish = str(self.LET_workpublish.currentText())
        self.V_file      = str(self.CBX_files.currentText())
        self.dir_path    = os.path.join(ASSET_PATH, self.V_type, '%s%s_%s'%(self.V_type, self.V_sc, self.V_cam), self.V_progress, self.workpublish, 'maya')
    
    def __openCloseLight(self, args):
        self.btn_light.setEnabled(args)
        

    def __refreshFiles(self):
        self.__getValues()
        
        self.CBX_files.clear()
        if not os.path.isdir(self.dir_path):
            self.__openCloseLight(False)
            return

        fileList = [x for x in os.listdir(self.dir_path) if re.search('\.m[ab]$', x)]
        self.CBX_files.addItems(fileList)
        self.CBX_files.setCurrentIndex(self.CBX_files.count()-1)
        self.__openCloseLight(True)
    
    
    def on_LET_type_editingFinished(self):
        self.__refreshFiles()
        
    def on_LET_scene_editingFinished(self):
        self.__refreshFiles()

    def on_LET_camera_editingFinished(self):
        self.__refreshFiles()
    
    def on_LET_progress_currentIndexChanged(self, index):
        if isinstance(index, int):return
        self.__refreshFiles()
    
    def on_LET_workpublish_currentIndexChanged(self, index):
        if isinstance(index, int):return
        self.__refreshFiles()    
    
    def on_btn_SelectPath_clicked(self, args=None):
        if args==None:return
        
        dirPath = mc.fileDialog2(fm=3, dir=ASSET_PATH, okc='Select')
        if not dirPath:return
        
        baseDirName = os.path.basename(dirPath[0])
        if not re.match('^[A-Za-z]+\d+_\d+$', baseDirName):return
        
        self.LET_type.setText(  re.match('^[A-Za-z]+', baseDirName).group())
        self.LET_scene.setText( re.search('\d+(?=_)',  baseDirName).group())
        self.LET_camera.setText(re.search('\d+$',      baseDirName).group())    
        


    def on_btn_open_clicked(self, args=None):
        if args==None:return
        self.__getValues()

        filePath = os.path.join(self.dir_path, self.V_file)
        if not os.path.isfile(filePath):return 
        
        if mel.eval('saveChanges("file -f -new;");') == 0:return
        mc.file(filePath, o=True, f=True)
    
    
    def on_btn_saveas_clicked(self, args=None):
        if args==None:return
        self.__getValues()

        newFilePath = getNewVersionFile(self.dir_path)
        tempPath = tempfile.mktemp('.ma')
                
        mc.file(rn=tempPath)
        mc.file(save=True)
        
        shutil.copy(tempPath, newFilePath)
        mc.file(rn=newFilePath)
        print '# file was saved to -> %s'%newFilePath
    
    
    def on_btn_OpenFolder_clicked(self, args=None):
        if args==None:return
        self.__getValues()
        
        path = self.dir_path
        if not os.path.isdir(path):
            return
        path = path.replace('/', '\\')
        os.system('explorer.exe %s'%path)