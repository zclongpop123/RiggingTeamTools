#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Tue, 22 Jul 2014 17:41:44
#=============================================
import os, re
import maya.cmds as mc
from PyQt4 import QtCore, QtGui
from FoleyUtils import scriptTool, uiTool, publishTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
ASSET_PATH   = '//bjserver3/Tank/blinky_bill_movie/assets'
ASSET_FOLDER = ('character', 'prop', 'Setpiece')


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
                if not re.match(assetName, child):
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
        index = self.listView.selectedIndexes()[0].row()
        modelPath = self.asset_data[index]

        mc.file(modelPath, r=True, namespace='UV')

