#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
#=============================================
import os
from PyQt4 import QtGui
from FoleyUtils import uiTool, scriptTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
Uiwnd, UiClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'RootUI.ui'))

class PlugTool(Uiwnd, UiClass):
    def __init__(self, parent=uiTool.getMayaWindow()):
        if uiTool.windowExists(parent, 'DDrigTools'):
            return
        
        super(PlugTool, self).__init__(parent)
        self.setupUi(self)
        
        #===============================================
        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(1)
        #============================================================================================================
        self.btn_TitleA.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'pencil.png')))
        self.btn_TitleB.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'pencil.png')))
        self.btn_TitleC.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'pencil.png')))
        
        self.btn_GrabWindow.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'scissors.png')))        
        self.btn_CleanWindows.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(), 'icons', 'brush.png')))
        self.btn_Help.setIcon(QtGui.QIcon(os.path.join(scriptTool.getScriptPath(),   'icons', 'help.png')))
        #============================================================================================================
        self.show()

    
    def on_btn_GrabWindow_clicked(self, args=None):
        if args==None:return
        path = os.path.join(scriptTool.getScriptPath(), 'Snapshot', 'SogouSnapShot.exe')
        path = path.replace('/', '\\')
        os.popen('explorer.exe %s'%path)
        

    def on_btn_CleanWindows_clicked(self, args=None):
        if args==None:return
        uiTool.cleanChildrenWindows(self.parent())


    def on_btn_Help_clicked(self, args=None):
        if args==None:return
        path = os.path.join(scriptTool.getScriptPath(), 'ToolIndex', 'readme.docx')
        path = path.replace('/', '\\')
        os.system('explorer.exe %s'%path)
        

    def on_btn_RenameJointToSystem_clicked(self, args=None):
        if args==None:return
        import Plugcmds.RenameJnts
        reload(Plugcmds.RenameJnts)
        Plugcmds.RenameJnts.setupRename()


    def on_btn_MirrorControlShape_clicked(self, args=None):
        if args==None:return
        import Plugcmds.mirrorCtlShp
        reload(Plugcmds.mirrorCtlShp)
        Plugcmds.mirrorCtlShp.MirrorControlShp(uiTool.getMayaWindow())

    def on_btn_LatticeWeight_clicked(self, args=None):
        if args==None:return
        import Plugcmds.latticeWeightsTool
        reload(Plugcmds.latticeWeightsTool)
        Plugcmds.latticeWeightsTool.latticeWeightTool()


    def on_btn_ControlColor_clicked(self, args=None):
        if args==None:return
        import Plugcmds.ControlColor
        reload(Plugcmds.ControlColor)
        Plugcmds.ControlColor.ControlColorUI(uiTool.getMayaWindow())
      
 
    def on_btn_NameTool_clicked(self, args=None):
        if args==None:return
        import Plugcmds.nameToolCmds
        reload(Plugcmds.nameToolCmds)
        Plugcmds.nameToolCmds.NameUI(uiTool.getMayaWindow())


    def on_btn_SetToesDrivenKey_clicked(self, args=None):
        if args==None:return
        import Plugcmds.SetDrivenKeysforToes
        reload(Plugcmds.SetDrivenKeysforToes)
        Plugcmds.SetDrivenKeysforToes.SetDrivenKeyforToes(uiTool.getMayaWindow())


    def on_btn_MakeJointsOnCurve_clicked(self, args=None):
        if args==None:return
        import Plugcmds.makeAttachJoints 
        reload(Plugcmds.makeAttachJoints )
        Plugcmds.makeAttachJoints .makeAttachJoints(uiTool.getMayaWindow())
        

    def on_btn_MirrorDrivenkey_clicked(self, args=None):
        if args==None:return
        import Plugcmds.mirrorSDK
        reload(Plugcmds.mirrorSDK)
        Plugcmds.mirrorSDK.MirrorSetDrivenKey(uiTool.getMayaWindow())

     
    def on_btn_QuickSDKA_clicked(self, args=None):
        if args==None:return
        import Plugcmds.quickSDKTool
        reload(Plugcmds.quickSDKTool)
        Plugcmds.quickSDKTool.quickSDK(uiTool.getMayaWindow())
        
          
    def on_btn_MoveObject_clicked(self, args=None):
        if args==None:return
        import Plugcmds.ChangeOBJpivot
        reload(Plugcmds.ChangeOBJpivot)
        Plugcmds.ChangeOBJpivot.ChangeOBJpivot(uiTool.getMayaWindow())

        
    def on_btn_InspectScene_clicked(self, args=None):
        if args==None:return
        import Plugcmds.inspectScene.inspectScene
        reload(Plugcmds.inspectScene.inspectScene)
        Plugcmds.inspectScene.inspectScene.InspectSceneUI(uiTool.getMayaWindow())
        
      
    def on_btn_BlendIKFKOutput_clicked(self, args=None):
        if args==None:return
        import Plugcmds.BlendIKFKoutputs
        reload(Plugcmds.BlendIKFKoutputs)
        instance = Plugcmds.BlendIKFKoutputs.CompIKFKoutput()
        instance.builde()
        
    
    def on_btn_DynamicControl_clicked(self, args=None):
        if args==None:return
        import Plugcmds.DynControl.DynControl
        reload(Plugcmds.DynControl.DynControl)
        Plugcmds.DynControl.DynControl.DynControl(uiTool.getMayaWindow())
        
        
    def on_btn_makeRotateInfo_clicked(self, args=None):
        if args==None:return
        import Plugcmds.makeRotateInfo
        reload(Plugcmds.makeRotateInfo)
        Plugcmds.makeRotateInfo.makeRotateInfo()
        
        
    def on_btn_FixAnim_clicked(self, args=None):
        if args==None:return
        import Plugcmds.FixAnim     
        reload(Plugcmds.FixAnim)
        Plugcmds.FixAnim.FixAnim(uiTool.getMayaWindow())


    def on_btn_IKFKSwitch_clicked(self, args=None):
        if args==None:return
        import Plugcmds.IKFKSwitch.IKFKSwitch
        reload(Plugcmds.IKFKSwitch.IKFKSwitch)
        Plugcmds.IKFKSwitch.IKFKSwitch.IKFKSwitch(uiTool.getMayaWindow())
        
    
    def on_btn_AddIKFKSwitch_clicked(self, args=None):
        if args==None:return
        import Plugcmds.IKFKSwitch 
        reload(Plugcmds.IKFKSwitch)
        Plugcmds.IKFKSwitch .addIKFKSwitch()
        
    
    def on_btn_MakeHeadStreatch_clicked(self, args=None):
        if args==None:return
        import Plugcmds.HeadStreatch.HeadStreatchTool
        reload(Plugcmds.HeadStreatch.HeadStreatchTool)
        Plugcmds.HeadStreatch.HeadStreatchTool.HeadStreatchUI(uiTool.getMayaWindow())
        
        
    def on_btn_AddPalmJoint_clicked(self, args=None):
        if args==None:return
        import Plugcmds.addPalmBindJoint
        reload(Plugcmds.addPalmBindJoint)
        Plugcmds.addPalmBindJoint.addPalmBindJoint()
        
    
    def on_btn_QuickSDKB_clicked(self, args=None):
        if args==None:return
        import Plugcmds.quickSetDrivenKey 
        reload(Plugcmds.quickSetDrivenKey )
        Plugcmds.quickSetDrivenKey .QuickSetDrivenKey(uiTool.getMayaWindow())
        
    
    def on_btn_faceControlBuilder_clicked(self, args=None):
        if args==None:return
        import Plugcmds.ConvertControl.FaceControlBuilderUI
        reload(Plugcmds.ConvertControl.FaceControlBuilderUI)
        Plugcmds.ConvertControl.FaceControlBuilderUI.FaceControlBuilderUI(uiTool.getMayaWindow())   
        
    
    def on_btn_AddTwistJoints_clicked(self, args=None):
        if args==None:return
        import Plugcmds.addTwistJoints.UI
        reload(Plugcmds.addTwistJoints.UI)
        Plugcmds.addTwistJoints.UI.AddTwistJointsUI(uiTool.getMayaWindow())
        
        
    def on_btn_SaveDrivenKey_clicked(self, args=None):
        if args==None:return
        import Plugcmds.saveDrivenKeys
        reload(Plugcmds.saveDrivenKeys)
        Plugcmds.saveDrivenKeys.SaveDrivenKeyWindow(uiTool.getMayaWindow())

   
    def on_btn_ControlSelecter_clicked(self, args=None):
        if args==None:return
        import Plugcmds.ControlSelecter.ControlSelecterUI
        reload(Plugcmds.ControlSelecter.ControlSelecterUI)
        Plugcmds.ControlSelecter.ControlSelecterUI.ControlSelecterWnd(uiTool.getMayaWindow())

 
    def on_btn_ShapeBuilder_clicked(self, args=None):
        if args == None:return
        import Plugcmds.ShapeBuilder.ShapeBuilderUI
        reload(Plugcmds.ShapeBuilder.ShapeBuilderUI)
        Plugcmds.ShapeBuilder.ShapeBuilderUI.ShapeBuilderUI(uiTool.getMayaWindow())
    
    
    def on_btn_Tpose_clicked(self, args=None):
        if args == None:return
        import Plugcmds.Tpose
        reload(Plugcmds.Tpose)
        Plugcmds.Tpose.backtoTpose()
        
    
    def on_btn_BlendShapeWeightTool_clicked(self, args=None):
        if args == None:return
        import Plugcmds.blendShapeWeights
        reload(Plugcmds.blendShapeWeights)
        Plugcmds.blendShapeWeights.BlendShapeWeightUI(uiTool.getMayaWindow())
        
    
    def on_btn_CopyBlendShapeWeights_clicked(self, args=None):
        if args == None:return
        import Plugcmds.CopyBlendShapeWeights.CopyBlendShapeWeights
        reload(Plugcmds.CopyBlendShapeWeights.CopyBlendShapeWeights)
        Plugcmds.CopyBlendShapeWeights.CopyBlendShapeWeights.CopyBlendShapeWeightsUI(uiTool.getMayaWindow())    
        
        
        
    def on_btn_animSceneReader_clicked(self, args=None):
        if args == None:return
        import Plugcmds.AnimSceneReader.AnimSceneReader
        reload(Plugcmds.AnimSceneReader.AnimSceneReader)
        Plugcmds.AnimSceneReader.AnimSceneReader.AnimSceneReaderUI(uiTool.getMayaWindow())       

    
    def on_btn_ReBuildeTargents_clicked(self, args=None):
        if args == None:return
        import Plugcmds.buildTargents
        reload(Plugcmds.buildTargents)
        Plugcmds.buildTargents.BuildTargents(uiTool.getMayaWindow())
        

    def on_btn_mirrorDrivenkeys_clicked(self, args=None):
        if args == None:return
        import Plugcmds.mirrorDrivenKeys
        reload(Plugcmds.mirrorDrivenKeys)
        Plugcmds.mirrorDrivenKeys.MirrorDrivenKeysUI(uiTool.getMayaWindow())
        
        
    def on_btn_makeControlSet_clicked(self, args=None):
        if args == None:return
        import Plugcmds.createControlSet
        reload(Plugcmds.createControlSet)
        Plugcmds.createControlSet.CreateControlSetUI(uiTool.getMayaWindow())        
    
    
    def on_btn_addGroups_clicked(self, args=None):
        if args == None:return
        import Plugcmds.addGroups
        reload(Plugcmds.addGroups)
        Plugcmds.addGroups.AddGroup(uiTool.getMayaWindow())
    
    
    def on_btn_fixShapeTool_clicked(self, args=None):
        if args == None:return
        import Plugcmds.FixShape.FixShape
        reload(Plugcmds.FixShape.FixShape)
        Plugcmds.FixShape.FixShape.FixShapeUI(uiTool.getMayaWindow())
    
    def on_btn_ReplaceUV_clicked(self, args=None):
        if args == None:return
        import Plugcmds.ReplaceUV.ReplaceUV
        reload(Plugcmds.ReplaceUV.ReplaceUV)
        Plugcmds.ReplaceUV.ReplaceUV.ReplaceUV(uiTool.getMayaWindow())
    
    def on_btn_EditBlendShapeWeights_clicked(self, args=None):
        if args == None:return
        import Plugcmds.blendShapeWeightsTool.blendShapeWeights
        reload(Plugcmds.blendShapeWeightsTool.blendShapeWeights)
        Plugcmds.blendShapeWeightsTool.blendShapeWeights.BlendShapeWeightsUI(uiTool.getMayaWindow()) 
    
    
    def on_btn_transWeights_clicked(self, args=None):
        if args == None:return
        import Plugcmds.TransWeights.TransWeights
        reload(Plugcmds.TransWeights.TransWeights)
        Plugcmds.TransWeights.TransWeights.TransWeightsUI(uiTool.getMayaWindow())    
    
    def on_btn_convertSkin_clicked(self, args=None):
        if args == None:return
        import Plugcmds.transSkinWeightsToCluster.transWeights
        reload(Plugcmds.transSkinWeightsToCluster.transWeights)
        Plugcmds.transSkinWeightsToCluster.transWeights.transWeightsUI(uiTool.getMayaWindow())
    
    def on_btn_copyClusterWeights_clicked(self, args=None):
        if args == None:return
        import Plugcmds.MirrorClusterWeights.MirrorClusterWeights
        reload(Plugcmds.MirrorClusterWeights.MirrorClusterWeights)
        Plugcmds.MirrorClusterWeights.MirrorClusterWeights.ClusterWeightsUI(uiTool.getMayaWindow())

    
    def on_btn_WeightsTool_clicked(self, args=None):
        if args == None:return
        import Plugcmds.weightsTool.weightsTool
        reload(Plugcmds.weightsTool.weightsTool)
        Plugcmds.weightsTool.weightsTool.WeightsTool(uiTool.getMayaWindow())    
    
    
    def on_btn_findCoincidentGeometry_clicked(self, args=None):
        if args == None:return
        import Plugcmds.findCoincidentGeometry.findCoincidentGeometryUI
        reload(Plugcmds.findCoincidentGeometry.findCoincidentGeometryUI)
        Plugcmds.findCoincidentGeometry.findCoincidentGeometryUI.findCoincidentGeometryUI(uiTool.getMayaWindow())        