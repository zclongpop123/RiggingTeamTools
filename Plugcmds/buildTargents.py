#=================================
# author: changlong.zang
#   date: 2014-05-05
#=================================
import os, re
import maya.cmds as mc
from FoleyUtils import uiTool, scriptTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

WindowClass, BaseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'buildTargents.ui'))
class BuildTargents(WindowClass, BaseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'buildTargentsWindow'):
            return         
        
        super(BuildTargents, self).__init__(parent)
        self.setupUi(self)
        self.show()


    def on_actionLoad_Object_triggered(self, args=None):
        if args==None:return
        selOBJ = mc.ls(sl=True)
        if selOBJ == []:return
        
        self.LET_Geometry.setText(selOBJ[0])
        
        blendShapes = mc.ls(mc.listHistory(selOBJ[0]), type='blendShape')
        if blendShapes == []:
            self.LET_BlendShape.setText('')
            return
        self.LET_BlendShape.setText(blendShapes[0])



    def on_actionClear_triggered(self, args=None):
        if args==None:return
        self.LET_Geometry.setText('')
        self.LET_BlendShape.setText('')



    def on_btn_builde_clicked(self, args=None):
        if args==None:return
        geometry   = str(self.LET_Geometry.text())
        blendShape = str(self.LET_BlendShape.text())
        if not mc.objExists(geometry):return
        if not mc.objExists(blendShape):return 
        
        #buildTargents(geometry, blendShape)
        targentList = mc.aliasAttr(blendShape, q=True)
        targentDict = {}
        for i in range(len(targentList)):
            if i % 2 != 0:continue
            targentDict[targentList[i]] = re.search('\d+', targentList[i+1]).group()
        
    
        #===========================================================
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(len(targentDict))
        self.progressLabel.setText('0 / %d'%len(targentDict))
        mc.setAttr('%s.en'%blendShape, 0)
        #===========================================================
        #- builde
        v = 0
        for name, index in targentDict.iteritems():
            targent = mc.duplicate(geometry, n=name)[0]
            buildTargent(blendShape, targent, index)
            
            targentShape = mc.listRelatives(targent, s=True, path=True)
            mc.connectAttr('%s.worldMesh[0]'%targentShape[0], '%s.it[0].itg[%s].iti[6000].igt'%(blendShape, index), f=True)
            
            #--------------------------------------------------------------
            v += 1
            self.progressBar.setValue(v)
            self.progressLabel.setText('%d / %d'%(v, len(targentDict)))
            self.progressName.setText(targent)
            #--------------------------------------------------------------

        #- move 
        targents = targentList[::2]
        targents.sort()
        W = mc.getAttr('%s.bbmx'%geometry)[0][0] - mc.getAttr('%s.bbmn'%geometry)[0][0]
        H = mc.getAttr('%s.bbmx'%geometry)[0][1] - mc.getAttr('%s.bbmn'%geometry)[0][1]
        for i, targent in enumerate(targents):
            for attr in ('tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'):
                mc.setAttr('%s.%s'%(targent, attr), l=False, k=True, cb=True)
        
            mc.move(W*(i % 15), H*(i // 15 + 1), 0, targent, r=True)
        
        #================================================
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1)
        self.progressLabel.setText('0 / 0')
        self.progressName.setText('{$targent}')
        mc.setAttr('%s.en'%blendShape, 1)
        #================================================
 


def buildTargent(blendShape, targentname, weightID):
    postions = mc.getAttr('%s.it[0].itg[%s].iti[6000].ipt'%(blendShape, weightID))
    if postions == None :return
    points = mc.ls(['%s.%s'%(targentname, pnt)  for pnt in mc.getAttr('%s.it[0].itg[%s].iti[6000].ict'%(blendShape, weightID))], fl=True)
    
    for pnt, posi in zip(points, postions):
        mc.move(posi[0], posi[1], posi[2], pnt, r=True)