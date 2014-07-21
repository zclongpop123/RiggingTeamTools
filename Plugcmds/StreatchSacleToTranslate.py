#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Fri, 18 Jul 2014 13:58:07
#=============================================
import re
import maya.cmds as mc
import maya.mel as mel
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
mel.eval('source "C:/Program Files/Autodesk/Maya2013.5/scripts/startup/channelBoxCommand.mel"')

def breakScale():
    Joints = ' '.join(mc.ls(type='joint'))
    arm_part_jnts = re.findall('[LR]_\w+Elbow\w*_bnd_\d+', Joints)
    leg_part_jnts = re.findall('[LR]_\w+Knee\w*_bnd_\d+',  Joints)
    
    two_part_jnts = []
    two_part_jnts.extend(dict.fromkeys(arm_part_jnts).keys())
    two_part_jnts.extend(dict.fromkeys(leg_part_jnts).keys())
    
    
    for jnt in two_part_jnts:
        mel.eval('CBdeleteConnection "%s.sx";'%jnt)
    
    print '#- Successed -#  Disconnected scale connection for : %s !!'%', '.join(two_part_jnts), 