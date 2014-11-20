#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Thu, 20 Nov 2014 17:10:31
#========================================
import os.path, time, findCoincidentGeometry
from FoleyUtils import scriptTool, uiTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'findCoincidentGeometry.ui'))
class findCoincidentGeometryUI(windowClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'findCoincidentGeometryUI'):
            return
        super(findCoincidentGeometryUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #------------------
    
    def on_pushButton_clicked(self, args=None):
        if args == None:return
        self.plainTextEdit.setPlainText('')
        self.plainTextEdit.appendPlainText('------ %s ------'%time.strftime("%H:%M:%S", time.localtime()))
        
        geometrys = findCoincidentGeometry.findCoincidentGeometrys()
        
        self.plainTextEdit.appendPlainText('\n'.join(geometrys))
        self.plainTextEdit.appendPlainText('------ %s ------'%time.strftime("%H:%M:%S", time.localtime()))