import json
from functools import partial
import maya.cmds as mc
import maya.mel as mel
class latticeWeightTool(object):
    def __init__(self):

        if mc.window('latticeWeiWnd', ex=True): mc.deleteUI('latticeWeiWnd', wnd=True)
        if mc.windowPref('latticeWeiWnd', ex=True): mc.windowPref('latticeWeiWnd', r=True)
        
        mc.window('latticeWeiWnd', wh=(300, 30), t='Lattice Weights')
        mc.columnLayout()
        mc.rowColumnLayout(nc=2, cw=((1,149), (2,149)))
        mc.button(h=26, l='Save', c=partial(self.SaveWeight))
        mc.button(l='Load', c=partial(self.LaodWeight))
        mc.showWindow('latticeWeiWnd')



    def SaveWeight(self, Unuse):
        FileFullpath = mc.fileDialog2(ff=("JSON Files (*.json)")) 
        if FileFullpath == None:return
        latice = mc.ls(sl=True)
        latticePT = mc.lattice(latice[0], q=True, dv=True)
        
        SkinUseDt = {}
        SkinUseDt['skinNode'] = mel.eval('findRelatedSkinCluster ' + latice[0])
        SkinUseDt['skinJoints'] = mc.skinCluster(latice[0], q=True, inf=True)


        for x in range(latticePT[0]):
            for y in range(latticePT[1]):
                for z in range(latticePT[2]):
                    Pts = '%s.pt[%d][%d][%d]' %(latice[0], x, y, z)
                    weightList = mc.skinPercent(SkinUseDt['skinNode'], Pts, q=True, v=True)
                    SkinUseDt.setdefault('weightList', {})['pt[%d][%d][%d]' %(x, y, z)] = weightList
        
        
        f = open(FileFullpath[0], mode='w')
        json.dump(SkinUseDt, f, indent=2)
        f.close()    
        print '# Result:  weight was saved to  ->   %s ' %FileFullpath[0],
    
    
    def LaodWeight(self, Unuse):
        FileFullpath = mc.fileDialog2(fm=1, ff=("JSON Files (*.json)"))
        if FileFullpath == None:return
        
        f = open(FileFullpath[0], mode='r')
        fileDt = json.load(f)
        f.close()
        
        latice = mc.ls(sl=True)
        skinNode = mel.eval('findRelatedSkinCluster ' + latice[0])
        for pt, Weilist in fileDt['weightList'].iteritems():
            mc.skinPercent(skinNode, '%s.%s'%(latice[0], pt), tv=zip(fileDt['skinJoints'], Weilist))
        
        print '#   Result:   weight Read Final! ',    
#------------------------------------------------------------------------------------------------
if __name__ == '__main__':latticeWeightTool()
