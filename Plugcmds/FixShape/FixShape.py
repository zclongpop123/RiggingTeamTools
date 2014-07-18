#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 09 Jul 2014 10:49:27
#=============================================
import os, math, re
from FoleyUtils import scriptTool, uiTool, ioTool
from PyQt4 import QtCore, QtGui
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'FixShape.ui'))

class ListModel(QtCore.QAbstractListModel):
    def __init__(self, L=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__data = L[:]


    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.__data)


    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__data[index.row()]
    
    
    def refresh(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount())
        del self.__data[:]
        self.endRemoveRows()
        
        transforms = ' '.join(mc.ls(type='transform'))
        rotateInfoGrps = re.findall('\S+_RIF_G', transforms)
        
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self.__data = rotateInfoGrps[:]
        self.endInsertRows()



class FixShapeUI(windowClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'FixShapeUI'):return
        #-
        super(FixShapeUI, self).__init__(parent)
        self.setupUi(self)
        self.__model = ListModel()
        self.listView.setModel(self.__model)
        self.show()
    
    
    def on_btn_makeDriver_clicked(self, args=None):
        if args==None:return
        nameData = ioTool.readData(os.path.join(scriptTool.getScriptPath(), 'Data.json'))
        for n in nameData:
            if not mc.objExists(n):continue
            if mc.objExists('%s_RIF_G'%n.rsplit('_', 2)[0]):continue
            makeRotateInfoForOneJoint(n)
        self.on_btn_refresh_clicked(True)
        
   
    def on_listView_clicked(self, index):
        mc.select(self.__model.data(index, QtCore.Qt.DisplayRole))
    
    
    
    def on_btn_refresh_clicked(self, args=None):
        if args==None:return
        self.__model.refresh()
   
   
   
    def on_btn_inputBsattr_clicked(self, args=None):
        if args==None:return
        blendShape = mc.ls(sl=True, type='blendShape')
        if len(mc.ls(sl=True)) == 1:
            attrs = mc.channelBox('mainChannelBox', q=True, sma=True)
        else:
            attrs = mc.channelBox('mainChannelBox', q=True, sha=True)
        if not attrs:return
        self.lineEdit.setText('%s.%s'%(blendShape[0], attrs[0]))

        
    #--------------------------------------------------------------------
    def on_btn_SetTestKey_clicked(self, args=None):
        if args==None:return
        mc.playbackOptions(ast=0, aet=100, min=0, max=100)
        
        selControl = mc.ls(sl=True)
        if len(selControl) == 0:return
        
        Ui_Tuple = ((self.CBX_X, self.Spx_minX, self.Spx_maxX, 'rx'),
                    (self.CBX_Y, self.Spx_minY, self.Spx_maxY, 'ry'),
                    (self.CBX_Z, self.Spx_minZ, self.Spx_maxZ, 'rz'))
        for cbx, minbox, maxbox, attr in Ui_Tuple:
            if not cbx.isChecked():continue
            minV = minbox.value()
            maxV = maxbox.value()
            
            for ctl in selControl:
                mc.setKeyframe('%s.%s'%(ctl, attr), t=0,   v=minV)
                mc.setKeyframe('%s.%s'%(ctl, attr), t=50,  v=0)
                mc.setKeyframe('%s.%s'%(ctl, attr), t=100, v=maxV)
    
    
    def on_btn_delTestKey_clicked(self, args=None):
        if args==None:return
        selControl = mc.ls(sl=True, type='transform')
        for ctl in selControl:
            mc.delete(mc.keyframe(ctl, q=True, n=True))
        
        
    def on_DNFLD_editingFinished(self):
        self.DNSLD.setValue(self.DNFLD.value() * 1000.0)
        
        
    def on_DNSLD_valueChanged(self, value):
        self.DNFLD.setValue(value / 1000.0)
        try:
            mc.setAttr(str(self.lineEdit.text()), value/ 1000.0)
        except:
            pass
    #--------------------------------------------------------------------
    
    def on_btn_setDrivenkey_clicked(self, args=None):
        if args==None:return
        rdnDict = {'rdn_A':'ypxn',  # -X+Y
                   'rdn_B':'y',     # +Y
                   'rdn_C':'ypxp',  # +X+Y
                   
                   'rdn_D':'x',     # -X
                   'rdn_E':'x',     # +X
                   
                   'rdn_F':'ynxn',  # -X-Y
                   'rdn_G':'y',     # -Y
                   'rdn_H':'ynxp'   # +X-Y
                   }
        selectRdn = ''
        for child in self.rdn_Box.findChildren(QtGui.QRadioButton):
            if child.isChecked():
                selectRdn = str(child.objectName())
                break
            else:
                continue
        #-----------------------------------------------------------
        driverAttr  = '%s.%s'%(self.__model.data(self.listView.selectedIndexes()[0], QtCore.Qt.DisplayRole), rdnDict.get(selectRdn))
        drivenAttr  = str(self.lineEdit.text())
        driverValue = mc.getAttr(driverAttr)
        drivenValue = mc.getAttr(drivenAttr)
        
        mc.setDrivenKeyframe(drivenAttr, cd=driverAttr, dv=driverValue, v=drivenValue)
        print driverAttr, drivenAttr, driverValue, drivenValue

    def on_btn_EditData_clicked(self, args=None):
        if args==None:return
        filePath = os.path.join(scriptTool.getScriptPath(), 'Data.json')
        filePath = filePath.replace('/', '\\')
        os.system('explorer.exe %s'%filePath)



