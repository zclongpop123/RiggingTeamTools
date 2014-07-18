import os
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool, mayaTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


UIClass, BaseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'quickSetDrivenKey.ui'))

class QuickSetDrivenKey(UIClass, BaseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'quickSetDrivenKeywindow'):
            return        
        
        super(QuickSetDrivenKey, self).__init__(parent)
        self.setupUi(self)
        self.show()
    
       
    def _loadAttribute(self, LineEdit):
        SelectOBJ = mc.ls(sl=True)
        if len(SelectOBJ) == 0:return
        
        SelectAttriBute = mc.channelBox('mainChannelBox', q=True, sma=True)
        if SelectAttriBute == None:return
        
        LineEdit.setText('%s.%s'%(SelectOBJ[-1], SelectAttriBute[0]))
        
       
        
    def on_actionLoadDriverAttribute_triggered(self, args=None):
        if args==None:return
        self._loadAttribute(self.DriverAttributeLineEdit)
        


    def on_actionLoadDrivenAttribute_triggered(self, args=None):
        if args==None:return
        self._loadAttribute(self.DrivenAttributeLineEdit)



    def _setKeyFrame(self, DriverValueSpinbox, DrivenValueSpinbox):
        DriverAttibute = str(self.DriverAttributeLineEdit.text())
        DrivenAttibute = str(self.DrivenAttributeLineEdit.text())
        DriverValue = DriverValueSpinbox.value()
        DrivenValue = DrivenValueSpinbox.value()
        
        if len(DriverAttibute) == 0:return
        if len(DrivenAttibute) == 0:return
        
        mc.setDrivenKeyframe(DrivenAttibute, cd=DriverAttibute, dv=DriverValue, v=DrivenValue)
        
    
    @mayaTool.undo_decorator
    def on_actionKeyDriven1_triggered(self, args=None):
        if args==None:return
        self._setKeyFrame(self.DriverValueSpinbox1, self.DrivenValueSpinbox1)
        
    
    @mayaTool.undo_decorator
    def on_actionKeyDriven2_triggered(self, args=None):
        if args==None:return
        self._setKeyFrame(self.DriverValueSpinbox2, self.DrivenValueSpinbox2)
        
      
    @mayaTool.undo_decorator
    def on_actionKeyDriven3_triggered(self, args=None):
        if args==None:return
        self._setKeyFrame(self.DriverValueSpinbox3, self.DrivenValueSpinbox3)
        
      
    @mayaTool.undo_decorator
    def on_actionKeyDriven4_triggered(self, args=None):
        if args==None:return
        self._setKeyFrame(self.DriverValueSpinbox4, self.DrivenValueSpinbox4)
        
       
    @mayaTool.undo_decorator    
    def on_actionKeyDriven5_triggered(self, args=None):
        if args==None:return
        self._setKeyFrame(self.DriverValueSpinbox5, self.DrivenValueSpinbox5)
        
    
    @mayaTool.undo_decorator
    def on_actionKeyDrivenAll_triggered(self, args=None):
        if args==None:return
        self.on_actionKeyDriven1_triggered(True)
        self.on_actionKeyDriven2_triggered(True)
        self.on_actionKeyDriven3_triggered(True)
        self.on_actionKeyDriven4_triggered(True)
        self.on_actionKeyDriven5_triggered(True)