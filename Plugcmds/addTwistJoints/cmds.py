#=================================
# author: changlong.zang
#   date: 2014-03-12   
#=================================
import os, inspect, re, string, json, tempfile, shutil
import maya.cmds as mc


#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

def getScriptPath():
    filePath = inspect.getfile(inspect.currentframe())
    return os.path.dirname(filePath)


#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
def attachToCurve(Obj, curve, parameter):
    CusShape = mc.listRelatives(curve, s=True, path=True, type='nurbsCurve')
    motionpathNode = mc.createNode('motionPath')
    
    #- connect curve and motionpath node..
    mc.connectAttr(CusShape[0] + '.worldSpace[0]', motionpathNode + '.geometryPath')
    
    #- connect motionpath node and object..
    for outAttr, inAttr in (('rotateOrder', 'rotateOrder'),('rotate', 'rotate'),('allCoordinates', 'translate')):
        mc.connectAttr('%s.%s'%(motionpathNode, outAttr), '%s.%s'%(Obj, inAttr))        
    
    #- set Uvalue..
    mc.setAttr(motionpathNode + '.fractionMode', 1)
    mc.setAttr(motionpathNode + '.uValue', parameter)

    #-
    multiNode = mc.createNode('multDoubleLinear')
    mc.setAttr('%s.input2'%multiNode, parameter, l=True)
    mc.connectAttr('%s.output'%multiNode, '%s.frontTwist'%motionpathNode)

    return multiNode


def addUpObject(Obj, UpObj):
    motionpathNodes = mc.listConnections(Obj, s=1, t='motionPath')
    if not motionpathNodes:return
    #- - - - - - - - - - - - - - - - - - - - - - - - - -
    mc.setAttr(motionpathNodes[0] + '.worldUpType', 1)
    mc.connectAttr(UpObj + '.worldMatrix[0]', motionpathNodes[0] + '.worldUpMatrix')
    mc.setAttr(motionpathNodes[0] + '.frontAxis', 0)
    mc.setAttr(motionpathNodes[0] + '.upAxis', 1)    



def buideGuide(character, version, componentData):
    #- remove all guides -
    for f in mc.file(q=True, r=True):
        if 'guide.ma' in f:
            mc.file(f, rr=True)
    
    #- import published guides -
    guidefile = getAssetVersionedFile(ROOT_ASSET_PATH, character, 'body', 'twistJointguide', version)
    if os.path.isfile(guidefile):
        mc.file(guidefile, i=True, pr=True)
    ExistsnameSpace = [mc.file(f, q=True, ns=True) for f in mc.file(q=True, r=True) if 'guide.ma' in f]
   
    #- builde component guide -
    guideFile = os.path.join(getScriptPath(), 'guide.ma')
    for data in componentData:
        if data[0] in ExistsnameSpace:
            mc.setAttr('%s:link_start_gui.jointCount'%data[0] , data[1])
            if mc.objExists('%s:link_start_gui.jointCount'%data[0].replace('L_', 'R_')):
                mc.setAttr('%s:link_start_gui.jointCount'%data[0].replace('L_', 'R_'), data[1])
            continue

        mc.file(guideFile, r=True, ns=data[0])
        mc.setAttr('%s:link_start_gui.jointCount'%data[0] , data[1])
        
        if data[2] == False:continue
        
        mirNameSpace = data[0].replace('L_', 'R_')
        if mirNameSpace in ExistsnameSpace:continue
        
        mc.file(guideFile, r=True, ns=mirNameSpace)
        mc.setAttr('%s:link_start_gui.jointCount'%mirNameSpace, data[1])
    
    #- read component nameSpaces -
    componentNS = []
    for x in componentData:
        componentNS.append(x[0])
        if x[2]:componentNS.append(x[0].replace('L_', 'R_'))
        
    #- remove more guides -
    for f in mc.file(q=True, r=True):
        nameSpace = mc.file(f, q=True, ns=True) 
        if nameSpace in componentNS:continue
        
        mc.file(f, rr=True)


    
