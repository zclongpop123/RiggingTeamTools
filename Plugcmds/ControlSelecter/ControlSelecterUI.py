#=================================
# author: changlong.zang
#   date: 2014-06-09
#=================================
import  os, sys, json, re
from PyQt4 import QtCore, QtGui
import maya.cmds as mc

if '//bjserver2/Temp Documents/Foley/Tools' not in sys.path:
    sys.path.append('//bjserver2/Temp Documents/Foley/Tools')
    
from FoleyUtils import scriptTool, uiTool, mayaTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

if scriptTool.getScriptPath() not in sys.path:
    sys.path.append(scriptTool.getScriptPath())

class ContextMenu(QtGui.QMenu):
    def __init__(self, Point, btn, parent=None):
        super(ContextMenu, self).__init__(parent)
        self.Button = btn
        
        action_addControl = self.addAction('Add Controls')
        self.addSeparator()
        action_removeControl = self.addAction('Remove Controls')

        action_addControl.triggered.connect(self.addControls)
        action_removeControl.triggered.connect(self.removeControls)

        self.move(Point)
        self.exec_()


    def addControls(self):
        #- get select controls
        selectControl = mc.ls(sl=True)
        selectControl = [x.split(':')[-1] for x in selectControl]
        
        #- read Data
        f = open(os.path.join(getScriptPath(), 'ControlNameData.json'), 'r')
        controlDT = json.load(f)
        f.close()
        
        #- set Data
        controlDT.setdefault(self.Button, []).extend(selectControl)
        
        #- save Data
        f = open(os.path.join(getScriptPath(), 'ControlNameData.json'), 'w')
        json.dump(controlDT, f, indent=4)
        f.close()     


    def removeControls(self):
        #- get select controls
        selectControl = mc.ls(sl=True)
        selectControl = [x.split(':')[-1] for x in selectControl]
        
        #- read Data
        f = open(os.path.join(getScriptPath(), 'ControlNameData.json'), 'r')
        controlDT = json.load(f)
        f.close()
        
        #- set Data
        for ctl in selectControl:
            if ctl in controlDT.get(self.Button, []):
                controlDT.get(self.Button, []).remove(ctl)
        
        #- save Data
        f = open(os.path.join(getScriptPath(), 'ControlNameData.json'), 'w')
        json.dump(controlDT, f, indent=4)
        f.close()  




windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'ControlSelecterUI.ui'))
class ControlSelecterWnd(windowClass, baseClass):
    selectAdd = False
    def __init__(self, parent=uiTool.getMayaWindow()):
        if uiTool.windowExists(parent, 'ControlSelecterWindow'):
            return        
        super(ControlSelecterWnd, self).__init__(parent)
        self.setupUi(self)
        self.show()
        
        #- connect Signal
        for btn in self.groupBox.findChildren(QtGui.QPushButton):
            btn.clicked.connect(self.SelectControl)

        for btn in self.groupBox_2.findChildren(QtGui.QPushButton):
            btn.clicked.connect(self.SelectControl)    
        
        #- refresh characters
        self.on_btn_loadCharacters_clicked(True)
        
        #- read control name Data
        f = open(os.path.join(scriptTool.getScriptPath(), 'ControlNameData.json'), 'r')
        self.CONTROL_NAME_DATA = json.load(f)
        f.close()


    #======================================================================================
    def keyPressEvent(self, Event):
        if Event.key() == QtCore.Qt.Key_Shift:
            self.selectAdd = True

    
    
    def keyReleaseEvent(self, Event):
        if Event.key() == QtCore.Qt.Key_Shift:
            self.selectAdd = False
    #======================================================================================


    def contextMenuEvent(self, Event):
        child = self.childAt(Event.pos())
        if not isinstance(child, QtGui.QPushButton):return
        ContextMenu(Event.globalPos(), str(child.objectName()))        



    def on_btn_loadCharacters_clicked(self, args=None):
        '''
        load characters
        '''
        if args==None:return
        #- clear character list
        self.cbx_CharacterList.clear()
        
        #- add characters
        for f in mc.file(q=True, r=True):
            if not re.search('\Wcharacter\W', f): continue
            self.cbx_CharacterList.addItem(mc.file(f, q=True, ns=True))
    
    
    
    #def on_cbx_CharacterList_currentIndexChanged(self, index):
        #if isinstance(index, int):return
        #all_sets = ' '.join(mc.ls(type='objectSet'))
        #nameSpace = str(self.cbx_CharacterList.currentText())
        #sets = re.search('%s\S+(Allctrls|body_Ctrls|facial_Ctrls)'%nameSpace, all_sets)
        #if sets:
            #self.SetsButtonBox.setEnabled(True)
        #else:
            #self.SetsButtonBox.setEnabled(False)

        
    def SelectControl(self):
        btn = self.sender() # get clicked button
        
        #- get last clicked
        if hasattr(self, 'CLECKED_BUTTON'):
            self.CLECKED_BUTTON.setChecked(False)
        
        #- set last clicked
        self.CLECKED_BUTTON = btn
        btn.setChecked(True)
        
        # current character
        nameSpace = str(self.cbx_CharacterList.currentText())  
        
        # add namespace to character
        controls = self.CONTROL_NAME_DATA.get(str(btn.objectName()), [])
        if nameSpace != '':
            controls = [':'.join([nameSpace, x]) for x in controls]

        # obj is exists
        controls = [ctr for ctr in controls if mc.objExists(ctr)] 
        # testing...
        RealControls = []
        for ctr in controls:
            try:
                mc.select(ctr)
            except ValueError:
                dagNodes = ' '.join(mc.ls(dag=True))
                for c in re.findall('\S+%s'%ctr, dagNodes):
                    if not mc.objExists(c):continue
                    if c in RealControls:continue
                    RealControls.append(c)
            else:
                RealControls.append(ctr)
        controls = RealControls[:]
        
        if len(controls) < 1:return
        
        # select control
        mc.select(controls, add=self.selectAdd)

    #=========================================================================

    def getMembers(self, setName):
        members = []
        all_sets = ' '.join(mc.ls(type='objectSet'))
        nameSpace = str(self.cbx_CharacterList.currentText())
        
        sets = re.search('%s\S+%s'%(nameSpace, setName), all_sets)
        if not sets:
            sets = re.search('%s'%setName, all_sets)
        if not sets:
            return members
        members = mayaTool.getSetsMembers(sets.group())
        return members


    @mayaTool.undo_decorator
    def on_btn_SelectAll_clicked(self, args=None):
        if args == None:return
        mc.select(self.getMembers('Allctrls')) #-  Binky:Allctrls
       
    
    @mayaTool.undo_decorator
    def on_btn_SelectBodyAll_clicked(self, args=None):
        if args == None:return
        mc.select(self.getMembers('body_Ctrls')) #-  Binky:body_Ctrls

    @mayaTool.undo_decorator
    def on_btn_SelectFaceAll_clicked(self, args=None):
        if args == None:return
        mc.select(self.getMembers('facial_Ctrls')) #-  Binky:facial_Ctrls

    
    @mayaTool.undo_decorator
    def on_btn_TposeAllNew_clicked(self, args=None):
        if args == None:return
        for control in self.getMembers('Allctrls'):
            if re.search('C_main[AB]_ctl_0$', control):
                continue
            Set(control)
    
    
    @mayaTool.undo_decorator
    def on_btn_TposeBodyNew_clicked(self, args=None):
        if args == None:return
        for control in self.getMembers('body_Ctrls'):
            if re.search('C_main[AB]_ctl_0$', control):
                continue
            Set(control)        
        
        
    @mayaTool.undo_decorator
    def on_btn_TposeFaceNew_clicked(self, args=None):
        if args == None:return
        for control in self.getMembers('facial_Ctrls'):
            if re.search('C_main[AB]_ctl_0$', control):
                continue
            Set(control)        
    #=========================================================================


    @mayaTool.undo_decorator
    def on_btn_TposeAll_clicked(self, args=None):
        if args == None:return
        backtoTpose()


    @mayaTool.undo_decorator
    def on_btn_TposeSelected_clicked(self, args=None):
        if args == None:return

        for control in mc.ls(sl=True):
            Set(control)


