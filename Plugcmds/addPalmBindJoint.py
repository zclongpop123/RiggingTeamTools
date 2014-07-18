import maya.cmds as mc


def addPalmBindJoint():
    
    def addJoint(side='L'):
        if mc.objExists('%s_armPalm_bnd_0'%side):return
        
        # make joint and locators
        Joint = mc.createNode('joint', name='%s_armPalm_bnd_0'%side)
        JointGroup = mc.group(Joint, name='%s_armPalm_bndgrp_0'%side)
        FKloc = mc.spaceLocator(p=(0,0,0), name='%s_armPalmFK_loc_0'%side)[0]
        IKloc = mc.spaceLocator(p=(0,0,0), name='%s_armPalmIK_loc_0'%side)[0]
        
        # constraint 
        constraintNode = mc.parentConstraint(FKloc, IKloc, JointGroup)
        
        # match position
        mc.delete(mc.parentConstraint('%s_armMiddleAIK_jnt_0'%side, FKloc))
        mc.delete(mc.parentConstraint('%s_armMiddleAIK_jnt_0'%side, IKloc))
    
        # parent locator
        mc.parent(FKloc, '%s_armWristFk_jnt_0'%side)
        mc.parent(IKloc, '%s_armMiddleAIK_jnt_0'%side)
        
        # make ikfk switch
        reverseNode = [x.split('.')[0] for x in mc.connectionInfo('%s_armFkIk_ctl_0.FKIKBlend'%side, dfs=True) if mc.nodeType(x.split('.')[0])=='reverse'][0]
        mc.connectAttr('%s.outputX'%reverseNode, '%s.%sW0'%(constraintNode[0], FKloc))
        mc.connectAttr('%s_armFkIk_ctl_0.FKIKBlend'%side, '%s.%sW1'%(constraintNode[0], IKloc))
        
        # add to bind set
        mc.sets(Joint, e=True, forceElement='bind_joints_set')
        
        # connect jointLayer
        mc.connectAttr('jointLayer.drawInfo',  '%s.drawOverride'%Joint)
        
        # parent joint
        mc.parent(JointGroup, '%s_armBind_org_0'%side)
    
    
    #-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    for side in 'LR':
        addJoint(side)     