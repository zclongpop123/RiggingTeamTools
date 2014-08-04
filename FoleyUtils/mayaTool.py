#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Tue, 08 Jul 2014 14:46:14
#=============================================
import re, struct
import maya.cmds, maya.mel, pymel.core, maya.OpenMaya, maya.OpenMayaAnim
import nameTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def undo_decorator(func):
    '''
    To fix maya can't undo bug..
    '''
    def doIt(*args, **kvargs):
        maya.cmds.undoInfo(openChunk=True)
        func(*args, **kvargs)
        maya.cmds.undoInfo(closeChunk=True)
    return doIt



#==============================================
#                  General                    #
#==============================================

def getChildren(dagObject, dagType='transform'):
    '''
    Give a root dagNode name, find all children to return..
    '''
    L = [dagObject]
    for O in maya.cmds.listRelatives(dagObject, c=True, type=dagType, path=True) or []:
        L.append(O)
        
        ccd = maya.cmds.listRelatives(O, c=True, type=dagType, path=True)
        if ccd:
            for o in ccd:
                L.extend(getChildren(o))
        else:
            pass
    return L




def getParents(obj):
    '''
    Get object's parent list..
    '''
    parents = []
    if not maya.cmds.objExists(obj):
        return parents
    
    pnt = maya.cmds.listRelatives(obj, p=True, path=True)
    if pnt:
        parents.extend(pnt)
        parents.extend(getParents(pnt[0]))

    return parents




def getParentByType(obj, typ='transform'):
    '''
    return object type by input type..
    '''
    for pnt in getParents(obj):
        if maya.cmds.nodeType(pnt) == typ:
            return pnt


#==============================================
#                    Shapes                   #
#==============================================


def parentShape(*args):
    '''
    Parent shapes to last one..
    '''
    if len(args) < 2:
        return
    shapes = maya.cmds.listRelatives(args[:-1], s=True, path=True) or []
    maya.cmds.parent(shapes, args[-1], s=True, r=True)
    maya.cmds.delete(args[:-1])



def conformShapeNames(transform):
    '''
    pSphere1 -> pSphere1Shape, pSphere1Shape1, pSphere1Shape2..
    '''
    shapes = maya.cmds.listRelatives(transform, s=True, path=True) or []
    for shape in shapes:
        maya.cmds.rename(shape, nameTool.compileMayaObjectName('%sShape'%transform))



#==============================================
#                    History                  #
#==============================================


def getHistoryByType(geometry, historyType):
    '''
    Return object history by type..
    '''
    historys = maya.cmds.listHistory(geometry, pdo=True)
    typedHistory = maya.cmds.ls(historys, type=historyType)
    typedHistory = {}.fromkeys(typedHistory).keys()    
    
    return typedHistory




def findDeformer(geometry):
    '''
    Return object's deformers..
    '''
    deformers = maya.mel.eval('findRelatedDeformer("%s")'%geometry)
    return deformers




def findSkinCluster(geometry):
    '''
    Return object's skinCluster node..
    '''
    skinCluster = maya.mel.eval('findRelatedSkinCluster("%s")'%geometry)
    return skinCluster



#==============================================
#                  blendShape                 #
#==============================================



def getBlendShapeInfo(blendShape):
    '''
    Return blendShape's ID and attributes dict..
    '''
    attribute_dict = {}
    if maya.cmds.nodeType(blendShape) != 'blendShape':
        return attribute_dict
    
    infomations =  maya.cmds.aliasAttr(blendShape, q=True)
    for i in range(len(infomations)):
        if i % 2 == 1:continue
        bs_id   = infomations[i + 1]
        bs_attr = infomations[i + 0]
        bs_id = int(re.search('\d+', bs_id).group())
        attribute_dict[bs_id] = bs_attr

    return attribute_dict




def getBlendShapeAttributes(blendShape):
    '''
    Return blendShape attributes..
    '''
    attribute_dict = getBlendShapeInfo(blendShape)
    bs_idList = attribute_dict.keys()
    bs_idList.sort()
    
    attributes = [attribute_dict.get(i,'')  for i in bs_idList]
    return attributes