def mirrorGuide(src='L_', dst='R_'):
    transforms = ' '.join(mc.ls(type='transform'))
    guides = re.findall('%s\S+link_\w+_gui'%src, transforms)
    guides = dict().fromkeys(guides).keys()
    
    for gui in guides:
        targentGuide = gui.replace(src, dst)
        if not mc.objExists(targentGuide):continue
        
        posi = mc.xform(gui, q=True, ws=True, t=True)
        mc.xform(targentGuide, ws=True, t=(posi[0] * -1, posi[1], posi[2]))



def buildeCurve(*args):
    positions = [mc.xform(x, q=True, ws=True, t=True) for x in args]
    Curve = mc.curve(d=1, p=positions)
    mc.rebuildCurve(Curve, ch=0, s=3, d=3)
    return Curve




def buidleUpCurve(startOBJ, endObj, upOBJ):
    startPosition = mc.xform(startOBJ, q=True, ws=True, t=True) 
    endPosition   = mc.xform(endObj,   q=True, ws=True, t=True) 
    upPosition    = mc.xform(upOBJ,    q=True, ws=True, t=True) 
    offsetVector  = (upPosition[0] - startPosition[0]) * 0.25, (upPosition[1] - startPosition[1]) * 0.25, (upPosition[2] - startPosition[2]) * 0.25
    
    startPosition = (startPosition[0] + offsetVector[0]), (startPosition[1] + offsetVector[1]), (startPosition[2] + offsetVector[2])
    endPosition   = (endPosition[0]   + offsetVector[0]), (endPosition[1] +   offsetVector[1]), (endPosition[2] +   offsetVector[2])
    
    Curve = mc.curve(d=1, p=(startPosition, endPosition))
    mc.rebuildCurve(Curve, ch=0, s=3, d=3)
    return Curve



def buildeRig(keepGuide):
    guides = {}
    for f in mc.file(q=True, r=True):
        guides[mc.file(f, q=True, ns=True)] = f
        
    for Ns, fpath in guides.iteritems():
        if not mc.objExists('%s:link_start_gui'%Ns):continue
        #-  -*-  -*-  -*-  -*-  -*-  
        Rig(Ns)
        #-  -*-  -*-  -*-  -*-  -*-  
        if keepGuide:continue
        mc.file(fpath, rr=True)
    


