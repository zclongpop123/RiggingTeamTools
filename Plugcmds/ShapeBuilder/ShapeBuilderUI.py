import os, re
from PyQt4 import QtCore, QtGui
import maya.cmds as mc
import maya.mel as mel
import rigBuilder.face.faceUI
import cvShapeInverterCmds
from FoleyUtils import uiTool, scriptTool, nameTool, mathTool, mayaTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def openCloseDeformer(model, value, ignal=()):
    for dfm in mayaTool.findDeformer(model):
        if mc.nodeType(dfm) in ignal:
            continue 
        
        if mc.getAttr('%s.en'%dfm, se=1):
            mc.setAttr('%s.en'%dfm, value)
        else:
            print '# - attribute "%s.en" is locked or connected can\'t modify...'%dfm,



class BlendShapeModel(QtCore.QAbstractListModel):
    openAttrLst = []
    def __init__(self, parent=None):
        super(BlendShapeModel, self).__init__(parent)
        self.__attributes = []


    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.__attributes)


    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__attributes[index.row()]
        if role == QtCore.Qt.ForegroundRole:
            if self.__attributes[index.row()] in self.openAttrLst:
                return QtGui.QColor(255, 170, 127)


    def insertRow(self, row, value, index=QtCore.QModelIndex()):
        self.beginInsertRows(index, row, row)
        self.__attributes.insert(row, value)
        self.endInsertRows()


    def clear(self):
        self.beginRemoveColumns(QtCore.QModelIndex(), 0, self.rowCount())
        del self.__attributes[:]
        self.endRemoveRows()