def getBlendShapeInputGeomTarget(blendShape):
    '''
    Return blendShape's inputTargentGeometry ( targent connected attr ) attributes..
    '''
    igt_dict = {}

    attributes = ' '.join(maya.cmds.listAttr(blendShape, m=True))
    for old, new in (('inputTargetGroup', 'itg'),
                      ('inputTargetItem',  'iti'),
                      ('inputGeomTarget',  'igt'),
                      ('inputTarget',      'it')):
        attributes = attributes.replace(old, new)
        
    igt_attributes = re.findall('it\[0\]\.itg\[\d+\]\.iti\[\d{4,}\]\.igt', attributes)
    for attr in igt_attributes:
        index = re.search('(?<=itg)\[\d+\]', attr).group()
        igt_dict[int(index[1:-1])] = attr

    return igt_dict





def getActiveTargets(blendShape):
    '''
    Get opend blendShape's ids..
    '''
    targents = []
    for weightid, attr in getBlendShapeInfo(blendShape).iteritems():
        if maya.cmds.getAttr('%s.%s'%(blendShape, attr)) == 1:
            targents.append(weightid)
    return targents





def getSetsMembers(Sets):
    '''
    Get all of sets children..
    '''
    args = []
    
    members = maya.cmds.sets(Sets, q=True)
    if maya.cmds.sets(members, q=True):
        args.extend(members)
        args.extend(getSetsMembers(members))
    else:
        args.extend(members)

    return args



#==============================================
#                  Control                    #
#==============================================

def makeControl(side, nameSpace, count):
    '''
    Make control with Hierarchy..
    '''
    types = ('ctl', 'cth', 'ctg', 'grp')
    control = []
    for t in types:
        controlName = nameTool.compileMayaObjectName('_'.join((side.upper(), nameSpace, t, str(count))))
        if len(control) == 0:
            control.append(maya.cmds.group(em=True, n=controlName))
        else:
            control.append(maya.cmds.group(control[-1], n=controlName))
    return control
        




def getControlData(control):
    '''
    Return control shape data by dict..
    '''
    shapes = maya.cmds.listRelatives(control, s=True, path=True)
    if not shapes:return
    
    data = {'control':control, 'shapeData':{}}
    for shape in shapes:
        if maya.cmds.nodeType(shape) != 'nurbsCurve':
            continue
        #- get data
        positions = maya.cmds.xform('%s.cv[:]'%shape, q=True, ws=True, t=True)
        positions = [(positions[i+0], positions[i+1], positions[i+2]) for i in range(0, len(positions), 3)]
        data['shapeData'][shape] = positions
        
    return data





def setControlData(data):
    '''
    Input control data, set control shape data..
    '''
    if not maya.cmds.objExists(data.get('control', '#')):
        return
    
    for shape, postions in data['shapeData'].iteritems():
        if not maya.cmds.objExists(shape):
            continue
        if maya.cmds.nodeType(shape) != 'nurbsCurve':
            continue
        #- set control data
        for i, ps in enumerate(postions):
            maya.cmds.xform('%s.cv[%d]'%(shape, i), ws=True, t=ps)
            


#==============================================
#                  Curve                      #
#==============================================


def attachToCurve(curve, attachOBJ, uValue, upperOBJ=None, uValuezerotoOne=True):
    '''
    Attact an object on a curve..
    '''
    CusShape = maya.cmds.listRelatives(pathCus, s=True, type='nurbsCurve')
    motionpathNode = maya.cmds.createNode('motionPath')
    
    # connect curve and motionpath node..
    maya.cmds.connectAttr(CusShape[0] + '.worldSpace[0]', motionpathNode + '.geometryPath')
    
    # connect motionpath node and object..
    for outAttr, inAttr in (('.rotateOrder', '.rotateOrder'),('.rotate', '.rotate'),('.allCoordinates', '.translate')):
        maya.cmds.connectAttr(motionpathNode + outAttr, attactOBJ + inAttr)

    # set Uvalue..
    maya.cmds.setAttr(motionpathNode + '.uValue', uValue)
    
    # set offset..
    if uValuezerotoone:
        maya.cmds.setAttr(motionpathNode + '.fractionMode', 1)

    
    if not UpperOBJ:
        return motionpathNode
    # set upvector..
    maya.cmds.setAttr(motionpathNode + '.worldUpType', 1)
    maya.cmds.connectAttr(UpperOBJ   + '.worldMatrix[0]', motionpathNode + '.worldUpMatrix')
    maya.cmds.setAttr(motionpathNode + '.frontAxis', 0)
    maya.cmds.setAttr(motionpathNode + '.upAxis', 2)
    return motionpathNode




