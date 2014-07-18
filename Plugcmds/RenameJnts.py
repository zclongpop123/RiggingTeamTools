import maya.cmds as mc
from functools import  partial
class CompName(object):
    def __init__(self):
        self.LRDt = {1:'L_', -1:'R_', 0:'C_'}
        mc.button(h=26, l=self.BtnLab, c=partial(self.RenameJnts), p='BtnLayout')

    
    def RenameJnts(self, unuse):
        SelJnt = mc.ls(sl=True)
        for Jnt, nmLab in zip(SelJnt, self.Nms):
            Xvalue = mc.xform(Jnt, q=True, ws=True, t=True)[0]
            mc.rename(Jnt, nmLab.replace('L_', self.LRDt[cmp(Xvalue, 0)]))

        
class Spine(CompName):
    BtnLab = 'Spine (8)'
    Nms = ('C_root_bnd_0', 'C_backA_bnd_0', 'C_backB_bnd_0', 'C_chest_bnd_0', 'C_neck_bnd_0', 'C_neckend_bnd_0', 'C_head_bnd_0', 'C_skull_bnd_0')        


class Arm(CompName):
    BtnLab='Arm (4)'
    Nms = ('L_armClavicle_bnd_0',  'L_armShoulder_bnd_0',  'L_armElbow_bnd_0',  'L_armWrist_bnd_0')


class ThumbFin(CompName):
    BtnLab='Thumb (4)'
    Nms = ('L_armThumbA_bnd_0', 'L_armThumbB_bnd_0', 'L_armThumbC_bnd_0', 'L_armThumbD_bnd_0') 


class IndexFin(CompName):
    BtnLab='Index (4)'
    Nms = ('L_armIndexA_bnd_0', 'L_armIndexB_bnd_0', 'L_armIndexC_bnd_0', 'L_armIndexD_bnd_0')


class MiddleFin(CompName):
    BtnLab = 'Middle (4)'
    Nms = ('L_armMiddleA_bnd_0', 'L_armMiddleB_bnd_0', 'L_armMiddleC_bnd_0', 'L_armMiddleD_bnd_0')


class PinkeyFin(CompName):
    BtnLab = 'Pinkey (5)'
    Nms = ('L_armCup_bnd_0', 'L_armPinkyA_bnd_0', 'L_armPinkyB_bnd_0', 'L_armPinkyC_bnd_0', 'L_armPinkyD_bnd_0')


class Leg(CompName):
    BtnLab = 'Leg (5)'
    Nms = ('L_legHip_bnd_0', 'L_legKnee_bnd_0', 'L_legAnkle_bnd_0', 'L_legToes_bnd_0', 'L_legToe_bnd_0')


def setupRename():
    if mc.window('CompNameWnd', ex=True): mc.deleteUI('CompNameWnd', wnd=True)
    if mc.windowPref('CompNameWnd', ex=True): mc.windowPref('CompNameWnd', r=True)
    
    mc.window('CompNameWnd', t=' ', wh=(360,56))
    mc.columnLayout()
    mc.rowColumnLayout('BtnLayout', nc=4, cw=((1, 90), (3, 89), (2, 89), (4, 90)))
    mc.showWindow()
    Spine()
    Arm()
    Leg()
    mc.text(l='', p='BtnLayout')
    ThumbFin()
    IndexFin()
    MiddleFin()
    PinkeyFin()
    
    
if __name__ == '__main__': setupRename()
