import re, rigToolUtils
import maya.cmds as mc
#=====================================================================================
CONTROL_TYPE = ('_ctl_', '_ctr_')

TRANS_ATTRIBUTES  = ('translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ')
SCACLE_AAARIBUTES = ('scaleX', 'scaleY', 'scaleZ', 'visibility')

#----------------------------------------------------------------------------------------------------------

def Set(control):
    attributes = mc.listAttr(control, k=True)
    if attributes == None:return 
    for attr in attributes:
        #- guess default attributes
        defaultValue = 0
        if attr in TRANS_ATTRIBUTES:
            defaultValue = 0
        elif attr in SCACLE_AAARIBUTES:
            defaultValue = 1
        else:
            minV = mc.addAttr('%s.%s'%(control, attr), q=True, min=True) or 0
            maxV = mc.addAttr('%s.%s'%(control, attr), q=True, max=True) or 0
            defV = mc.addAttr('%s.%s'%(control, attr), q=True, dv=True)  or 0

            defaultValue = min(max(minV, defV), maxV)
        
        #- set attribute
        if mc.getAttr('%s.%s'%(control, attr), se=True):
            mc.setAttr('%s.%s'%(control, attr), defaultValue)

#----------------------------------------------------------------------------------------------------------
@rigToolUtils.undo_decorator
def backtoTpose():
    selectControl = mc.ls(sl=True)
    if len(selectControl) == 0:
        mc.warning('you must select a control (any one) from a character !!!')
        return 

    #- list all of transforms 
    transforms = ' '.join(mc.ls(type='transform'))
    
    #- list all of the controls
    controls   = re.findall('(\S+(%s)\S+)'%'|'.join(CONTROL_TYPE), transforms)

    #- remove duplicates
    controls   = [x[0] for x in controls]
    
    #- do it
    for control in controls:
        if selectControl[0].rsplit(':', 1)[0] == control.rsplit(':', 1)[0]:
            Set(control)