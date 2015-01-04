#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Sun, 04 Jan 2015 13:39:56
#========================================
import sys, os, functools
from FoleyUtils import scriptTool, uiTool
from PyQt4 import QtCore, QtGui
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
baseClass, windowClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'ProjectTool_UI.ui'))
class ProjectUI(baseClass, windowClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'ProjectWindow'):
            return
        
        super(ProjectUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-
        project_icon = QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'map_pin.png'))
        self.btn_getProject.setIcon(project_icon)
        
        window_icon = QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'windowIcon.png'))
        self.setWindowIcon(window_icon)
        #-
        self.tableModel = TableModel()
        self.tableView.setModel(self.tableModel)
        #-
        self.delegate = Delegate(self)
        self.tableView.setItemDelegateForColumn(1, self.delegate)
        #-
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setClickable(False)
        self.tableView.horizontalHeader().setMovable(False)
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        #-
        self.resizeEvent(QtGui.QResizeEvent(QtCore.QSize(), QtCore.QSize()))
        #-
        self.getProjectPath()


    def resizeEvent(self, event):
        self.tableView.setColumnWidth(0, self.tableView.width() * 0.75)
        self.tableView.setColumnWidth(1, self.tableView.width() * 0.24)


    def getProjectPath(self):
        #----------------------------
        self.project_name = mc.workspace(q=True, sn=True)
        self.project_path = mc.workspace(q=True, fn=True)
        #-
        self.btn_getProject.setText(self.project_name)
        #----------------------------   
        self.tableModel.clear()
        for d in os.listdir(self.project_path):
            self.tableModel.insertRow([d, ''])
            self.tableView.openPersistentEditor(self.tableModel.index(self.tableModel.rowCount() - 1, 1))
            self.tableView.setRowHeight(self.tableModel.rowCount() - 1, 25)


    def on_btn_getProject_clicked(self, args=None):
        if args == None:return
        self.getProjectPath()


    def openPath(self, index):
        asset = self.tableModel.data(self.tableModel.index(index.row(), 0), QtCore.Qt.DisplayRole)
        path = os.path.normpath(os.path.join(self.project_path, asset))
        if sys.platform == 'darwin':
            os.system('open %s'%path)
        else:        
            os.system('explorer.exe %s'%path)


class TableModel(QtCore.QAbstractTableModel):
    
    HEAD_DATA = 'Asset', 'Button'
    
    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self._data = []
    
    def columnCount(self, index):
        return 2
    
    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self._data)
    
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        
        if role == QtCore.Qt.FontRole:
            return QtGui.QFont('Tahoma', 10)


    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.HEAD_DATA[section]
    
    
    def insertRow(self, data, row=0, index=QtCore.QModelIndex()):
        row = self.rowCount()
        self.beginInsertRows(index, row, row)
        self._data.insert(row, data)
        self.endInsertRows()

    
    def removeRow(self, row, index=QtCore.QModelIndex()):
        self.beginRemoveRows(index, row, row)
        self._data.pop(row)
        self.endRemoveRows()


    def clear(self):
        for i in reversed(range(self.rowCount())):
            self.removeRow(i)



class Delegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        super(Delegate, self).__init__(parent)
        self.parent = parent
        #-
        self.folder_icon  = QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'folder.png'))
    
    def createEditor(self, parent, option, index):
        button = QtGui.QPushButton(parent)
        button.setIcon(self.folder_icon)
        button.clicked.connect(functools.partial(self.parent.openPath, index))
        return button