shapeBaseClass, shapeWindowClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'ShapeBuilderUI.ui'))
class ShapeBuilderUI(shapeBaseClass, shapeWindowClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'ShapeBuilderWindow'):
            return         

        super(ShapeBuilderUI, self).__init__(parent)
        self.setupUi(self)
        #---------------------------------------------------
        self.__AttributeModel = BlendShapeModel()
        self.listView_attributeList.setModel(self.__AttributeModel)
        #---------------------------------------------------
        self.widget_Bs.setEnabled(True)
        self.widget_BsBs.setEnabled(False)
        self.widget_SkinBs.setEnabled(False)
               
        self.show()
    
   #=====================================================================================================================================
    def on_listView_attributeList_pressed(self, index):
        self.lab_blendIndex.setText(str(index.row() + 1))
        self.lab_blendAttribute.setText(self.__AttributeModel.data(index, QtCore.Qt.DisplayRole))
        self.spx_attrValue.setValue(mc.getAttr('%s.%s'%(self.__blendShape, self.__AttributeModel.data(index, QtCore.Qt.DisplayRole))))
        self.on_spx_attrValue_editingFinished()
        
        
    def on_spx_attrValue_editingFinished(self):
        self.Slider_attrValue.setValue(self.spx_attrValue.value() * 1000)
    
    
    def on_Slider_attrValue_valueChanged(self, value):
        self.spx_attrValue.setValue(value / 1000.0)
        if not mc.objExists(self.__blendShape):
            return
        mc.setAttr('%s.%s'%(self.__blendShape, self.__AttributeModel.data(self.listView_attributeList.currentIndex(), QtCore.Qt.DisplayRole)), self.spx_attrValue.value())
        

    def on_progressBar_valueChanged(self, value):
        realV = int(mathTool.setRange(self.progressBar.minimum(), self.progressBar.maximum(), 0, 100, value))
        self.label_progress.setText('%d%%'%realV)
        
    
    def on_btn_showChannelBox_clicked(self, clicked=None):
        if clicked == None:return
        if not mc.objExists(str(self.btn_blendShape.text())):return
        rigBuilder.face.faceUI.createChannelBoxForNode(str(self.btn_blendShape.text()))    

    #=====================================================================================================================================
    
    def on_btn_blendShape_clicked(self, clicked=None):
        if clicked == None:return
        
        sel = mc.ls(sl=True)
        if len(sel) < 1:
            return
        
        if not mc.nodeType(sel[0]) == 'blendShape':
            return
        
        self.btn_blendShape.setText(sel[0])
        #--------------------------------
        self.__blendShape   = sel[0]
        self.__AttributeDT  = mayaTool.getBlendShapeInfo(sel[0])
        self.__AttributeDT2 = dict(zip(self.__AttributeDT.values(), self.__AttributeDT.keys()))
        self.__IGTAttributeDT = mayaTool.getBlendShapeInputGeomTarget(sel[0])
        mesh = mc.blendShape(str(self.btn_blendShape.text()), q=True, g=True)
        self.__baseModel = mc.listRelatives(mesh, p=True, path=True)[0]        
        #--------------------------------
        self.__AttributeModel.clear()

        for i, attr in enumerate(mayaTool.getBlendShapeAttributes(sel[0])):
            self.__AttributeModel.insertRow(i, attr)
  
  
    def on_btn_findItem_clicked(self, clicked=None):
        if clicked == None:return
        ID = 0
        openAttrLst = []
        for attr in self.__AttributeDT.itervalues():
            if round(mc.getAttr('%s.%s'%(self.__blendShape, attr))) != 1:
                continue
            ID = self.__AttributeDT2.get(attr, 0)
            openAttrLst.append(attr)
        
        self.__AttributeModel.openAttrLst = openAttrLst
            
        self.listView_attributeList.setCurrentIndex(self.__AttributeModel.index(ID, 0))
        
        self.on_listView_attributeList_pressed(self.listView_attributeList.currentIndex())



    def on_btn_duplicate_clicked(self, clicked=None):
        if clicked == None:return
        if not mc.objExists(self.__blendShape):return

        self.__sculpmodel = mc.duplicate(self.__baseModel, n=nameTool.compileMayaObjectName('%s_Sculp'%self.__baseModel.split(':')[-1]))[0]
        openCloseDeformer(self.__baseModel, 0)
        self.__tempmodel = mc.duplicate(self.__baseModel, n=nameTool.compileMayaObjectName('%s_Temp'%self.__baseModel.split(':')[-1]))[0]
        openCloseDeformer(self.__baseModel, 1)
        for attr in ('tx', 'ty', 'tz','rx', 'ry', 'rz','sx', 'sy', 'sz'):
            mc.setAttr('%s.%s'%(self.__sculpmodel, attr), l=False, k=True, cb=True)
            mc.setAttr('%s.%s'%(self.__tempmodel,  attr), l=False, k=True, cb=True)
            
        mc.move(mc.getAttr('%s.bbmx'%self.__baseModel)[0][0]  -  mc.getAttr('%s.bbmn'%self.__baseModel)[0][0], 0, 0, self.__sculpmodel, r=True)
        mc.move(mc.getAttr('%s.bbmx'%self.__sculpmodel)[0][0]  - mc.getAttr('%s.bbmn'%self.__baseModel)[0][0], 0, 0, self.__tempmodel,  r=True)

        #- add BlendShape
        tempBlend = mc.blendShape(self.__sculpmodel, self.__tempmodel)[0]
        tempBlendAttr = mc.aliasAttr(tempBlend, q=True)[0]
        
        #- set key
        mc.setKeyframe('%s.%s'%(tempBlend, tempBlendAttr), t=0,  v=0)
        mc.setKeyframe('%s.%s'%(tempBlend, tempBlendAttr), t=24, v=1)
        keyName = mc.keyframe('%s.%s'%(tempBlend, tempBlendAttr), q=True, n=True)
        mc.keyTangent(keyName, e=True, itt="spline", ott="spline")
    
    
    #def on_btn_addBlendShape_clicked(self, clicked=None):
        #if clicked == None:return
        #if len(self.listView_attributeList.selectedIndexes())==0:return 
        
        #mc.setAttr('%s.en'%self.__blendShape, 0)

        ##- run mel script to builde shape
        ##melPath = os.path.join(scriptTool.getScriptPath(), 'GenerateBlendShape.mel')
        ##melPath = melPath.replace('\\', '/')
        
        ##mc.select(self.__sculpmodel, self.__baseModel)
        ##f = open(melPath, 'r')
        ##melString = f.read()
        ##f.close()
        ##newSculpModel = mel.eval(melString)
        
        
        #openCloseDeformer(self.__baseModel, 0)
        #midShape = mc.duplicate(self.__baseModel, n=nameTool.compileMayaObjectName('Scup_invert_Mid'))[0]
        #mc.blendShape(self.__baseModel, midShape, w=(0,1))
        #openCloseDeformer(self.__baseModel, 1)
        

        #newSculpModel = cvShapeInverterCmds.invert(midShape, self.__sculpmodel, self.progressBar)
        #mc.delete(newSculpModel, ch=True)
        
        #mc.delete(self.__sculpmodel, midShape)
        #self.__sculpmodel = newSculpModel
        ##------------------------------------------------------
        #selectAttr = self.__AttributeModel.data(self.listView_attributeList.selectedIndexes()[0], QtCore.Qt.DisplayRole)
        
        #weightID = self.__AttributeDT2.get(selectAttr, None)
        #TGTattr  = self.__IGTAttributeDT.get(weightID, None)
        
        #original = mc.connectionInfo('%s.%s'%(self.__blendShape, TGTattr), sfd=True)
        #if len(original) == 0:
            #sculpShape = [x for x in mc.listRelatives(self.__sculpmodel, s=True, path=True) if mc.getAttr('%s.io'%x)==0][-1]
            #mc.connectAttr('%s.worldMesh[0]'%sculpShape, '%s.%s'%(self.__blendShape, TGTattr))
            #self.__sculpmodel = mc.rename(self.__sculpmodel, selectAttr)
        #else:
            #targentOBJ = original.split('.')[0]
            #mc.blendShape(self.__sculpmodel, targentOBJ, w=(0, 1))
            #mc.delete(targentOBJ, ch=True)
            #mc.delete(self.__sculpmodel)
        #mc.delete(self.__tempmodel)
        #mc.setAttr('%s.en'%self.__blendShape, 1)


    
    def on_btn_importBlendShapes_clicked(self, clicked=None):
        if clicked == None:return
        refrencefiles = mc.file(q=True, r=True)
        blendShapeFile = ''
        for f in refrencefiles:
            fileName = os.path.basename(f)
            if re.search('blendShapes_v\d+\.m[ab]$', fileName):
                blendShapeFile = f
                break
        if blendShapeFile == '':return
        nameSpace = mc.file(blendShapeFile, q=True, ns=True)
        mc.file(blendShapeFile, ir=True)
    
        mel.eval('source "C:/Program Files/Autodesk/Maya2013.5/scripts/others/namespaceEditCmd.mel"')
        mel.eval('namespaceEditorDeleteNamespaces {"%s"}'%nameSpace)
            
    
    
    
    def on_btn_exportBlendShapes_clicked(self, clicked=None):
        if clicked == None:return
        filePath = mc.fileDialog2(ff="Maya ASCII (*.ma);;Maya Binary (*.mb)")
        if not filePath:return
        mc.select('model_face_100_shape')
        mc.file(filePath, es=True, typ="mayaAscii")
    


    def on_btn_RepalceBlendShape_clicked(self, clicked=None):
        if clicked == None:return
        selModel = mc.ls(sl=True)
        if len(selModel) == 0:return
        shape = mc.listRelatives(selModel, s=True, path=True)[0]
        
        if len(self.listView_attributeList.selectedIndexes()) == 0:return
        selectAttr = self.__AttributeModel.data(self.listView_attributeList.selectedIndexes()[0], QtCore.Qt.DisplayRole)
        if not uiTool.warning('BlendShape\'s shape on attribute "%s" will be changed,\nand it can\'t to undo, \ncontinue? ?'%selectAttr):return
        
        weightID = self.__AttributeDT2.get(selectAttr, None)
        TGTattr  = self.__IGTAttributeDT.get(weightID, None)
        mc.connectAttr('%s.worldMesh[0]'%shape, '%s.%s'%(self.__blendShape, TGTattr), f=True)
    
    
    
    #@mayaTool.undo_decorator
    #def on_btn_fixBs_clicked(self, clicked=None):
        #if clicked == None:return
        #selModel = mc.ls(sl=True)
        #if len(selModel) == 0:return
        #shape = mc.listRelatives(selModel, s=True, path=True)[0]
        
        #if len(self.listView_attributeList.selectedIndexes()) == 0:return
        #selectAttr = self.__AttributeModel.data(self.listView_attributeList.selectedIndexes()[0], QtCore.Qt.DisplayRole)
        #if not uiTool.warning('BlendShape\'s shape on attribute "%s" will be changed,\nand it can\'t to undo, \ncontinue? ?'%selectAttr):return
        
        #weightID = self.__AttributeDT2.get(selectAttr, None)
        #TGTattr  = self.__IGTAttributeDT.get(weightID, None)
        #mc.connectAttr('%s.worldMesh[0]'%shape, '%s.%s'%(self.__blendShape, TGTattr), f=True)
    
    #==========================================================================================================================================
    
    
    def on_btn_FixBsStart_clicked(self, clicked=None):
        if clicked == None:return
        self.duplicateScupModel()
        self.dupliacteTempModel()
        
        
    def on_btn_FixBsEnd_clicked(self, clicked=None):
        if clicked == None:return

        #- 
        selectIndexes = self.listView_attributeList.selectedIndexes()
        if len(selectIndexes) == 0:return
        
        selectAttr = self.__AttributeModel.data(selectIndexes[0], QtCore.Qt.DisplayRole)
        #-
        if not uiTool.warning('BlendShape\'s shape on attribute "%s" will be changed,\nand it can\'t to undo, \ncontinue? ?'%selectAttr):return
        
        
        if mc.objExists(selectAttr):
            mc.blendShape(self.__sculpmodel, selectAttr, w=((0, 1)))
            mc.delete(selectAttr, ch=True)
            mc.delete(self.__sculpmodel)
            
        else:
            shape = mc.listRelatives(self.__sculpmodel, s=True, path=True)[0]
            
            weightID = self.__AttributeDT2.get(selectAttr, None)
            TGTattr  = self.__IGTAttributeDT.get(weightID, None)
            mc.connectAttr('%s.worldMesh[0]'%shape, '%s.%s'%(self.__blendShape, TGTattr), f=True)
            mc.rename(self.__sculpmodel, selectAttr)
        
        mc.delete(self.__tempmodel)


    def on_btn_FixBsBsStart_clicked(self, clicked=None):
        if clicked == None:return
        self.duplicateScupModel()
        self.dupliacteTempModel()
        
        
    def on_btn_FixBsBsEnd_clicked(self, clicked=None):
        if clicked == None:return
        
        #- 
        selectIndexes = self.listView_attributeList.selectedIndexes()
        if len(selectIndexes) == 0:return 
        selectAttr = self.__AttributeModel.data(selectIndexes[0], QtCore.Qt.DisplayRole)
        
        if not uiTool.warning('BlendShape\'s shape on attribute "%s" will be changed,\nand it can\'t to undo, \ncontinue? ?'%selectAttr):return
        
        #- dup model
        openCloseDeformer(self.__baseModel, 0)
        midModel = mc.duplicate(self.__baseModel, n=nameTool.compileMayaObjectName('%s_mid'%self.__baseModel.split(':')[-1]))[0]
        openCloseDeformer(self.__baseModel, 1)
        
        #- add blendShape
        mc.blendShape(self.__sculpmodel, self.__baseModel, midModel, w=((0, 1), (1, -1)))
        mc.delete(midModel, ch=True)
       

        if mc.objExists(selectAttr):
            mc.blendShape(midModel, selectAttr, w=((0, 1)))
            mc.delete(selectAttr, ch=True)
            mc.delete(midModel)
        else:
            shape = mc.listRelatives(midModel, s=True, path=True)[0]
            
            weightID = self.__AttributeDT2.get(selectAttr, None)
            TGTattr  = self.__IGTAttributeDT.get(weightID, None)
            mc.connectAttr('%s.worldMesh[0]'%shape, '%s.%s'%(self.__blendShape, TGTattr), f=True)                 
        
            mc.rename(midModel, selectAttr)
        mc.delete(self.__sculpmodel)
        mc.delete(self.__tempmodel)
        
    def on_btn_FixSkinBsStart_clicked(self, clicked=None):
        if clicked == None:return
        openCloseDeformer(self.__baseModel, 0, ('skinCluster'))
        self.duplicateScupModel()
        
        
        openCloseDeformer(self.__baseModel, 1, ('skinCluster'))
        bs = mc.blendShape(self.__baseModel, self.__sculpmodel)[0]
        attr = mc.aliasAttr(bs, q=True)[0]
        mc.setAttr(bs + '.' + attr, 1)
        mc.delete(self.__sculpmodel, ch=True)
        
        
        
        openCloseDeformer(self.__baseModel, 0, ('skinCluster'))
        self.dupliacteTempModel()
        


    def on_btn_FixSkinBsEnd_clicked(self, clicked=None):
        if clicked == None:return
        
        selectIndexes = self.listView_attributeList.selectedIndexes()
        if len(selectIndexes) == 0:return 
        selectAttr = self.__AttributeModel.data(selectIndexes[0], QtCore.Qt.DisplayRole)
        if not uiTool.warning('BlendShape\'s shape on attribute "%s" will be changed,\nand it can\'t to undo, \ncontinue? ?'%selectAttr):return
        
        openCloseDeformer(self.__baseModel, 0, ('skinCluster'))
        newSculpModel = cvShapeInverterCmds.invert(self.__baseModel, self.__sculpmodel, self.progressBar)
        mc.delete(newSculpModel, ch=True)        
        
            
        if mc.objExists(selectAttr):
            mc.blendShape(newSculpModel, selectAttr, w=((0, 1)))
            mc.delete(selectAttr, ch=True)
            mc.delete(newSculpModel)
        else:
            shape = mc.listRelatives(newSculpModel, s=True, path=True)[0]
            
            weightID = self.__AttributeDT2.get(selectAttr, None)
            TGTattr  = self.__IGTAttributeDT.get(weightID, None)
            mc.connectAttr('%s.worldMesh[0]'%shape, '%s.%s'%(self.__blendShape, TGTattr), f=True)                 
        
            mc.rename(newSculpModel, selectAttr)
        mc.delete(self.__sculpmodel)
        mc.delete(self.__tempmodel) 
    
    
    
    def duplicateScupModel(self):
        self.__sculpmodel = mc.duplicate(self.__baseModel, n=nameTool.compileMayaObjectName('%s_Sculp'%self.__baseModel.split(':')[-1]))[0]
        for attr in ('tx', 'ty', 'tz','rx', 'ry', 'rz','sx', 'sy', 'sz'):
            mc.setAttr('%s.%s'%(self.__sculpmodel, attr), l=False, k=True, cb=True)
        mc.move(mc.getAttr('%s.bbmx'%self.__baseModel)[0][0]  -  mc.getAttr('%s.bbmn'%self.__baseModel)[0][0], 0, 0, self.__sculpmodel, r=True)        
    
   
   
    def dupliacteTempModel(self):
        openCloseDeformer(self.__baseModel, 0)
        self.__tempmodel = mc.duplicate(self.__baseModel, n=nameTool.compileMayaObjectName('%s_Temp'%self.__baseModel.split(':')[-1]))[0]
        openCloseDeformer(self.__baseModel, 1)


        for attr in ('tx', 'ty', 'tz','rx', 'ry', 'rz','sx', 'sy', 'sz'):
            mc.setAttr('%s.%s'%(self.__tempmodel,  attr), l=False, k=True, cb=True)
            
        mc.move((mc.getAttr('%s.bbmx'%self.__baseModel)[0][0]  -  mc.getAttr('%s.bbmn'%self.__baseModel)[0][0])*2, 0, 0, self.__tempmodel,  r=True)

        #- add BlendShape
        tempBlend = mc.blendShape(self.__sculpmodel, self.__tempmodel)[0]
        tempBlendAttr = mc.aliasAttr(tempBlend, q=True)[0]
        
        #- set key
        startFrame = mc.playbackOptions(q=True, min=True)
        endFrame   = mc.playbackOptions(q=True, max=True)
        
        mc.setKeyframe('%s.%s'%(tempBlend, tempBlendAttr), t=startFrame,  v=0.0)
        mc.setKeyframe('%s.%s'%(tempBlend, tempBlendAttr), t=endFrame,    v=1.0)
        #- edit Key Type
        keyName = mc.keyframe('%s.%s'%(tempBlend, tempBlendAttr), q=True, n=True)
        mc.keyTangent(keyName, e=True, itt="spline", ott="spline")