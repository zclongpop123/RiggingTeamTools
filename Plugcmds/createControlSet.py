#=================================
# author: changlong.zang
#   date: 2014-06-10
#=================================
import os.path
from FoleyUtils import scriptTool, uiTool
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'createControlSet.ui'))
class CreateControlSetUI(windowClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'makeControlSetUI'):
            return 
        super(CreateControlSetUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
    
    #=============================================================================================
    def __createSet(self, name):
        if not mc.objExists(name):
            mc.sets(n=name, em=True)
        if name != 'Allctrls': return
        
        if mc.objExists('body_Ctrls'):
            mc.sets('body_Ctrls', add=name)
            
        if mc.objExists('facial_Ctrls'):
            mc.sets('facial_Ctrls', add=name)


    def __addMembers(self, name):
        selObj = mc.ls(sl=True)
        if selObj == []:return
        mc.sets(selObj, add=name)


    def on_btn_AllAddMebbers_clicked(self, args=None):
        if args == None:return
        self.__createSet('Allctrls')
        self.__addMembers('Allctrls')
        

    def on_btn_BodyAddMebbers_clicked(self, args=None):
        if args == None:return
        self.__createSet('body_Ctrls')
        self.__addMembers('body_Ctrls')
        

    def on_btn_FaceAddMebbers_clicked(self, args=None):
        if args == None:return
        self.__createSet('facial_Ctrls')
        self.__addMembers('facial_Ctrls')
    
    #=============================================================================================

    def __removeMembers(self, name):
        if not mc.objExists(name):return
        selObj = mc.ls(sl=True)
        if selObj == []:return
        mc.sets(selObj, remove=name)        
            

    def on_btn_AllRemoveMebbers_clicked(self, args=None):
        if args == None:return
        self.__removeMembers('Allctrls')
    
    
    def on_btn_BodyRemoveMebbers_clicked(self, args=None):
        if args == None:return
        self.__removeMembers('body_Ctrls')
        

    def on_btn_FaceRemoveMebbers_clicked(self, args=None):
        if args == None:return
        self.__removeMembers('facial_Ctrls')
        
    #=============================================================================================