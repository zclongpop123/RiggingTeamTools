import os.path, re
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool, mayaTool


windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'mirrorCtlShp.ui'))
class MirrorControlShp(windowClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'mirrorControlShapeUI'):return 
        super(MirrorControlShp, self).__init__(parent)
        self.setupUi(self)
        self.show()


    def on_btn_mirror_clicked(self, click=None):
        if click == None:return
        controlType = str(self.fld_controlType.text())
        
        flipAxis = 'X'
        if self.rdn_filpX.isChecked():
            flipAxis = 'X'
        elif self.rdn_filpY.isChecked():
            flipAxis = 'Y'
        else:
            flipAxis = 'Z'


        if self.rdn_lefttoright.isChecked():
            mirrorControlShape(controlType, 'L', 'R', flipAxis)
        else:
            mirrorControlShape(controlType, 'R', 'L', flipAxis)




@mayaTool.undo_decorator
def mirrorControlShape(typ, source, targent, flipAxis):
    if len(typ) == 0:return
    if source not in 'LR':return
    if source == targent:return
    
    #- get source side controls
    all_controls     = ' '.join(mc.listRelatives(mc.ls(type='nurbsCurve'), p=True, path=True))
    matched_controls = re.findall('\S*%s_\w+_%s_\d+'%(source, typ), all_controls)
    
    for ctl in matched_controls:
        #- get targent control
        targentControl = re.sub('%s_'%source, '%s_'%targent, ctl)
        if not mc.objExists(targentControl):continue
        
        #- duplicate shape
        tempx = mc.duplicate(ctl, po=True)
        mc.parent(mc.listRelatives(ctl, s=True, path=True), tempx, s=True, add=True)
        
        #- make Temp
        Temp = mc.duplicate(tempx)[0]
        for a in 'trs':
            for b in 'xyz':
                attr = a + b
                mc.setAttr('%s.%s'%(Temp, attr), l=False, k=True, cb=False)  

        #- close max min value controler
        mc.transformLimits(Temp, etx=(0, 0),ety=(0, 0),etz=(0, 0),erx=(0, 0),ery=(0, 0),erz=(0, 0))
        Temp = mc.parent(Temp, w=True)
        
        #- filp
        grp = mc.createNode('transform')
        
        sourcePosi = mc.xform(ctl, q=True, ws=True, rp=True)
        targenPosi = mc.xform(targentControl, q=True, ws=True, rp=True)
        
        midPoint = [(sourcePosi[0] + targenPosi[0]) / 2,
                    (sourcePosi[0] + targenPosi[0]) / 2,
                    (sourcePosi[0] + targenPosi[0]) / 2]
        mc.move(midPoint[0], midPoint[1], midPoint[2], grp, a=True)


        Temp = mc.parent(Temp, grp)
        mc.setAttr('%s.s%s'%(grp, flipAxis.lower()), -1)
        
        #- freeze transformations
        Temp = mc.parent(Temp, targentControl)
        mc.makeIdentity(Temp, apply=True, t=True, r=True, s=True)
        
        #- get original shapes
        originalShapes = mc.listRelatives(targentControl, s=True, path=True)
        
        #- parent new shapes
        shapes = mc.listRelatives(Temp, s=True, path=True)
        for shp in shapes:
            mc.setAttr('%s.ovc'%shp, mc.getAttr('%s.ovc'%originalShapes[0]))
        mc.parent(shapes, targentControl, s=True, r=True)
        for shp in shapes:
            mc.rename(shp, '%sShape'%targentControl)
                  
        #- delete temp
        mc.delete(tempx, Temp, grp, originalShapes)
        
