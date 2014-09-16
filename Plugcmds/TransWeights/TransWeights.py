#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Tue, 16 Sep 2014 15:31:44
#========================================
import os.path, tempfile
import maya.cmds as mc
from PyQt4 import QtGui
from FoleyUtils import scriptTool, uiTool, mayaTool
from rigBuilder import rigUtils
from rigBuilder.body import bodyIO
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def getSkinClusterByJoint(geometry, Joint):
    skincluster = mayaTool.findSkinCluster(geometry)
    influcences = mc.skinCluster(skincluster, q=True, inf=True)
    vtxCount    = mc.polyEvaluate(geometry, v=True)
    index = influcences.index(Joint)
    weights = []
    for i in range(vtxCount):
        weights.append(mc.skinPercent(skincluster, '%s.vtx[%d]'%(geometry, i), q=True, v=True)[index])
    return weights


def setSkinCluster(geometry, Joint, weights):
    skincluster = mayaTool.findSkinCluster(geometry)
    for i, w in enumerate(weights):
        mc.skinPercent(skincluster, '%s.vtx[%d]'%(geometry, i), tv=(Joint, w))


windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'TransWeights.ui')) 
class TransWeightsUI(windowClass, baseClass):
    def __init__(self, parent=uiTool.getMayaWindow()):
        if uiTool.windowExists(parent, 'TransWeightsUI'):
            return                
        #---------------------------------------------------------------------------------------------------
        super(TransWeightsUI, self).__init__(parent)
        self.setupUi(self)
        
        self.btn_LoadSkin.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'load.png')))
        self.btn_LoadJoint.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'load.png')))
        self.btn_Export.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'export.png')))
        self.btn_Import.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'import.png')))
        
        self.show()
        #---------------------------------------------------------------------------------------------------
        self.__data = []
        
    def on_btn_LoadSkin_clicked(self, args=None):
        if args == None:return
        self.lineEdit_Geometry.setText(mc.ls(sl=True, type='transform')[0])
        
        
    def on_btn_LoadJoint_clicked(self, args=None):
        if args == None:return
        self.lineEdit_Joint.setText(mc.ls(sl=True, type='joint')[0])
        
        
    def on_btn_Export_clicked(self, args=None):
        if args == None:return
        geometry = str(self.lineEdit_Geometry.text())
        Joint = str(self.lineEdit_Joint.text())
        #- 
        self.__data = getSkinClusterByJoint(geometry, Joint)
        #-
        self.lineEdit_Geometry.setStyleSheet('color: rgb(255, 255, 127);')
        self.lineEdit_Joint.setStyleSheet('color: rgb(255, 255, 127);')

 
    def on_btn_Import_clicked(self, args=None):
        if args == None:return

        geometry = str(self.lineEdit_Geometry.text())
        Joint = str(self.lineEdit_Joint.text())
        
        setSkinCluster(geometry, Joint, self.__data)
        self.__data = []
        
        self.lineEdit_Geometry.setStyleSheet('')
        self.lineEdit_Joint.setStyleSheet('')