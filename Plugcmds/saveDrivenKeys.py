from PyQt4 import QtCore, QtGui
import maya.cmds as mc
import rigBuilder.face.faceIO
from FoleyUtils import uiTool

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

class SaveDrivenKeyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'saveDrivenkeysWindow'):
            return 
        super(SaveDrivenKeyWindow, self).__init__(parent)
        self.setupUi()
        self.setObjectName('saveDrivenkeysWindow')
        #------------------------------------------------
        self.loadButton.clicked.connect(self.loadKeys)
        self.saveButton.clicked.connect(self.saveKeys)
        #------------------------------------------------


    def setupUi(self):
        self.setObjectName('SaveDrivenKeyWindow')
        self.setWindowTitle('Save DrivenKey')
        self.resize(240, 43)
        self.setMinimumSize(QtCore.QSize(240, 43))
        self.setMaximumSize(QtCore.QSize(240, 43))
        
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName('centralwidget')
       
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName('horizontalLayout')
       
        self.loadButton = QtGui.QPushButton('Load', self.centralwidget)
        self.loadButton.setMinimumSize(QtCore.QSize(0, 26))
        self.loadButton.setMaximumSize(QtCore.QSize(16777215, 26))
        self.loadButton.setObjectName('loadButton')
        self.horizontalLayout.addWidget(self.loadButton)
        
        self.saveButton = QtGui.QPushButton('Save', self.centralwidget)
        self.saveButton.setMinimumSize(QtCore.QSize(0, 26))
        self.saveButton.setMaximumSize(QtCore.QSize(16777215, 26))
        self.saveButton.setObjectName('saveButton')
        self.horizontalLayout.addWidget(self.saveButton)
        self.setCentralWidget(self.centralwidget)
        self.show()


    def loadKeys(self, args=None):
        filePath = mc.fileDialog2(fm=1, ff='JSON Files(*.json)')
        if not filePath:return
        rigBuilder.face.faceIO.importSceneDrivenKeyData(filePath[0], verbose=True)   
        
    def saveKeys(self, args=None):
        filePath = mc.fileDialog2(fm=0, ff='JSON Files(*.json)')
        if not filePath:return
        rigBuilder.face.faceIO.exportSceneDrivenKeyData(filePath[0], verbose=True)