def makeRotateInfoForOneJoint(joint):
    #- create sets
    TempCircle = mc.circle(r=1, ch=False)
    TempLine = mc.curve(d=1, p=((-1, 1, 0), (-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)))
    
    BaseLoc = mc.spaceLocator(p=(0, 0, 0), name='%s_RIF_Baseloc'%joint.rsplit('_', 2)[0])[0]
    AimLoc = mc.spaceLocator(p=(0, 0, 0), name='%s_RIF_aimLoc'%joint.rsplit('_', 2)[0])[0]
    
    grp = mc.group(TempCircle, TempLine, BaseLoc, AimLoc, name='%s_RIF_G'%joint.rsplit('_', 2)[0])
    
    #- set Temp Curve Template
    for temp in (TempCircle, TempLine):
        shape = mc.listRelatives(temp, s=True, path=True)
        mc.setAttr('%s.ove'%shape[0], 1)
        mc.setAttr('%s.ovdt'%shape[0], 1)
    
    #- lock attributes
    for attr in mc.listAttr(BaseLoc, k=True):
        if attr in ('translateX', 'translateY'):
            continue
        mc.setAttr('%s.%s'%(BaseLoc, attr), l=True, k=False)
    
    #- limit Translate
    mc.transformLimits(BaseLoc, tx=(-1, 1), ty=(-1, 1), etx=(True, True), ety=(True, True))
    mc.pointConstraint(AimLoc, BaseLoc, skip='z')
    
    
    #- add Atributes
    for attr in ('x', 'y', 'ypxp', 'ypxn', 'ynxp', 'ynxn', 'up', 'down', 'left', 'right'):
        mc.addAttr(grp, sn=attr, k=True)
    
    #- comp connections
    #- 1
    mc.connectAttr('%s.tx'%BaseLoc, '%s.x'%grp)
    mc.connectAttr('%s.ty'%BaseLoc, '%s.y'%grp)      
    
    #- 2
    Values = ('ypxp', 0.707,0.707), ('ypxn', -0.707,0.707), ('ynxp', 0.707,-0.707), ('ynxn', -0.707,-0.707)
    for Attr, x, y in Values:
        node = mc.createNode('multDoubleLinear')
        mc.setDrivenKeyframe('%s.i1'%node, cd='%s.tx'%BaseLoc, dv=0, v=0, itt='linear', ott='linear')
        mc.setDrivenKeyframe('%s.i1'%node, cd='%s.tx'%BaseLoc, dv=x, v=1, itt='linear', ott='linear')
        mc.setDrivenKeyframe('%s.i2'%node, cd='%s.ty'%BaseLoc, dv=0, v=0, itt='linear', ott='linear')
        mc.setDrivenKeyframe('%s.i2'%node, cd='%s.ty'%BaseLoc, dv=y, v=1, itt='linear', ott='linear')        
        mc.connectAttr('%s.o'%node, '%s.%s'%(grp, Attr))
    
    #- 3
    # to line 71
    
    #- match Position
    mc.delete(mc.parentConstraint(joint, grp))
    JntChildren = mc.listRelatives(joint, c=True, path=True, type='joint')
    if JntChildren:
        mc.delete(mc.aimConstraint(JntChildren, grp, aim=(0,0,1), u=(0,1,0)))
        mc.delete(mc.pointConstraint(JntChildren, AimLoc))
    
    mc.parentConstraint(joint, AimLoc, mo=True)
    jointParent = mc.listRelatives(joint, p=True, path=True)[0]
    mc.parentConstraint(jointParent, grp, mo=True)
    
    
    #- match Scale
    startPosi = mc.xform(grp, q=True, ws=True, rp=True)
    endPosi = mc.xform(AimLoc , q=True, ws=True, rp=True)
    Dis = math.sqrt((startPosi[0] - endPosi[0]) ** 2 + (startPosi[1] - endPosi[1]) ** 2 + (startPosi[2] - endPosi[2]) ** 2)
    mc.setAttr(grp + '.sx', Dis)
    mc.setAttr(grp + '.sy', Dis)
    mc.setAttr(grp + '.sz', Dis)
    
    
    #- connect line 52
    Expstrings = '\
    $Ah = %s.ty;\n\
    $Aw = %s.tx;\n\
    $C = %s;\n\
    %s.%s = clamp(0, 180,  90 - acos($Ah / $C) * 180 / 3.14159265359);\n\
    %s.%s = clamp(-180, 0, 90 - acos($Ah / $C) * 180 / 3.14159265359);\n\
    %s.%s = clamp(0, 180,  90 - acos($Aw / $C) * 180 / 3.14159265359);\n\
    %s.%s = clamp(-180, 0, 90 - acos($Aw / $C) * 180 / 3.14159265359);\n\
    '%(BaseLoc, BaseLoc, mc.getAttr('%s.tz'%AimLoc),  grp, 'up', grp, 'down', grp, 'left', grp, 'right')
    mc.expression(s=Expstrings)
    #---------------------------------------------------------------------------------------

    return grp, AimLoc