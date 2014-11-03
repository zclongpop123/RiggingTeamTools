#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Tue, 28 Oct 2014 15:15:07
#========================================
import os.path, re
import maya.cmds as mc
import maya.mel as mel
from PyQt4 import QtCore, QtGui
from FoleyUtils import scriptTool, uiTool, mayaTool, ioTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

class ListModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(ListModel, self).__init__(parent)
        self.LIST_DATA = list()

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.LIST_DATA)


    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.LIST_DATA[index.row()]
    
    
    def changeData(self, inputData):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount())
        del self.LIST_DATA[:]
        self.endRemoveRows()
        
        self.beginInsertRows(QtCore.QModelIndex(), 0, self.rowCount())
        self.LIST_DATA = inputData
        self.endInsertRows()


windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'weightsTool.ui'))

class WeightsTool(windowClass, baseClass):
    SOURCE_DEFORM_TYPE = 'cluster'
    TARGET_DEFORM_TYPE = 'cluster'
    
    def __init__(self, parent=None):
        super(WeightsTool, self).__init__(parent)
        self.setupUi(self)
        self.show()
        
        self.SOURCE_MODEL = ListModel()
        self.TARGET_MODEL = ListModel()
        self.VIW_Source.setModel(self.SOURCE_MODEL)
        self.VIW_Target.setModel(self.TARGET_MODEL)
        
        self.LayoutComps = {'SOURCE_DEFORM_TYPE':(self.SOURCE_MODEL, self.LET_Source), 
                            'TARGET_DEFORM_TYPE':(self.TARGET_MODEL, self.LET_Target)}
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if not hasattr(self, 'LayoutComps'):
            return
        if not name in self.LayoutComps.keys():
            return
        self.LayoutComps[name][0].changeData(getDeformers(str(self.LayoutComps[name][1].text()), value))
  
  
    def on_LET_Source_textChanged(self, text):
        self.SOURCE_GEOMETRY = str(text)
    
    def on_LET_Target_textChanged(self, text):
        self.TARGET_GEOMETRY = str(text)    

    def on_btn_Copy_clicked(self, args=None):
        if args==None:return
        weights = getWeights(self.SOURCE_GEOMETRY, self.SOURCE_MODEL.data(self.VIW_Source.selectedIndexes()[0]))
        setWeights(self.TARGET_GEOMETRY, self.TARGET_MODEL.data(self.VIW_Target.selectedIndexes()[0]), weights)

    def on_btn_Mirror_clicked(self, args=None):
        if args==None:return

    def on_btn_Export_clicked(self, args=None):
        if args==None:return
        exportWeights(self.SOURCE_GEOMETRY, self.SOURCE_DEFORM_TYPE, self.SOURCE_MODEL.LIST_DATA)

    def on_btn_Import_clicked(self, args=None):
        if args==None:return
        importWeights()
  
    def on_actionLoadSource_triggered(self, args=None):
        if args==None:return
        self.LET_Source.setText(getSelected())

    def on_actionLoadTargent_triggered(self, args=None):
        if args==None:return
        self.LET_Target.setText(getSelected())
    
    def on_actionSourceSwitchToCluster_triggered(self, args=None):
        if args==None:return
        self.SOURCE_DEFORM_TYPE = 'cluster'

    def on_actionSourceSwitchToBlendShape_triggered(self, args=None):
        if args==None:return
        self.SOURCE_DEFORM_TYPE = 'blendShape'
    
    def on_actionSourceSwitchToSkinCluster_triggered(self, args=None):
        if args==None:return
        self.SOURCE_DEFORM_TYPE = 'skinCluster'        

    def on_actionTargetSwitchToCluster_triggered(self, args=None):
        if args==None:return
        self.TARGET_DEFORM_TYPE = 'cluster'

    def on_actionTargetSwitchBlendShape_triggered(self, args=None):
        if args==None:return
        self.TARGET_DEFORM_TYPE = 'blendShape'

    def on_actionTargetSwitchSkinCluster_triggered(self, args=None):
        if args==None:return
        self.TARGET_DEFORM_TYPE = 'skinCluster'



def getSelected():
    sel = mc.ls(sl=True)
    if not sel:
        return ''
    if not mc.listRelatives(sel[0], s=True, typ=('mesh', 'nurbsSurface', 'nurbsCurve')):
        return ''
    return sel[0]



def getDeformers(geometry, deformerType):
    if not mc.objExists(geometry):
        return []
    deformers = mayaTool.findDeformer(geometry)
    deformers = [dfm for dfm in deformers if mc.nodeType(dfm) == deformerType]
    
    if len(deformers) == 0:
        return []
    
    if deformerType == 'cluster':
        return deformers
    
    elif deformerType == 'blendShape':
        attributes = []
        for bsp in deformers:
            attributes.append('%s.envelope'%bsp)
            for attr in mayaTool.getBlendShapeAttributes(bsp):
                attributes.append('%s.%s'%(bsp, attr))
        return attributes
    
    elif deformerType == 'skinCluster':
        return mc.skinCluster(deformers[0], q=True, inf=True)
    
    else:
        return []


