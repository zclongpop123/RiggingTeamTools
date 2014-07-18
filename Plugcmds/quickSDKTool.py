import os.path
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool


UIwndClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'quickSDKTool.ui'))
class quickSDK(UIwndClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'quickSDKwindow'):
            return        
        
        super(quickSDK, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-------------


    def on_actionLoadAttributes_triggered(self, clicked=None):
        if clicked==None:return
        
        
        mainChannelBox = 'mainChannelBox'  
        ChannelBoxs = mc.lsUI(typ='channelBox')
        ChannelBoxs.remove(mainChannelBox)
        if len(ChannelBoxs) == 0:return
        
        
        
        DriverOBJ = mc.channelBox(mainChannelBox, q=True, mol=True)
        DriverAttr = mc.channelBox(mainChannelBox, q=True, sma=True)
        
        
        if not DriverOBJ or not DriverAttr:return
        self.driverAttributelineEdit.setText('%s.%s'%(DriverOBJ[0], DriverAttr[0]))

        

        DrivenOBJ = mc.channelBox(ChannelBoxs[0], q=True, mol=True)
        DrivenAttr = mc.channelBox(ChannelBoxs[0], q=True, sma=True)
        DrivenAttrList = []
        for attribute in DrivenAttr:
            DrivenAttrList.append('%s.%s'%(DrivenOBJ[0], attribute))
        self.drivenAttributelineEdit.clear()
        self.drivenAttributelineEdit.addItems(DrivenAttrList)
        

   
    def on_actionQuickSDK_triggered(self, clicked=None):
        if clicked==None:return
        
        DriverAttribute = str(self.driverAttributelineEdit.text())

        
        for i in range(self.drivenAttributelineEdit.count()):
            Drivenattr = str(self.drivenAttributelineEdit.item(i).text())
            mc.setDrivenKeyframe(Drivenattr, cd=DriverAttribute)
            