#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Thu, 03 Jul 2014 10:26:11
#=============================================

import sys, os, functools
from PyQt4 import QtCore, QtGui
from FoleyUtils import mathTool, uiTool
import maya.cmds as mc

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

class ControlColorUI(QtGui.QMainWindow):
    colorRGB = ((0.267, 0.267, 0.267),(0.000, 0.000, 0.000),(0.251, 0.251, 0.251),(0.500, 0.500, 0.500),(0.608, 0.000, 0.157),(0.000, 0.016, 0.376),
                (0.000, 0.000, 1.000),(0.000, 0.275, 0.098),(0.149, 0.000, 0.263),(0.784, 0.000, 0.784),(0.541, 0.282, 0.200),(0.247, 0.137, 0.122),
                (0.600, 0.149, 0.000),(1.000, 0.000, 0.000),(0.000, 1.000, 0.000),(0.000, 0.255, 0.600),(1.000, 1.000, 1.000),(1.000, 1.000, 0.000),
                (0.392, 0.863, 1.000),(0.263, 1.000, 0.639),(1.000, 0.690, 0.690),(0.894, 0.675, 0.475),(1.000, 1.000, 0.388),(0.000, 0.600, 0.329),
                (0.631, 0.412, 0.188),(0.624, 0.631, 0.188),(0.408, 0.631, 0.188),(0.188, 0.631, 0.365),(0.188, 0.631, 0.631),(0.188, 0.404, 0.631),
                (0.435, 0.188, 0.631),(0.631, 0.188, 0.412))    


    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'ControlColorUI'):return
            
        super(ControlColorUI, self).__init__(parent)
        self.resize(400, 50)
        
        self.setObjectName('ControlColorUI')
        self.setWindowTitle('Control Color')
        self.setMaximumSize(400, 50)
        self.setMinimumSize(400, 50)        
        
        self.__createButton()
        self.show()
    
    
    def __createButton(self):
        for i, rgb in enumerate(self.colorRGB):
            btn = QtGui.QPushButton(self)
            btn.resize(24, 24)
            #-
            x = i  % (len(self.colorRGB) / 2) * 25
            y = i // (len(self.colorRGB) / 2) * 25
            btn.move(x, y)
            
            #-
            r = mathTool.setRange(0.0, 1.0, 0, 255, rgb[0])
            g = mathTool.setRange(0.0, 1.0, 0, 255, rgb[1])
            b = mathTool.setRange(0.0, 1.0, 0, 255, rgb[2])
            btn.setStyleSheet('background-color: rgb(%f, %f, %f);'%(r, g, b))
            
            btn.clicked.connect(functools.partial(self.setColor, i))
            if i != 0:continue
            icon = QtGui.QIcon()
            icon.addFile(os.path.join(os.path.dirname(sys.exec_prefix), 'icons', 'fpe_brokenPaths.png'), QtCore.QSize(25, 25))
            btn.setIcon(icon)

    
    def setColor(self, colorIndex):
        selectOBJs = mc.ls(sl=True)
        for OBJ in selectOBJs:
            for shp in mc.listRelatives(OBJ, s=True, path=True) or []:
                if colorIndex == 0:
                    mc.setAttr(shp + '.ove', 0) 
                else:
                    mc.setAttr(shp + '.ove', 1)
                mc.setAttr(shp + '.ovc', colorIndex)