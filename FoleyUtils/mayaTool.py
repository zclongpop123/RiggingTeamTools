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


def getSkinWeightsData(skincluster):
    """Spit out a dictionary containing the skin data per vertex of a dagnode."""

    skindict = {}

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


    skindict['weightData']   = pointdata
    
    return skindict
    





def importSkin(skindict, geo, count=0, mirrored=False, **kwargs):
    """Import and apply skin weighting from json file."""
    
    influences = skindict['influences']
    pointdata  = skindict['pointdata']
    notfound   = []
    tmp        = []
    
    for inf in influences:
        if mirrored:
            if inf[0] == 'R':
                inf = 'L%s' % inf[1:]
            elif inf[0] == 'L':
                inf = 'R%s' % inf[1:]
            tmp.append(inf)

        if not maya.cmds.objExists(inf): notfound.append(inf)

    # switch around the influences
    if mirrored: influences = tmp

    # test influence existence
    if notfound:
        msg = 'Influences Not Found For: %s\n' % geo
        for nf in notfound:
            msg = '%s%s\n' % (msg, nf)

        return False

    # test skin cluster existence
    skincluster = findSkinCluster(geo)
    
    if skincluster: maya.cmds.delete(skincluster)
    #if not skincluster:
        
    # ensure geo is visible
    shps   = maya.cmds.listRelatives(geo, s=True)
    geosrc = maya.cmds.listConnections('%s.v' % geo, s=True, d=False, p=True)
    
    if geosrc:
        maya.cmds.disconnectAttr(geosrc[0], '%s.v' % geo)
        maya.cmds.setAttr('%s.v' % geo, 1)
    for shp in shps:
        shpsrc = maya.cmds.listConnections('%s.v' % shp, s=True, d=False, p=True)
        if shpsrc:
            maya.cmds.disconnectAttr(shpsrc[0], '%s.v' % shp)
            maya.cmds.setAttr('%s.v' % shp, 1)
    # apply
    ###################################################################
    # hack - need to replace with storing of skin position in JSON file
    ###################################################################

    bShapes = None
    shape = maya.cmds.listRelatives(geo, ad=True, s=True, path=True)
    if shape:
        bShapes = maya.cmds.listConnections(shape[0], s=True, d=False, p=False, type='blendShape')

#         if 'jacket' in geo:
#             skincluster = maya.cmds.skinCluster(influences, geo, sm=2, foc=False, tsb=True, nw=2)[0]
#         elif bShapes and maya.cmds.objExists('%s.frontOfChain' % bShapes[0]): # frontOfChain tag for corrective blendShapes
#             skincluster = maya.cmds.skinCluster(influences, geo, sm=2, foc=False, tsb=True, nw=2)[0]
#         else:
#             skincluster = maya.cmds.skinCluster(influences, geo, sm=2, foc=True, tsb=True, nw=2)[0]

    VALID_ARGS = [
        ('af', 'after'),
        ('ar', 'afterReference'),
        ('bf', 'before'),
        ('ex', 'exclusive'),
        ('foc', 'frontOfChain'),
        ('par', 'parallel')
        ]

    skinArgs = dict()

    if not kwargs:
        skinArgs['foc'] = False  # 2013.12.5 change True -> False (changlong)
    else:
        for item in VALID_ARGS:
            for i in item:
                if i in kwargs:
                    skinArgs[i] = kwargs[i]
                    break

    skincluster = maya.cmds.skinCluster(influences, geo, sm=2, tsb=True, nw=1, **skinArgs)[0]

    # reconnect
    if geosrc: maya.cmds.connectAttr(geosrc[0], '%s.v' % geo)
    if shpsrc: maya.cmds.connectAttr(shpsrc[0], '%s.v' % shp)
    
    # Check to see that the influences are actually attached to the skinCluster.
    invalidInfs = list()
    skinInfluences = maya.cmds.skinCluster(skincluster, q=True, inf=True)

    for influence in influences:
        if not influence in skinInfluences: invalidInfs.append(influence)

    if invalidInfs:
        msg = str()
        for inf in invalidInfs:
            msg += '%s is not an influence object for skinCluster %s\n' % (inf, skincluster)

        return False

    # We need to know what we're applying the weights too so we can get the
    # component identifier correct.
    cidDict = {
        'lattice':'pt',
        'mesh':'vtx',
        'nurbsCurve':'cv',
        'nurbsSurface':'cv'
        }

    cid = cidDict[maya.cmds.objectType(maya.cmds.skinCluster(skincluster, q=True, g=True)[0])]


    # Get the size of the weight array.
    arraySize = maya.cmds.getAttr('%s.weightList' % skincluster, size=True)

    # Start the progress bar.
    gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')
    maya.cmds.progressBar(gMainProgressBar, e=True, bp=True, ii=True, st='Applying weights to %s' % geo, max=arraySize)

    # Apply the weights.
#     for i in range(arraySize):
    for point in pointdata:
        #  Increase the progress bar.
        if maya.cmds.progressBar(gMainProgressBar, q=True, ic=True): break
        maya.cmds.progressBar(gMainProgressBar, e=True, s=1)

#         try: point = pointdata[unicode(i)]
#         except KeyError:
#             rigUtils.log('Mismatching number of verts for %s' % geo, 'w')
#             break
#
#         weights     = point['skinweights']
#         blendweight = point['blendweight']

        weights     = pointdata[point]['skinweights']
        blendweight = pointdata[point]['blendweight']

        for j, value in enumerate(weights):
#             maya.cmds.setAttr('%s.weightList[%d].weights[%d]' % (skincluster, i, j), value)
            maya.cmds.setAttr('%s.weightList[%s].weights[%s]' % (skincluster, point, j), value)

#         maya.cmds.setAttr('%s.blendWeights[%d]' % (skincluster, i), blendweight)
        maya.cmds.setAttr('%s.blendWeights[%s]' % (skincluster, point), blendweight)

    # Stop the progress bar.
    maya.cmds.progressBar(gMainProgressBar, e=True, ep=True)



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