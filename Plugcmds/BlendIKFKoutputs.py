import maya.cmds as mc
class CompIKFKoutput(object):
    prefsNode = 'prefs_grp'
    DriverDt = {
            'leftArm':('L_armElbowFk_ctl_0.ry', 'L_armElbowIk_jnt_0.ry', 'L_armFkIk_ctl_0'),
            'rightArm':('R_armElbowFk_ctl_0.ry', 'R_armElbowIk_jnt_0.ry', 'R_armFkIk_ctl_0'),
            'leftLeg':('L_legKneeFk_ctl_0.rz', 'L_legKneeIk_jnt_0.rz', 'L_legFkIk_ctl_0'),
            'rightLeg':('R_legKneeFk_ctl_0.rz', 'R_legKneeIk_jnt_0.rz', 'R_legFkIk_ctl_0')
            }
    part = ('leftArm','rightArm','leftLeg','rightLeg', 'leftAnkle', 'rightAnkle') 

    def builde(self):
        if not mc.objExists(self.prefsNode):return
        
        #-> add Attr
        for compent in self.part:
            mc.addAttr(self.prefsNode, sn=compent, k=True)
            mc.setAttr('%s.%s'%(self.prefsNode, compent), 0, l=True)
            #mc.addAttr(self.prefsNode, sn='%smax'%compent, nn='max', min=0, max=360, dv=100, k=True)
            #mc.addAttr(self.prefsNode, sn='%sBlend'%compent, nn='blend', min=0, max=1, dv=0, k=True)
            mc.addAttr(self.prefsNode, sn='%soutput'%compent, nn='output', min=0, max=360, dv=0, k=True)            
        
        
        
        
        for i, side in enumerate('LR'):
            
            RangeNode = mc.createNode('setRange')
            mc.setAttr('%s.oldMinY'%RangeNode, mc.getAttr('%s_legAnkle_bnd_0.rz'%side))
            mc.setAttr('%s.oldMaxY'%RangeNode, mc.getAttr('%s_legAnkle_bnd_0.rz'%side) + 360)
            mc.setAttr('%s.minY'%RangeNode, 0)
            mc.setAttr('%s.maxY'%RangeNode, 360)
            mc.connectAttr('%s_legAnkle_bnd_0.rz'%side, '%s.valueY'%RangeNode)
            mc.connectAttr('%s.oy'%RangeNode, '%s.%soutput'%(self.prefsNode, self.part[-2:][i]))
            mc.setAttr('%s.%soutput'%(self.prefsNode, self.part[-2:][i]), l=True)
        
        for compent, Joint in self.DriverDt.iteritems():
            if not mc.objExists(Joint[0]) or not mc.objExists(Joint[1]):return
            
            #-FK range
            #FKRange = mc.createNode('setRange')
            #mc.setAttr('%s.oldMinY'%FKRange, 0)
            #mc.setAttr('%s.oldMaxY'%FKRange, 0)
            #mc.setAttr('%s.minY'%FKRange, 0)
            #mc.setAttr('%s.maxY'%FKRange, 360)
            #mc.connectAttr(Joint[0], '%s.valueY'%FKRange)
            
            
            #-IK range
            IKRange = mc.createNode('setRange')
            mc.setAttr('%s.oldMinY'%IKRange, mc.getAttr(Joint[1]) - 360)
            mc.setAttr('%s.oldMaxY'%IKRange, mc.getAttr(Joint[1]) + 360)
            mc.setAttr('%s.minY'%IKRange, -360)
            mc.setAttr('%s.maxY'%IKRange,  360)
            mc.connectAttr(Joint[1], '%s.valueY'%IKRange)
            
            
            #-Blend
            BlendNode = mc.createNode('blendTwoAttr')
            mc.connectAttr('%s.FKIKBlend'%Joint[2], '%s.ab'%BlendNode)#mc.connectAttr('%s.%sBlend'%(self.prefsNode, compent), '%s.ab'%BlendNode)
            mc.connectAttr(Joint[0],        '%s.input[0]'%BlendNode)
            mc.connectAttr('%s.oy'%IKRange, '%s.input[1]'%BlendNode)
            
            
            mc.connectAttr('%s.o'%BlendNode, '%s.%soutput'%(self.prefsNode, compent))
            mc.setAttr('%s.%soutput'%(self.prefsNode, compent), l=True)
            
        mc.select(self.prefsNode)