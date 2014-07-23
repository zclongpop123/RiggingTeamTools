import maya.cmds as cmds

def RemoveUVWasteNode():
    cmds.select(hierarchy=True)
    sels = cmds.ls(selection=True, long=True)
    for sel in sels:
        obj = sel
        if (cmds.nodeType(sel) == 'mesh'):
            trans = cmds.listRelatives(sel, p=True, f=True)
            obj = trans[0]
        if ((cmds.nodeType(obj) == 'transform') and delUVTransferAttributesNode(obj)):
            pass




def delUVTransferAttributesNode(obj):
    SH = cmds.listRelatives(obj, s=True, f=True, ni=True, type='mesh')
    allSH = cmds.listRelatives(obj, s=True, f=True, type='mesh')
    orgSH = []
    deformers = []
    inputType    = ('skinCluster', 'blendShape', 'ffd', 'wrap', 'cluster', 'nonLinear', 'sculpt', 'jiggle', 'wire', 'groupParts', 'groupId')
    deformerType = ('skinCluster', 'blendShape', 'ffd', 'wrap', 'cluster', 'nonLinear', 'sculpt', 'jiggle', 'wire')
    hist = cmds.listHistory(obj)
    for histIt in hist:
        ListNode = cmds.nodeType(histIt)
        if (deformerType.count(ListNode) and deformers.append(histIt)):
            pass

    for itSH in allSH:
        if (cmds.getAttr((itSH + '.intermediateObject')) and (cmds.listConnections(itSH, d=False) == None)):
            orgSH.append(itSH)

    if (len(SH) == 1):
        imputNode = cmds.listConnections((SH[0] + '.inMesh'), d=False, sh=True)
        if (len(imputNode) and (inputType.count(cmds.nodeType(imputNode)) != True)):
            if len(orgSH):
                mesh = cmds.createNode('mesh')
                for orgIt in orgSH:
                    cmds.connectAttr((SH[0] + '.outMesh'), (mesh + '.inMesh'), f=True)
                    cmds.refresh()
                    cmds.disconnectAttr((SH[0] + '.outMesh'), (mesh + '.inMesh'))
                    cmds.polyTransfer(orgIt, v=False, vc=False, uv=True, ao=mesh)
                    transfer = cmds.listConnections(orgIt, d=False)
                    NewOrg = cmds.listConnections((transfer[0] + '.inputPolymesh'), d=False, sh=True)
                    cmds.delete(NewOrg)

                if cmds.delete(cmds.listRelatives(mesh, p=True, f=True)):
                    pass
                
                n = True
                while n:
                    inputNode = cmds.listConnections((SH[0] + '.inMesh'), d=False, sh=True)
                    if (len(inputNode) is None):
                        n = False
                        break
                    breakWhile = []
                    selINode = cmds.nodeType(inputNode)
                    breakWhile.append(str(selINode))
                    if (inputType.count(breakWhile) == True):
                        n = False
                        break
                    cmds.delete(inputNode)
                    n = False