def getGeometryPointsCount(geometry):
    shapes = mc.listRelatives(geometry, s=True, path=True)
    if not shapes:
        return 0
    
    if mc.nodeType(shapes[0]) == 'mesh':
        return len(mc.ls('%s.vtx[:]'%geometry, fl=True))
    
    elif mc.nodeType(shapes[0]) in ('nurbsSurface', 'nurbsCurve'):
        return len(mc.ls('%s.cv[:]'%geometry, fl=True))
    
    else:
        return 0



def getWeights(geometry, args):
    weights = list()
    if not mc.objExists(geometry):
        return weights
    if not mc.objExists(args):
        return weights
    
    if mc.nodeType(args) == 'cluster':
        weights = getClusterWeights(geometry, args)
    
    elif mc.nodeType(args) == 'blendShape':
        weights = getBlendShapeWeights(geometry, args)
    
    elif mc.nodeType(args) == 'joint':
        weights = getSkinClusterWeights(geometry, args)
    
    else:
        pass
    
    return weights



def getClusterWeights(geometry, args):
    weightListIndex = mc.listRelatives(mc.cluster(args, q=True, g=True), p=True, path=True).index(geometry)
    vtxCounts = getGeometryPointsCount(geometry)
    weights = mc.getAttr('%s.wl[%d].w[:%d]'%(args, weightListIndex, vtxCounts-1))
    return weights




def getBlendShapeWeights(geometry, args):
    vtxCounts = getGeometryPointsCount(geometry)
    bsp, attr = args.split('.')
    
    if re.search('\.envelope$', args):
        weights = mc.getAttr('%s.it[0].bw[:%d]'%(bsp, vtxCounts-1))
    
    else:
        attrIndex = mayaTool.getBlendShapeAttributes(bsp).index(attr)
        weights = mc.getAttr('%s.it[0].itg[%d].tw[:%d]'%(bsp, attrIndex, vtxCounts-1))

    return weights



def getSkinClusterWeights(geometry, args):
    vtxCounts  = getGeometryPointsCount(geometry)
    skinNode   = mel.eval('findRelatedSkinCluster("%s")'%geometry)
    jointIndex = mc.skinCluster(skinNode, q=True, inf=True).index(args)
    weights = mc.getAttr('%s.wl[0:%d].w[%d]'%(skinNode, vtxCounts-1, jointIndex))
    return weights



def setWeights(geometry, args, weights):
    if not mc.objExists(geometry):
        return
    if not mc.objExists(args):
        return
    
    if mc.nodeType(args) == 'cluster':
        setClusterWeights(geometry, args, weights)
    
    elif mc.nodeType(args) == 'blendShape':
        setBlendShapeWeights(geometry, args, weights)
    
    elif mc.nodeType(args) == 'joint':
        setSkinClusterWeights(geometry, args, weights)
    
    else:
        pass
    


def setClusterWeights(geometry, args, weights):
    weightListIndex = mc.listRelatives(mc.cluster(args, q=True, g=True), p=True, path=True).index(geometry)
    vtxCounts = len(weights)
    weights = mc.setAttr('%s.wl[%d].w[:%d]'%(args, weightListIndex, vtxCounts-1), *weights)




def setBlendShapeWeights(geometry, args, weights):
    vtxCounts = len(weights)
    bsp, attr = args.split('.')

    if re.search('\.envelope$', args):
        weights = mc.setAttr('%s.it[0].bw[:%d]'%(bsp, vtxCounts-1), *weights)
    else:
        attrIndex = mayaTool.getBlendShapeAttributes(bsp).index(attr)
        mc.setAttr('%s.it[0].itg[%d].tw[:%d]'%(bsp, attrIndex, vtxCounts-1), *weights)




def setSkinClusterWeights(geometry, args, weights):
    vtxCounts  = len(weights)
    skinNode   = mel.eval('findRelatedSkinCluster("%s")'%geometry)
    jointIndex = mc.skinCluster(skinNode, q=True, inf=True).index(args)
    mc.setAttr('%s.wl[0:%d].w[%d]'%(skinNode, vtxCounts-1, jointIndex), *weights)



def exportWeights(geometry, deformerType, args):
    path = mc.fileDialog2(ff='JSON Files (*.json)', fm=0)
    if not path:
        return
    path = path[0]
    
    weights = {'geometry':geometry, 'type':deformerType, 'deformers':args}
    for arg in args:
        weights.setdefault('weights', list()).append(getWeights(geometry, arg))
    ioTool.writeData(path, weights)


def importWeights():
    path = mc.fileDialog2(ff='JSON Files (*.json)', fm=1)
    if not path:
        return
    path = path[0]
    
    data = ioTool.readData(path)
    for deformer, weights in zip(data['deformers'], data['weights']):
        setWeights(data['geometry'], deformer, weights)