def Rig(nameSpace):
    
    #- get guides -
    guides = ['%s:link_start_gui'%nameSpace, '%s:link_end_gui'%nameSpace, '%s:link_up_gui'%nameSpace]
    
    #- make curve -
    pathCurve = buildeCurve(guides[0], guides[1])
    
    #- make up curve -
    upvectorCurve = buidleUpCurve(*guides)
    
    #- make Joints and locators-
    Joints = []
    locators = []
    multiNodes = []
    counts = mc.getAttr('%s.jointCount'%guides[0])
    for i in range(counts):
        #- 1 create 
        Joints.append(mc.createNode('joint'))
        locators.append(mc.spaceLocator(p=(0,0,0))[0])
        
        #- 2 
        parameter = (((float(i + 1) - 0) / (counts + 1 - 0)) * (1 - 0)) + 0
        
        #- 3 attact to curve
        multiNodes.append(attachToCurve(Joints[-1], pathCurve, parameter))
        attachToCurve(locators[-1], upvectorCurve, parameter)
    
        #- 4 connect object up
        addUpObject(Joints[-1], locators[-1])
    
    
    #- add rig Joins -
    rigJoints = []
    for i in range(4):
        rigJoints.append(mc.createNode('joint'))
        #- move
        position = mc.pointOnCurve(pathCurve, pr= 1.0 / 3 * i)
        mc.move(position[0], position[1], position[2], rigJoints[-1], a=True)
        #- orient
        mc.delete(mc.orientConstraint(Joints[0], rigJoints[-1]))
    
    #- bind Curve
    mc.skinCluster(rigJoints, pathCurve)    
    mc.skinCluster(rigJoints, upvectorCurve)

    #- rig rigJoints -
    controlLst = []
    for jnt in rigJoints:
        
        #- make control
        controls = [mc.createNode('transform')  for i in range(4)]
        for i in range(len(controls) - 1):
            mc.parent(controls[i], controls[i+1])
        controlLst.append(controls)
        
        #- match positions, parent Joint
        mc.delete(mc.parentConstraint(jnt, controls[-1]))
        mc.parent(jnt, controls[0])
        
        #-add Shape
        circle = mc.circle(nr=(1,0,0), ch=0)
        mc.parent(mc.listRelatives(circle, s=True, path=True), controls[0], r=True, s=True)
        mc.delete(circle)
  
        
    #- Constraint control
    appLocators = []
    for controls in controlLst:
        appLocators.append(mc.spaceLocator(p=(0,0,0))[0])
        mc.delete(mc.parentConstraint(controls[0], appLocators[-1]))
        mc.parentConstraint(appLocators[-1], controls[-2])

    #- add def
    mc.addAttr(appLocators[-1], sn='IKFKSwitch', min=0, max=1, dv=0, k=True)
    mc.addAttr(appLocators[-1], sn='fkRotate', dv=0, k=True)
    mc.addAttr(appLocators[-1], sn='ikRotate', dv=0, k=True)
    
    blendNode = mc.createNode('blendTwoAttr')
    mc.connectAttr('%s.IKFKSwitch'%appLocators[-1], '%s.ab'%blendNode)
    mc.connectAttr('%s.fkRotate'%appLocators[-1], '%s.input[0]'%blendNode)
    mc.connectAttr('%s.ikRotate'%appLocators[-1], '%s.input[1]'%blendNode)
    
    for md in multiNodes:
        mc.connectAttr('%s.output'%blendNode, '%s.input1'%md)
    
    #-- comp hery --
    curveGrp   = mc.group(pathCurve, upvectorCurve)
    jointGrp   = mc.group(Joints) 
    locatorGrp = mc.group(locators)    
    controlGrp = mc.group([L[-1] for L in controlLst])
    RootGrp    = mc.group(curveGrp, jointGrp, locatorGrp, controlGrp)
    
    #-- clean scene --
    mc.hide(curveGrp, locatorGrp, rigJoints)
    
    #-* rename *-
    
    #- groups -
    curveGrp   = mc.rename(curveGrp,   '%s_cusg_0'%nameSpace)
    jointGrp   = mc.rename(jointGrp,   '%s_jntg_0'%nameSpace)
    locatorGrp = mc.rename(locatorGrp, '%s_locg_0'%nameSpace)
    controlGrp = mc.rename(controlGrp, '%s_ctlg_0'%nameSpace)
    RootGrp    = mc.rename(RootGrp,    '%s_setg_0'%nameSpace)
    
    #- joints -
    for i,jnt in enumerate(Joints):
        Joints[i] = mc.rename(jnt, '%s_bnd%s_0'%(nameSpace, string.uppercase[i]))
    
    #- locators -
    for i,loc in enumerate(locators):
        locators[i] = mc.rename(loc, '%s_loc%s_0'%(nameSpace, string.uppercase[i]))    
    
    #- aooLocators -
    for i, loc in enumerate(appLocators):
        appLocators[i] = mc.rename(loc, '%s_apploc%s_0'%(nameSpace, string.uppercase[i]))    
    
    #- rig Joints -
    for i,jnt in enumerate(rigJoints):
        rigJoints[i] = mc.rename(jnt, '%s_ctj%s_0'%(nameSpace, string.uppercase[i]))   

    #- control -
    ctlType = ('ctl', 'ctu', 'cth', 'ctg') 
    for i, ctls in enumerate(controlLst):
        for d, ctl in enumerate(ctls):
            controlLst[i][d] = mc.rename(ctl, '%s%s_%s_0'%(nameSpace, string.uppercase[i], ctlType[d]))   
    
    #- curve -
    pathCurve = mc.rename(pathCurve, '%s_TWbaseCus_0'%nameSpace)    
    upvectorCurve = mc.rename(upvectorCurve , '%s_TWupperCus_0'%nameSpace)    
    

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
ROOT_ASSET_PATH = '//bjserver3/Tank/blinky_bill_movie/assets/rigItem/asset/character'

def getCharacters():
    chracters = [d for d in os.listdir(ROOT_ASSET_PATH) if os.path.isdir(os.path.join(ROOT_ASSET_PATH, d))]
    return chracters
    