def findClosestPointOnCurve(curve, point=[0.0, 0.0, 0.0]):
    '''
    Input a curve and a position, return a parameter value on curve..
    '''
    # Get the point as an MPoint.
    p = maya.OpenMaya.MPoint(*point)
    
    # I'm using pymel to get the curve because it's easier to pass to the API.
    crv = pymel.core.PyNode(curve)
    
    # We need to create a pointer to capture the parameter value.
    u_util = maya.OpenMaya.MScriptUtil(0.0)
    u_ptr = u_util.asDoublePtr()

    # Create the MFn class passing in the nurbsCurve.
    mfn = maya.OpenMaya.MFnNurbsCurve(crv.__apiobject__())
    
    # Get the closest point on curve. 
    mfn.closestPoint(p, u_ptr, 0.001, maya.OpenMaya.MSpace.kWorld)
                    
    return u_util.getDouble(u_ptr)



#==============================================
#                 Skin weights                #
#==============================================


def getSkinWeightsData(geometry):
    """
    Export skinWeights data by a dict..
    """
    skindict = {'geometry':geometry}
    
    skincluster = findSkinCluster(geometry)
    if not skincluster:
        return skindict
    
    # get skin cluster
    selection = maya.OpenMaya.MSelectionList()
    selection.add(skincluster)
    clusterobject = maya.OpenMaya.MObject()
    selection.getDependNode(0, clusterobject)
    skin = maya.OpenMayaAnim.MFnSkinCluster(clusterobject)

    # get influences
    influences = maya.OpenMaya.MDagPathArray()
    infcount = skin.influenceObjects(influences)

    strinfluences = []
    for i in range(infcount):
        infpath = influences[i]
        strinfluences.append(infpath.partialPathName())

    # get dagpath to skinned object
    skinpath = maya.OpenMaya.MDagPath()
    skin.getPathAtIndex(0, skinpath) # hardcoded to first element - should iterate

    skindict['influences'] = strinfluences
    pointdata = {}

    it = maya.OpenMaya.MItGeometry(skinpath)
    while not it.isDone(): # step through vertices

        weightarray = []

        comp = it.currentItem() # get vertex
        db = maya.OpenMaya.MDoubleArray() # place holder

        # get skin weights
        for i in range(infcount): # step through influences
            skin.getWeights(skinpath, comp, i, db)
            weightarray.append(db[0])
        pointdata[it.index()] = weightarray

        it.next()


    skindict['weightData'] = pointdata
    skindict['posiData']   = getMeshPositionData(geometry)
    
    return skindict
    





def setSkinWeightsData(skindict):
    '''
    Import skinWeights data for a geometry..
    '''
    geometry   = skindict.get('geometry',  '*')
    influences = skindict.get('influences', [])
    weightData = skindict.get('weightData', {})
    
    #- check influecens
    lostInfluecens = []
    for inf in influences:
        if not maya.cmds.objExists(inf):
            lostInfluecens.append(inf)
    
    if lostInfluecens:
        print 'Error: influecens lost ( %s )...'%' '.join(lostInfluecens)
        return False
    
    #- check geometry
    if not maya.cmds.objExists(geometry):
        print 'Error: geometry lost ( %s )...'%geometry
        return False

    #- set weights data
    skincluster = maya.cmds.skinCluster(influences, geometry, sm=2, tsb=True, nw=1)[0]
    for vtx, weights in weightData.iteritems():
        for i, weight in enumerate(weights):
            maya.cmds.setAttr('%s.wl[%s].w[%d]'%(skincluster, vtx, i), weight)
    
    return True



#==============================================
#                   Polygon                   #
#==============================================



def getMeshPositionData(geometry, precision=6):
    '''
    Return mesh postions and vtx id in dict..
    Exp:{ 
          0 : 'ffed2a41208043c0ca0a7141',
          1 : 'fff2a21fb3232142067cb2c1'
        }
    '''
    if not maya.cmds.objExists(geometry):
        return
    
    positions = maya.cmds.xform('%s.vtx[:]'%geometry, q=True, ws=True, t=True)
    data = {}
    vtx  = 0
    for i in range(0, len(positions), 3):
        posi_hex = struct.pack('fff', round(positions[i], precision), round(positions[i+1], precision), round(positions[i+2], precision)).encode('hex')
        data[vtx] = posi_hex
        vtx += 1
    return data