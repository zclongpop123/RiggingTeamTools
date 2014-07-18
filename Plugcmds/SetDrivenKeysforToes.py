import os, json
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool


UIwndClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'SetDrivenKeysforToes.ui'))
class SetDrivenKeyforToes(UIwndClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'setDrivenKeyForToesWindow'):
            return
        super(SetDrivenKeyforToes, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-------------


    def setRange(self, Value, OldMin, OldMax, minV, maxV):
        OutValue = minV + (((Value-OldMin)/(OldMax-OldMin)) * (maxV-minV))
        return OutValue
    
    
    
    def on_actionSetkeys_triggered(self, clicked=None):
        if clicked==None:return
        if not os.path.exists('D:/toe.json'):return
        # open File
        f = open('D:/toe.json', 'r')
        ControlNameData = json.load(f)
        f.close()

        # get Axis
        Axis = 'ry'
        if self.axisXRDN.isChecked():
            Axis = 'rx'
        elif self.axisYRDN.isChecked():
            Axis = 'ry'
        else:
            Axis = 'rz'

        # get Value
        DvnMinValue = self.minFLD.value()
        DvnMaxValue = self.maxFLD.value()
            
        if self.reverseBOX.isChecked():
            Reverse = 1
        else:
            Reverse = -1
        #---
        
        print '-*-' * 20       
        print '\n'
        for Driver, Drivens in ControlNameData.iteritems():
            if not mc.objExists(Driver):continue
            DriverMinV = mc.addAttr('%s.spread'%Driver, q=True, min=True)
            DriverMaxV = mc.addAttr('%s.spread'%Driver, q=True, max=True)
            
            Drivens = [x for i, x in enumerate(Drivens) if x not in Drivens[:i]]
            Counts = len(Drivens)
            for i, Driven in enumerate(Drivens):
                #- Driven Open
                mc.setDrivenKeyframe('%s.%s'%(Driven, Axis), cd='%s.spread'%Driver, dv=0, v=0)
                DrivenrotateV = self.setRange(i * 1.0, 0, Counts-1, DvnMaxValue*-1, DvnMaxValue)
                mc.setDrivenKeyframe('%s.%s'%(Driven, Axis), cd='%s.spread'%Driver, dv=DriverMaxV, v=DrivenrotateV * Reverse)
                #- Driven Close
                DrivenrotateV = self.setRange(i * 1.0, 0, Counts-1, DvnMinValue, DvnMinValue * -1)
                mc.setDrivenKeyframe('%s.%s'%(Driven, Axis), cd='%s.spread'%Driver, dv=DriverMinV, v=DrivenrotateV * -1 * Reverse)
                
                #--- output ---
                print 'cmds.setDrivenKeyframe("%s.%s", cd="%s.spread", dv=0, v=0)'%(Driven, Axis, Driver)
                print 'cmds.setDrivenKeyframe("%s.%s", cd="%s.spread", dv=%f, v=%f)'%(Driven, Axis, Driver, DriverMaxV, DrivenrotateV * Reverse)
                print 'cmds.setDrivenKeyframe("%s.%s", cd="%s.spread", dv=%f, v=%f)'%(Driven, Axis, Driver, DriverMinV, DrivenrotateV * -1 * Reverse)
        
        print '\n'       
        print '-*-' * 20          
        
        if self.deleteFilesCBX.isChecked():
            os.remove('D:/toe.json')