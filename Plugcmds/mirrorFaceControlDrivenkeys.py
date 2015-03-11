#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 09 Mar 2015 14:38:00
#========================================
import re
import maya.cmds as mc
from FoleyUtils import uiTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def getDrivenKeys(obj):
    keys = mc.listConnections(obj, t='animCurve') or []
    for unc in mc.listConnections(obj, t='unitConversion') or []:
        keys.extend(mc.listConnections(unc, t='animCurve') or list())
    
    for k in keys:
        driver = mc.connectionInfo('%s.input'%k, sfd=True)
        driven = mc.connectionInfo('%s.output'%k, dfs=True)
        if not driver or not driven:
            continue
        if mc.nodeType(driver) == 'unitConversion':
            driver = mc.connectionInfo('%s.input'%driver.split('.')[0], sfd=True)
        
        yield driver, driven[0]



def mirrorDrivenkeys(src, dst):
    for driver, driven in getDrivenKeys(src):
        newDriver = driver.replace(src, dst)
        newDriven = driven.replace('L_', 'R_')
        if not mc.objExists(newDriven) or newDriven == driven:
            newDriven = driven.replace('left', 'right')
        if not mc.objExists(newDriven) or newDriven == driven:
            newDriven = driven.replace('L', 'R')         

        if not mc.objExists(newDriver) or not mc.objExists(newDriven):
            continue
        if newDriven == driven:
            continue
        
        driverValues = mc.keyframe(driven, q=True, fc=True)
        drivenValues = mc.keyframe(driven, q=True, vc=True)
        for drv, dnv in zip(driverValues, drivenValues):
            if re.search('(translateX|eyeRotInner_ctl_0.rotateZ|mouthCorner_ctl_0\.translateY|mouth_ctl_0\.translateY)$', newDriver):
                dnv = dnv * -1
            if re.search('(mainCheek_ctl_0\.translateX)$', newDriver):
                dnv = dnv * -1
            mc.setDrivenKeyframe(newDriven, cd=newDriver, dv=drv, v=dnv)
        
        print 'Copy Driven keys: %s : %s -> %s : %s'%(driver, driven, newDriver, newDriven)



def mirrorDrivenkeyByControls():
    if not uiTool.warning(message='Mirror face control\'s drivenKeys? ?'):
        return
    controls = mc.ls('L_*_ctl_*', type='transform')
    for src in controls:
        dst = src.replace('L_', 'R_')
        if not mc.objExists(dst):
            continue
        mirrorDrivenkeys(src, dst)