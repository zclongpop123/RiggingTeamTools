import os.path
from PyQt4 import QtGui
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


UIwndClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'mirrorSDK.ui'))
class MirrorSetDrivenKey(UIwndClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'mirrorSDKwindow'):
            return        
        
        super(MirrorSetDrivenKey, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-------------
        self.sourceAtrLst = []
        self.targentAtrLst = []

    
    def on_btn_deleteItem_clicked(self, args=None):
        if args==None:return
        
        for item in self.SourceAttributeList.selectedItems():
            for x in self.sourceAtrLst:
                if x[1] == item.text():
                    self.sourceAtrLst.remove(x)
                    break
        strings = self.SearchFLD.text()
        self.SearchFLD.setText('9999999')
        self.SearchFLD.setText(strings)


    def on_actionInputSearchReplace_triggered(self):
        SEARCH = self.SearchFLD.text()
        REPLACE = self.ReplaceFLD.text()
        OLDDRIVER = self.sourceControlFLD.text()
        NEWDRIVER = self.targentControlFLD.text()
        
        #
        self.SourceAttributeList.clear()
        sourceAttrs = [x[1] for x in self.sourceAtrLst]
        self.SourceAttributeList.addItems(sourceAttrs)
        #
        self.targentAtrLst = [[x[0].replace(OLDDRIVER, NEWDRIVER), x[1].replace(SEARCH, REPLACE), x[2], x[3]] for x in self.sourceAtrLst]
        #    
        #self.TargentAttributeList.clear()
        #SEARCH = self.SearchFLD.text()
        #REPLACE = self.ReplaceFLD.text()
        #targentAttrs = [x[1] for x in self.targentAtrLst]
        #self.TargentAttributeList.addItems(targentAttrs)
        targentAttrs = [x[1] for x in self.targentAtrLst]
        self.Model = QtGui.QStringListModel()
        self.Model.setStringList(targentAttrs)
        self.TargentAttributeList.setModel(self.Model)


    def on_actionLoadSourceControl_triggered(self, clicked=None):
        if clicked == None:return
        selectOBJ = mc.ls(sl=True)
        
        if len(selectOBJ) == 0:return
        self.sourceControlFLD.setText(selectOBJ[0])
        
        KeyableAttr = mc.listAttr(selectOBJ[0], k=True)
        
        del self.sourceAtrLst[:]
        del self.targentAtrLst[:]
        # loop  Attributes..
        for Attr in KeyableAttr:
            SDKeys = mc.connectionInfo('%s.%s'%(selectOBJ[0], Attr), dfs=True)
            # loop driven Attributes..
            for key in SDKeys:
                if mc.nodeType(key) == 'unitConversion':
                    keyNode = mc.connectionInfo('%s.output'%key.split('.')[0], dfs=True)[0].split('.')[0]
                
                elif mc.nodeType(key) not in ('animCurve','animCurveTA', 'animCurveTL', 'animCurveTT','animCurveTU','animCurveUA','animCurveUL','animCurveUT','animCurveUU'):
                    continue
                else:
                    keyNode = key.split('.')[0]
                DriverValues     =  mc.keyframe(keyNode, q=True, fc=True)
                DrivenValues     =  mc.keyframe(keyNode, q=True, vc=True)
                DriverAttribute =  mc.connectionInfo('%s.output'%keyNode, dfs=True)[0]
                
                # if more than one Drivers, from add  node get the attribute..
                if  DriverAttribute.endswith(']'):
                    DriverAttribute = mc.connectionInfo('%s.output'%(DriverAttribute.split('.')[0]), dfs=True)[0]
                 
                self.sourceAtrLst.append(['%s.%s'%(selectOBJ[0], Attr), DriverAttribute, DriverValues, DrivenValues])
        
        self.on_actionInputSearchReplace_triggered()

    
    def on_actionLoadTargentControl_triggered(self, clicked=None):
        if clicked == None:return
        selectOBJ = mc.ls(sl=True)
        
        if len(selectOBJ) == 0:return
        self.targentControlFLD.setText(selectOBJ[0])
        self.on_actionInputSearchReplace_triggered()
        
 
    
    def on_actionMirrorSDK_triggered(self, clicked=None):
        if clicked == None:return

        ReverDt = {'X':1, 'Y':1, 'Z':1}
        
        if self.REVERX.isChecked():ReverDt['X'] = -1
        if self.REVERY.isChecked():ReverDt['Y'] = -1
        if self.REVERZ.isChecked():ReverDt['Z'] = -1
        
        for i,DrivenInformations in enumerate(self.targentAtrLst):
            DrivenAttr = str(list(self.Model.stringList())[i])
            for driverValue, value in zip(DrivenInformations[2], DrivenInformations[3]):
                mc.setDrivenKeyframe(DrivenAttr, cd=DrivenInformations[0], dv=driverValue, v=value * ReverDt.get(DrivenInformations[0][-1], 1))
                print DrivenInformations[0], DrivenAttr



if __name__ == '__main__':MirrorSetDrivenKey(getMayaWnd())