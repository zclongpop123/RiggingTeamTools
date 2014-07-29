#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Tue, 29 Jul 2014 09:29:32
#=============================================
import math, re, os
import maya.cmds as mc
from FoleyUtils import uiTool, scriptTool, mayaTool, mathTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#- Refresh Characters                                           +
#- Guess Character Type                                         +
#- Left arm, Right arm, Left leg, Right leg                     +
#- Left foreleg, Right foreleg, Left hindleg, Right hindleg     +
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


Uiwnd, UiClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'IKFKSwitch.ui'))
class IKFKSwitch(Uiwnd, UiClass):
    def __init__(self, parent = None):
        if uiTool.windowExists(parent, 'DDikfkSwitchWindow'):
                return    
            
        super(IKFKSwitch, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #--------
        self.on_actionRefreshCharacter_triggered(True)

    
    def on_actionRefreshCharacter_triggered(self, args=None):
        if args==None:return
        self.Controls = ' '.join(mc.ls())
    
        referenceCharacters = [mc.file(f, q=True, ns=True) for f in mc.file(q=True, r=True) if re.search('\Wcharacter\W', f)]
        self.CharacterComboBox.clear()
        for ns in referenceCharacters:
            self.CharacterComboBox.addItem(ns)
            


    def on_actionCurrentCharacterChanged_triggered(self, args=None):
        if args==None:return
        nameSpace = str(self.CharacterComboBox.currentText())
        if re.search('%s\S*%s'%(nameSpace, 'L_arm_mod_0'), self.Controls):
            self.radioButton_A.setChecked(True)
        else:
            self.radioButton_B.setChecked(True)

    #----------------------------------------------------------------------------------------------------------------
    @mayaTool.undo_decorator
    def on_actionLeftArmSwitch_triggered(self, args=None):
        if args==None:return
        nameSpace = str(self.CharacterComboBox.currentText())
        switchControl = re.search('%s\S*%s'%(nameSpace, 'L_armFkIk_ctl_0'), self.Controls)
        if not switchControl:return
    
        starts = switchControl.group().rsplit(':', 1)[0]
        if mc.getAttr('%s.FKIKBlend'%switchControl.group()) == 0:
            armToIK('L', starts)
            armToIK('L', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 1)
        else:
            armToFK('L', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 0)
            

   
    @mayaTool.undo_decorator 
    def on_actionRightArmSwitch_triggered(self, args=None):
        if args==None:return
        nameSpace = str(self.CharacterComboBox.currentText())
        switchControl = re.search('%s\S*%s'%(nameSpace, 'R_armFkIk_ctl_0'), self.Controls)
        if not switchControl:return
    
        starts = switchControl.group().rsplit(':', 1)[0]
        if mc.getAttr('%s.FKIKBlend'%switchControl.group()) == 0:
            armToIK('R', starts)
            armToIK('R', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 1)
        else:
            armToFK('R', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 0)
            
        
    @mayaTool.undo_decorator    
    def on_actionLeftLegSwitch_triggered(self, args=None):
        if args==None:return
        nameSpace = str(self.CharacterComboBox.currentText())
        switchControl = re.search('%s\S*%s'%(nameSpace, 'L_legFkIk_ctl_0'), self.Controls)
        if not switchControl:return
    
        starts = switchControl.group().rsplit(':', 1)[0]
        if mc.getAttr('%s.FKIKBlend'%switchControl.group()) == 0:
            legToIK('L', starts)
            legToIK('L', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 1)
        else:
            legToFK('L', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 0)        
        
        
    @mayaTool.undo_decorator   
    def on_actionRightLegSwitch_triggered(self, args=None):
        if args==None:return
        nameSpace = str(self.CharacterComboBox.currentText())
        switchControl = re.search('%s\S*%s'%(nameSpace, 'R_legFkIk_ctl_0'), self.Controls)
        if not switchControl:return
    
        starts = switchControl.group().rsplit(':', 1)[0]
        if mc.getAttr('%s.FKIKBlend'%switchControl.group()) == 0:
            legToIK('R', starts)
            legToIK('R', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 1)
        else:
            legToFK('R', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 0) 

    
    @mayaTool.undo_decorator
    def on_actionLeftForeLegSwitch_triggered(self, args=None):
        if args==None:return
        nameSpace = str(self.CharacterComboBox.currentText())
        switchControl = re.search('%s\S*%s'%(nameSpace, 'L_legFrontFkIk_ctl_0'), self.Controls)
        if not switchControl:return
    
        starts = switchControl.group().rsplit(':', 1)[0]
        if mc.getAttr('%s.FKIKBlend'%switchControl.group()) == 0:
            foreLegToIK('L', starts)
            foreLegToIK('L', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 1)
        else:
            foreLegToFK('L', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 0) 
    
    

    @mayaTool.undo_decorator  
    def on_actionRightForeLegSwitch_triggered(self, args=None):
        if args==None:return
        nameSpace = str(self.CharacterComboBox.currentText())
        switchControl = re.search('%s\S*%s'%(nameSpace, 'R_legFrontFkIk_ctl_0'), self.Controls)
        if not switchControl:return
    
        starts = switchControl.group().rsplit(':', 1)[0]
        if mc.getAttr('%s.FKIKBlend'%switchControl.group()) == 0:
            foreLegToIK('R', starts)
            foreLegToIK('R', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 1)
        else:
            foreLegToFK('R', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 0) 
    
    
        
    @mayaTool.undo_decorator    
    def on_actionLeftHindLegSwitch_triggered(self, args=None):
        if args==None:return
        nameSpace = str(self.CharacterComboBox.currentText())
        switchControl = re.search('%s\S*%s'%(nameSpace, 'L_legFkIk_ctl_0'), self.Controls)
        if not switchControl:return
    
        starts = switchControl.group().rsplit(':', 1)[0]
        if mc.getAttr('%s.FKIKBlend'%switchControl.group()) == 0:
            hindLegToIK('L', starts)
            hindLegToIK('L', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 1)
        else:
            hindLegToFK('L', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 0)        
        
        
    @mayaTool.undo_decorator   
    def on_actionRightHindLegSwitch_triggered(self, args=None):
        if args==None:return
        nameSpace = str(self.CharacterComboBox.currentText())
        switchControl = re.search('%s\S*%s'%(nameSpace, 'R_legFkIk_ctl_0'), self.Controls)
        if not switchControl:return
        
        starts = switchControl.group().rsplit(':', 1)[0]
        if mc.getAttr('%s.FKIKBlend'%switchControl.group()) == 0:
            hindLegToIK('R', starts)
            hindLegToIK('R', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 1)
        else:
            hindLegToFK('R', starts)
            mc.setAttr('%s.FKIKBlend'%switchControl.group(), 0)   


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ ( Switch Function ) +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 
def matchFK(side='L', starts='', args=None):
    if not args:return
    for jnt, ctr in args:
        #-> 1
        jnt = starts + ':' + jnt%side
        ctr = starts + ':' + ctr%side
        #-> 2
        mid = mc.duplicate(ctr, po=True)[0]
        for attr in ('tx', 'ty', 'tz', 'rx', 'ry', 'rz'):
            mc.setAttr('%s.%s'%(mid, attr), l=False, k=True, cb=True)
        mc.parentConstraint(jnt, mid)
        #-> 3
        posi = mc.xform(mid, q=True, ws=True, rp=True)
        rota = mc.xform(mid, q=True, ws=True, ro=True)
        mc.xform(ctr, ws=True, t=posi)
        mc.xform(ctr, ws=True, ro=rota)
        #->4
        mc.delete(mid)
    



def matchIK(side='L', starts='', args=None):
    if not args:return
    for jnt, ctr in args:
        jnt = starts + ':' + jnt%side
        ctr = starts + ':' + ctr%side
        
        posi = mc.xform(jnt, q=True, ws=True, rp=True)
        rota = mc.xform(jnt, q=True, ws=True, ro=True)
        mc.xform(ctr, ws=True, t=posi)
        mc.xform(ctr, ws=True, ro=rota)
    
    userDefAttributes = mc.listAttr(ctr, ud=True, k=True)
    if not userDefAttributes:return
    
    for attr in userDefAttributes:
        defaultValue = mc.addAttr('%s.%s'%(ctr, attr), q=True, dv=True)
        mc.setAttr('%s.%s'%(ctr, attr), defaultValue)



def matchScale(starts, side, src, dst):
    value = mc.getAttr(starts + ':' + src%side)
    try:
        mc.setAttr(starts + ':' + dst%side, value)
    except:
        pass
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- ( Components Switch ) -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


def armToFK(side='L', starts=''):
    args = (('%s_armShoulderIk_jnt_0', '%s_armShoulderFk_ctl_0'),
            ('%s_armElbowIk_jnt_0', '%s_armElbowFk_ctl_0'),
            ('%s_armWristIk_jnt_0', '%s_armWristFk_ctl_0'))
    matchFK(side, starts, args)




def armToIK(side='L', starts=''):
    args = (('%s_armWrist_bnd_0',  '%s_armIk_ctl_0'), 
            ('%s_armElbow_bnd_0', '%s_poleArm_ctl_0'))
    matchIK(side, starts, args)
    #- move pole Vector Control -
    pointJointA = starts + ':' + '%s_armShoulder_bnd_0'%side
    pointJointB = starts + ':' + '%s_armElbow_bnd_0'%side
    pointJointC = starts + ':' + '%s_armWrist_bnd_0'%side
    endP = mathTool.getPoleVectorPosition(pointJointA, pointJointB, pointJointC)
    mc.move(endP[0], endP[1], endP[2], starts + ':' + '%s_poleArm_ctl_0'%side, a=True)




def legToFK(side='L', starts=''):
    args = (('%s_legHipIk_jnt_0', '%s_legHipFk_ctl_0'),
            ('%s_legKneeIk_jnt_0', '%s_legKneeFk_ctl_0'),
            ('%s_legAnkle_bnd_0', '%s_legAnkleFk_ctl_0'), 
            ('%s_legMidfoot_bnd_0', '%s_legMidfootFk_ctl_0'),
            ('%s_legToes_bnd_0', '%s_legToesFk_ctl_0'))
    matchFK(side, starts, args)
 



def legToIK(side='L', starts=''):
    args = (('%s_legIk_ctlAim_0',  '%s_legIk_ctl_0'),)
    matchIK(side, starts, args)
    #- move pole Vector Control -
    pointJointA = starts + ':' + '%s_legHip_bnd_0'%side
    pointJointB = starts + ':' + '%s_legKnee_bnd_0'%side
    pointJointC = starts + ':' + '%s_legAnkle_bnd_0'%side
    endP = mathTool.getPoleVectorPosition(pointJointA, pointJointB, pointJointC)
    mc.move(endP[0], endP[1], endP[2], starts + ':' + '%s_poleLeg_ctl_0'%side, a=True)





def hindLegToFK(side='L', starts=''):
    matchScale(starts, side, '%s_legIk_ctl_0.Lenght2', '%s_hindLegKneeFk_ctl_0.sx') 
    matchScale(starts, side, '%s_legIk_ctl_0.Lenght3', '%s_hindLegHockFk_ctl_0.sx') 

    args = (('%s_hindLegHip_bnd_0', '%s_hindLegHipFk_ctl_0'),
            ('%s_hindLegKnee_bnd_0', '%s_hindLegKneeFk_ctl_0'), 
            ('%s_hindLegHock_bnd_0', '%s_hindLegHockFk_ctl_0'), 
            ('%s_hindLegAnkle_bnd_0', '%s_hindLegAnkleFk_ctl_0'),
            ('%s_hindLegMidfoot_bnd_0', '%s_hindLegMidfootFk_ctl_0'),
            ('%s_hindLegToes_bnd_0', '%s_hindLegToesFk_ctl_0'))
    matchFK(side, starts, args)
    




def hindLegToIK(side='L', starts=''):
    args = (('%s_legIk_ctlAim_0',  '%s_legIk_ctl_0'), )
    matchIK(side, starts, args)
    
    HipControls = (('%s_hindLegHipFk_ctl_0', '%s_hindLegHipIk_ctl_0'), )
    matchFK(side, starts, HipControls)
    
    #- move pole Vector Control -
    pointJointA = starts + ':' + '%s_hindLegKnee_bnd_0'%side
    pointJointB = starts + ':' + '%s_hindLegHock_bnd_0'%side
    pointJointC = starts + ':' + '%s_hindLegAnkle_bnd_0'%side
    endP = mathTool.getPoleVectorPosition(pointJointA, pointJointB, pointJointC)
    mc.move(endP[0], endP[1], endP[2], starts + ':' + '%s_poleLeg_ctl_0'%side, a=True)




def foreLegToFK(side='L', starts=''):
    matchScale(starts, side, '%s_legFrontIk_ctl_0.Lenght2', '%s_foreLegElbowFk_ctl_0.sx')    
    args = (('%s_foreLegScapula_bnd_0', '%s_foreLegScapulaFk_ctl_0'),
            ('%s_foreLegShoulder_bnd_0', '%s_foreLegShoulderFk_ctl_0'),
            ('%s_foreLegElbow_bnd_0', '%s_foreLegElbowFk_ctl_0'),
            ('%s_foreLegFoot_bnd_0', '%s_foreLegFootFk_ctl_0'),
            ('%s_foreLegMidfoot_bnd_0', '%s_foreLegMidfootFk_ctl_0'),
            ('%s_foreLegToes_bnd_0', '%s_foreLegToesFk_ctl_0'))
    matchFK(side, starts, args) 
        




def foreLegToIK(side='L', starts=''):
    args = (('%s_legFrontIk_ctlAim_0',  '%s_legFrontIk_ctl_0'),)
    matchIK(side, starts, args)
    
    #- move pole Vector Control -
    pointJointA = starts + ':' + '%s_foreLegShoulder_bnd_0'%side
    pointJointB = starts + ':' + '%s_foreLegElbow_bnd_0'%side
    pointJointC = starts + ':' + '%s_foreLegFoot_bnd_0'%side
    endP = mathTool.getPoleVectorPosition(pointJointA, pointJointB, pointJointC)
    mc.move(endP[0], endP[1], endP[2], starts + ':' + '%s_poleLegFront_ctl_0'%side, a=True)



#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* ( Rig  Use ) *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#

def addIKFKSwitch():
    ControlData = (
    ('L_legFrontIk_ctl_0', 'L_foreLegFoot_bnd_0'),
    ('R_legFrontIk_ctl_0', 'R_foreLegFoot_bnd_0'),
    ('L_legIk_ctl_0',      'L_hindLegAnkle_bnd_0'),
    ('R_legIk_ctl_0',      'R_hindLegAnkle_bnd_0'),
    ('L_legIk_ctl_0',      'L_legAnkle_bnd_0'),
    ('R_legIk_ctl_0',      'R_legAnkle_bnd_0'))
    
    for ctl, jnt in ControlData:
        if not mc.objExists(ctl):continue
        if not mc.objExists(jnt):continue
        
        if mc.objExists(ctl.replace('_ctl_', '_ctlAim_')):
            print '>>> warning: IK FK Switch Aim was Exists !!! ( %s  ->  %s )'%(ctl, ctl.replace('_ctl_', '_ctlAim_'))
            continue
        
        ControlAim = mc.duplicate(ctl, po=True, name=ctl.replace('_ctl_', '_ctlAim_'))[0]
        mc.parentConstraint(jnt,  ControlAim, mo=True)
        mc.sets(ControlAim, e=True, rm='control_set')
        print '>>>  add IK FK Switch on ( %s  ->  %s )'%(ctl, ControlAim)