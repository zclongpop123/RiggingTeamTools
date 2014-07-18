import maya.cmds as mc
import math

def makeRotateInfo():
    selJoints = mc.ls(sl=True, type='joint')
    for Jnt in selJoints:
        makeRotateInfoForOneJoint(Jnt)
        
        
def makeRotateInfoForOneJoint(joint):
    #- create sets
    TempCircle = mc.circle(r=1, ch=False)
    TempLine = mc.curve(d=1, p=((-1, 1, 0), (-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)))
    
    BaseLoc = mc.spaceLocator(p=(0,0,0), name='%s_RIF_Baseloc'%joint.rsplit('_', 2)[0])[0]
    AimLoc = mc.spaceLocator(p=(0,0,0), name='%s_RIF_aimLoc'%joint.rsplit('_', 2)[0])[0]
    
    grp = mc.group(TempCircle, TempLine, BaseLoc, AimLoc, name='%s_RIF_G'%joint.rsplit('_', 2)[0])
    
    #- set Temp Curve Template
    for temp in (TempCircle, TempLine):
        shape = mc.listRelatives(temp, s=True, path=True)
        mc.setAttr('%s.ove'%shape[0], 1)
        mc.setAttr('%s.ovdt'%shape[0], 1)
    
    #- lock attributes
    for attr in mc.listAttr(BaseLoc, k=True):
        if attr in ('translateX', 'translateY'):
            continue
        mc.setAttr('%s.%s'%(BaseLoc, attr), l=True, k=False)
    
    #- limit Translate
    mc.transformLimits(BaseLoc, tx=(-1, 1), ty=(-1, 1), etx=(True, True), ety=(True, True))
    mc.pointConstraint(AimLoc, BaseLoc, skip='z')
    
    
    #- add Atributes
    for attr in ('x', 'y', 'ypxp', 'ypxn', 'ynxp', 'ynxn', 'up', 'down', 'left', 'right'):
        mc.addAttr(grp, sn=attr, k=True)
    
    #- comp connections
    #- 1
    mc.connectAttr('%s.tx'%BaseLoc, '%s.x'%grp)
    mc.connectAttr('%s.ty'%BaseLoc, '%s.y'%grp)      
    
    #- 2
    Values = ('ypxp', 0.707,0.707), ('ypxn', -0.707,0.707), ('ynxp', 0.707,-0.707), ('ynxn', -0.707,-0.707)
    for Attr, x, y in Values:
        node = mc.createNode('multDoubleLinear')
        mc.setDrivenKeyframe('%s.i1'%node, cd='%s.tx'%BaseLoc, dv=0, v=0, itt='linear', ott='linear')
        mc.setDrivenKeyframe('%s.i1'%node, cd='%s.tx'%BaseLoc, dv=x, v=1, itt='linear', ott='linear')
        mc.setDrivenKeyframe('%s.i2'%node, cd='%s.ty'%BaseLoc, dv=0, v=0, itt='linear', ott='linear')
        mc.setDrivenKeyframe('%s.i2'%node, cd='%s.ty'%BaseLoc, dv=y, v=1, itt='linear', ott='linear')        
        mc.connectAttr('%s.o'%node, '%s.%s'%(grp, Attr))
    
    #- 3
    # to line 71

    #- match Position
    mc.delete(mc.parentConstraint(joint, grp))
    JntChildren = mc.listRelatives(joint, c=True, path=True, type='joint')
    if not JntChildren:return
    mc.delete(mc.aimConstraint(JntChildren, grp, aim=(0,0,1), u=(0,1,0)))
    mc.delete(mc.pointConstraint(JntChildren, AimLoc))
    mc.parentConstraint(joint, AimLoc, mo=True)

    #- match Scale
    startPosi = mc.xform(grp, q=True, ws=True, rp=True)
    endPosi = mc.xform(AimLoc , q=True, ws=True, rp=True)
    Dis = math.sqrt((startPosi[0] - endPosi[0]) ** 2 + (startPosi[1] - endPosi[1]) ** 2 + (startPosi[2] - endPosi[2]) ** 2)
    mc.setAttr(grp + '.sx', Dis)
    mc.setAttr(grp + '.sy', Dis)
    mc.setAttr(grp + '.sz', Dis)    


    #- connect line 52
    Expstrings = '\
    $Ah = %s.ty;\n\
    $Aw = %s.tx;\n\
    $C = %s;\n\
    %s.%s = clamp(0, 180,  90 - acos($Ah / $C) * 180 / 3.14159265359);\n\
    %s.%s = clamp(-180, 0, 90 - acos($Ah / $C) * 180 / 3.14159265359);\n\
    %s.%s = clamp(0, 180,  90 - acos($Aw / $C) * 180 / 3.14159265359);\n\
    %s.%s = clamp(-180, 0, 90 - acos($Aw / $C) * 180 / 3.14159265359);\n\
    '%(BaseLoc, BaseLoc, mc.getAttr('%s.tz'%AimLoc),  grp, 'up', grp, 'down', grp, 'left', grp, 'right')
    mc.expression(s=Expstrings)
    #---------------------------------------------------------------------------------------
    
    
    
    # connect attbutes to prefs_grp
    if not mc.objExists('prefs_grp'):return
    typ = joint.rsplit('_', 2)[0]
    mc.addAttr('prefs_grp', sn=typ, k=True)
    mc.setAttr('prefs_grp.' + typ, l=True)
    for Attr in mc.listAttr(grp, ud=True):
        mc.addAttr('prefs_grp', sn=typ + Attr, k=True)
        mc.connectAttr('%s.%s'%(grp, Attr), 'prefs_grp.%s%s'%(typ , Attr))

    return grp, AimLoc