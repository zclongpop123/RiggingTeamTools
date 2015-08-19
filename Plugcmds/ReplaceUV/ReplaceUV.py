#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Tue, 22 Jul 2014 17:41:44
#=============================================
import os, re, RemoveUVWasteNode
import maya.cmds as mc
from PyQt4 import QtCore, QtGui
from FoleyUtils import scriptTool, uiTool, publishTool, mathTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
ASSET_PATH   = 'D:/assets'
ASSET_FOLDER = ('character', 'prop', 'Setpiece', 'set')


class ListModel(QtCore.QAbstractListModel):
    def __init__(self, Listdata=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__modelData = Listdata[:]

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.__modelData)


    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__modelData[index.row()]


    def clear(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount())
        del self.__modelData[:]
        self.endRemoveRows()
    
    def change(self, L=[]):
        self.beginInsertRows(QtCore.QModelIndex(), 0, self.rowCount())
        self.__modelData = L[:]
        self.endInsertRows()
        
        


windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'replaceUV.ui'))
class ReplaceUV(windowClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'replaceUVwindow'):return
        
        super(ReplaceUV, self).__init__(parent)
        self.setupUi(self)
        #----------------
        self.__listModel = ListModel()
        self.listView.setModel(self.__listModel)
        #----------------        
        self.show()


    def on_btn_search_clicked(self, clicked=None):
        if clicked == None:return
        assetName = str(self.let_input.text())
        if assetName == '':
            return
        
        self.asset_data = []
        model_use_list = []
        for folder in ASSET_FOLDER:
            for child in os.listdir(os.path.join(ASSET_PATH, folder)):
                if not re.match(assetName, child, re.I):
                    continue
                
                tup = (folder, child, 'Model', 'publish', 'maya')
                f = publishTool.getLastFile(os.path.join(ASSET_PATH, *tup))
                
                if not os.path.isfile(f):
                    continue
                
                model_use_list.append('( %s ) - %s'%(folder, os.path.basename(f)))
                self.asset_data.append(f)
        
        self.__listModel.change(model_use_list)
     

    
    
    def on_btn_replace_clicked(self, clicked=None):
        if clicked == None:return
        

        polyGeometry = mc.ls(type='mesh')
        if not polyGeometry:
            print '# Error # No polyGon geometrys...',
            return
        polyGeometry = (mc.listRelatives(polyGeometry, p=True))
        polyGeometry = dict.fromkeys(polyGeometry).keys()
        
        
        selectIndexes = self.listView.selectedIndexes()
        if not selectIndexes:
            print '# Error # - You must select a model file...',
            return
        index = selectIndexes[0].row()
        modelPath = self.asset_data[index]

        

        if not uiTool.warning(message='Model\'s UV will be replaced, and it can not to undo !!!\nContinue ? ?'):
            return 
        
        #- refrence
        f = mc.file(modelPath, r=True, namespace='UV')
        
        self.progressBar.setMaximum(len(polyGeometry))
        for i, geo in enumerate(polyGeometry):
            self.progressBar.setValue(i)
            self.btn_replace.setText('%d%%'%mathTool.setRange(0, len(polyGeometry), 0, 100, i))
            
            realName = re.search('\w+$', geo).group()
            UVgeo    = 'UV:%s'%realName
            if not mc.objExists(UVgeo):
                print '# Warning # There are no model in new file for %s...'%geo
                continue
            #-
            mc.transferAttributes(UVgeo, geo, pos=0, nml=0, uvs=2, col=0, spa=5, sus="map1", tus="map1", sm=0, fuv=0, clb=1)
            #-
            print '# Result # Copyed UV %s -> %s'%(UVgeo, geo)

            #- delete history
            RemoveUVWasteNode.delUVTransferAttributesNode(geo)
        
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self.btn_replace.setText('Replace')
        #- remove refrence
        mc.file(f, rr=True)