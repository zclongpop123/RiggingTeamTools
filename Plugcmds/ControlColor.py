#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 03 Dec 2014 18:25:09
#========================================
import FoleyUtils.uiTool, PyQt4.QtGui, functools, maya.cmds
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
BUTTON_COLOR_RGB_VALUE = ((68,68,68),(0,0,0),(64,64,64),(128,128,128),(155,0,40),(0,4,96),(0,0,255),(0,70,25),(38,0,67),(200,0,200),
                          (138,72,51),(63,35,31),(153,38,0),(255,0,0),(0,255,0),(0,65,153),(255,255,255),(255,255,0),(100,220,255),
                          (67,255,163),(255,176,176),(228,172,121),(255,255,99),(0,153,84),(161,105,48),(159,161,48),(104,161,48),
                          (48,161,93),(48,161,161),(48,103,161),(111,48,161),(161,48,105))   

class ColorWindow(PyQt4.QtGui.QMainWindow):
    windowName = 'DragonDreamsControlColorToolWindow'
    
    def __init__(self, parent=None):
        if FoleyUtils.uiTool.windowExists(parent, self.windowName):
            return
        
        #- setup window
        super(ColorWindow, self).__init__(parent)
        self.setObjectName(self.windowName)
        self.setWindowTitle('Control Color Tool')
        self.setMaximumSize (482, 62)
        self.setMinimumSize (482, 62)
        
        #- add buttons
        for i in range(32):
            btn = PyQt4.QtGui.QPushButton(self)
            px = i % 16  * 30 + 1
            py = i // 16 * 30 + 1
            sx = 30
            sy = 30
            btn.setGeometry(px, py, sx, sy)
            
            btn.clicked.connect(functools.partial(self.setColor, i))
            btn.setStyleSheet('background-color: rgb(%d, %d, %d);'%BUTTON_COLOR_RGB_VALUE[i])
            
        self.show()

    
    def setColor(self, colorIndex):
        selectObjects = maya.cmds.ls(sl=True)
        if len(selectObjects) == 0:
            return
            
        for shp in maya.cmds.listRelatives(selectObjects, s=True, path=True) or []:
            if colorIndex == 0:
                maya.cmds.setAttr(shp + '.ove', 0) 
            else:
                maya.cmds.setAttr(shp + '.ove', 1)
                maya.cmds.setAttr(shp + '.ovc', colorIndex)