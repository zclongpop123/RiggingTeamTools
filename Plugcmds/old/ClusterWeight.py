import re
import maya.cmds as mc
import maya.mel as mel


def LoadOBJ(FLDname):
    if len(mc.ls(sl=True)) == 0:
        mc.textField(FLDname, e=True, tx='')
    else:
        mc.textField(FLDname, e=True, tx=mc.ls(sl=True)[0])


def SelectOBJ(FLDname):
    OBJname =  mc.textField(FLDname, q=True, tx=True)
    if OBJname == '':
        pass
    else:
        mc.select(OBJname)



def TransWeightToJoint():

    ModelName = mc.textField('ClusterModelFLD', q=True, tx=True)
    SkinModel = mc.textField('SkinModelFLD', q=True, tx=True)
    ClusterName =  mc.textField('ClusterNameFLD', q=True, tx=True)
    JointName =  mc.textField('JointNameFLD', q=True, tx=True)
    #- get the cluster Node Name..
    if mc.nodeType(ClusterName) == 'transform':
        ClusterName = mc.listConnections(ClusterName, t='cluster')[0]
    else:
        pass

    #- get the Model Id and connect groupparts
    ModeID = mc.listRelatives(mc.cluster(ClusterName, q=True, g=True), p=True).index(ModelName)
    GroupParts = mc.connectionInfo(ClusterName + '.input[%d].inputGeometry'%ModeID, sfd=True).split('.')[0]


    #- get Inflution Vts
    Points = ['%s.%s'%(ModelName,Vtx)  for Vtx in mc.getAttr(GroupParts + '.inputComponents')]


    #- get Cluster Value
    WeightDT = {}
    for VVtx in mc.ls(Points, fl=True):
        VtxID = re.search('(?<=\[)\d+(?=\])', VVtx).group()
        WeightValue = mc.percent(ClusterName, VVtx,  q=True, v=True)
        WeightDT[VtxID] = WeightValue[0]

    #- get SkinNode Name
    SkinClusterNode = mel.eval('findRelatedSkinCluster ' + SkinModel)


    #- Remove Joint weights
    ModelVts = mc.polyEvaluate(SkinModel, v=True)
    mc.skinPercent(SkinClusterNode, '%s.vtx[0:%s]'%(SkinModel, ModelVts), tv=(JointName, 0))

    #- set Weight Value
    for VtxID, WeightV in WeightDT.iteritems():
        mc.skinPercent(SkinClusterNode, '%s.vtx[%s]'%(SkinModel, VtxID), tv=(JointName, WeightV))



def TransWeightToCluster():
    ModelName = mc.textField('ClusterModelFLD', q=True, tx=True)
    SkinModel = mc.textField('SkinModelFLD', q=True, tx=True)
    ClusterName =  mc.textField('ClusterNameFLD', q=True, tx=True)
    JointName =  mc.textField('JointNameFLD', q=True, tx=True)
    #- get the cluster Node Name..
    if mc.nodeType(ClusterName) == 'transform':
        ClusterName = mc.listConnections(ClusterName, t='cluster')[0]
    else:
        pass

    #- get SkinNode Name
    SkinClusterNode = mel.eval('findRelatedSkinCluster ' + SkinModel)

    #- set Value
    ModelVts = mc.polyEvaluate(SkinModel, v=True)
    JointID = mc.skinCluster(SkinClusterNode, q=True, inf=True).index(JointName)
    for i in range(ModelVts):
        SkinWeight = mc.skinPercent(SkinClusterNode, '%s.vtx[%s]'%(SkinModel, i), q=True, v=True)[JointID]
        mc.percent(ClusterName, '%s.vtx[%s]'%(ModelName, i), v=SkinWeight)


#if __name__ == "__main__":TransWeight('pPlane1', 'cluster1Handle', 'joint1')