def getAssetVersions(assetPath, character, rigType, rigAssetType):
    '''
    return a versions(stringList).
    Example:[ ]
            [001, 002, 003]
            [001, 002, 003, 004, 005, ...]
    '''
    versions = []
    fullPath = os.path.join(assetPath, character, 'rig', rigType, rigAssetType)
    if not os.path.isdir(fullPath):
        return versions
    files = ' '.join(os.listdir(fullPath))
    versions = re.findall('(?<=v)\d+(?=\.)', files)
    versions = {}.fromkeys(versions).keys()
    versions.sort()
    return versions



def getAssetLastVersion(assetPath, character, rigType, rigAssetType):
    '''
    return tbhe last version (string)
    Example: [ ]  -> 000
             [001, 002, 003] -> 003
    '''
    versions = getAssetVersions(assetPath, character, rigType, rigAssetType)
    if len(versions) != 0:
        lasetVersion = versions[-1]
    else:
        lasetVersion = '000'
    return lasetVersion



def getAssetNextVersion(assetPath, character, rigType, rigAssetType):
    '''
    retrun a version (string) last version right
    Example:[ ] -> 001
            [001, 002] -> 003
            [001, 002, 003] -> 004
    '''
    lastVersion = getAssetLastVersion(assetPath, character, rigType, rigAssetType)
    nextVersion = int(lastVersion) + 1
    nextVersion = str(nextVersion).zfill(3)
    return nextVersion



def getAssetVersionedFile(assetPath, character, rigType, rigAssetType, version):
    '''
    return a file path (string) by version
    Example: 001 -> //ASSET_PATH/* * */cranklepot_face_rig_TempLocator_v001.ma
             002 -> //ASSET_PATH/* * */cranklepot_face_rig_TempLocator_v002.ma
    '''
    filePath = ''
    dirPath = os.path.join(assetPath, character, 'rig', rigType, rigAssetType)
    if not os.path.isdir(dirPath): return filePath
    
    for f in os.listdir(dirPath):
        if re.search(version, f):
            filePath = os.path.join(dirPath, f)
            break
        
    filePath = filePath.replace('\\', '/')
    return filePath
        


def getNewVersionFile(assetPath, character, rigType, rigAssetType, fileFormat):
    '''
    return a file path (string).
    Example: blinky_face_rig_skeletonGuide_v003.ma
             blinky_body_rig_layout_v001.json
    '''
    lastVersion = getAssetLastVersion(assetPath, character, rigType, rigAssetType)
    newVersion  = getAssetNextVersion(assetPath, character, rigType, rigAssetType)
    
    lastVersionFile = getAssetVersionedFile(assetPath, character, rigType, rigAssetType, lastVersion)
    
    if os.path.isfile(lastVersionFile):
        newVersionfile  = lastVersionFile.replace(lastVersion, newVersion)
    else:
        newVersionfile  = os.path.join(assetPath, character, 'rig', rigType, rigAssetType, '%s_%s_rig_%s_v001.%s'%(character, rigType, rigAssetType, fileFormat))
    
    return newVersionfile



def readVersiondComponent(character, version):
    filepath = getAssetVersionedFile(ROOT_ASSET_PATH, character, 'body', 'twistJointcomponent', version)
    if not os.path.isfile(filepath):return
    
    #- read Data
    f = open(filepath, 'r')
    data = json.load(f)
    f.close()
    return data


def publishComponent(character, data):
    tempfilepath = tempfile.mktemp('.json')

    f = open(tempfilepath, 'w')
    json.dump(data, f, indent=4)
    f.close()

    filepath = getNewVersionFile(ROOT_ASSET_PATH, character, 'body', 'twistJointcomponent', 'json')
    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    shutil.copy(tempfilepath, filepath)
    
    print '\r\n publish Component to : %s'%filepath,


def publishGuide(character):
    transforms  = ' '.join(mc.ls(type='transform'))
    guideGroups = re.findall('\S+:link_gui_grp', transforms)
    if len(guideGroups) == 0:return
    
    mc.select(guideGroups)
    
    tmpin = tempfile.mktemp('.ma')
    mc.file(tmpin,pr=True,es=True,f=True,typ='mayaAscii')
    
    filepath = getNewVersionFile(ROOT_ASSET_PATH, character, 'body', 'twistJointguide', 'ma')
    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))    
    shutil.copy(tmpin, filepath)
    
    print '\r\n publish Guide to : %s'%filepath,