#=====================================================================================
CONTROL_TYPE = ('_ctl_', '_ctr_')
        
TRANS_ATTRIBUTES  = ('translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ')
SCACLE_AAARIBUTES = ('scaleX', 'scaleY', 'scaleZ', 'visibility')
TPOSE_DATA = {'Global': 0,
              'follow': 1,
              'chainStartEnveloppe':0,
              'StarCurveAttract': 0,
              #'Lenght3':1,
              #'Lenght2':1,
              #'Lenght1':1,
              'FKIKBlend':1,
              'minSquash':0.25}
#----------------------------------------------------------------------------------------------------------

def Set(control):
    attributes = mc.listAttr(control, k=True)
    if attributes == None:return 
    for attr in attributes:
        attributeFull = '%s.%s'%(control, attr)
        #- guess default attributes
        defaultValue = 0 
        if attr in TRANS_ATTRIBUTES:
            defaultValue = 0
        elif attr in SCACLE_AAARIBUTES:
            defaultValue = 1
        else:
            defV = mc.addAttr(attributeFull, q=True, dv=True)  or 0
            minV = mc.addAttr(attributeFull, q=True, min=True) or defV
            maxV = mc.addAttr(attributeFull, q=True, max=True) or defV
            

            defaultValue = min(max(minV, defV), maxV)
        
        #- set attribute
        if mc.getAttr(attributeFull, se=True):
            mc.setAttr(attributeFull, defaultValue)
        
            pattern = '(%s)$'%'|'.join(TPOSE_DATA.keys())
            res = re.search(pattern, attributeFull)
            if not res:continue
            mc.setAttr(attributeFull, TPOSE_DATA.get(res.group(), 0))
            

#----------------------------------------------------------------------------------------------------------
def backtoTpose():
    selectControl = mc.ls(sl=True)
    if len(selectControl) == 0:
        mc.warning('you must select a control (any one) from a character !!!')
        return

    #- list all of transforms 
    transforms = ' '.join(mc.ls(type='transform'))
    
    #- list all of the controls
    controls   = re.findall('(\S+(%s)\S+)'%'|'.join(CONTROL_TYPE), transforms)

    #- remove duplicates
    controls   = [x[0] for x in controls]
    
    #- do it
    for control in controls:
        if re.search('C_main[AB]_ctl_0$', control):
            continue
        
        if selectControl[0].rsplit(':', 1)[0] == control.rsplit(':', 1)[0]:
            Set(control)