import os, re, glob, tempfile, shutil, inspect, json
import maya.cmds as mc
import pymel.core

#-----------------------------------------------------------------------------
ROOTCHARA = '//bjserver3/Tank/blinky_bill_movie/assets/rigItem/asset/character'
FACE_CONTROL_GRP = 'C_faceGUI_ctl_0'
#-----------------------------------------------------------------------------
def getScriptPath():
    scriptFile = inspect.getfile(inspect.currentframe())
    return os.path.dirname(scriptFile)


def getTempLocatorPath(character):
    tempLocatorPath = os.path.join(ROOTCHARA, character, 'rig', 'face', 'TempLocators')
    if not os.path.isdir(tempLocatorPath):
        os.makedirs(tempLocatorPath)
    return tempLocatorPath



def getTempLocatorVersions(character):
    tempLocatorpath = getTempLocatorPath(character)
    os.chdir(tempLocatorpath)
    
    versions = []
    for locatorFile in glob.iglob('*.ma'):
        version = re.search('(?<=v)\d+(?=\.)', locatorFile)
        if not version:continue
        versions.append(version.group())
    return versions
        


def getTempLocatorlastVersion(character):
    versions = [int(x) for x in getTempLocatorVersions(character)]
    versions.append(0)
    lastVersion = str(max(versions))
    return lastVersion.zfill(3)



def getVersiondTempLocatorFile(character, version):
    filepath = os.path.join(getTempLocatorPath(character), '%s_face_rig_TempLocator_v%s.ma'%(character, version))
    return filepath.replace('\\', '/')




def getTempLocatorNextVersion(character):
    lastVersion = getTempLocatorlastVersion(character)
    nextVersion = str(int(lastVersion) + 1)
    return nextVersion.zfill(3)

#---------------------------------------------------------------------------------------------------------------------------------------------------
def exportControlData(file):

    # store control shape info
    buffer = {}
    ctlbuffer = {}
    shapes = mc.ls('*_Tctl_*', type='nurbsCurve')
    for shp in shapes:

        shpbuffer = {}
        spans = mc.getAttr('%s.spans' % shp)
        if not spans: continue
        
        deg = 0
        if not mc.getAttr('%s.form' % shp): deg = 3

        for i, space in enumerate(['objectSpace', 'worldSpace']):

            shpbuffer[space] = {}

            for j in range(spans + deg):
                pos = mc.xform('%s.cv[%s]' % (shp, j), q=True, ws=i, t=True)
                shpbuffer[space][j] = [pos[0], pos[1], pos[2]]

        ctlbuffer[shp] = shpbuffer

    if not ctlbuffer:
        return

    buffer['**CONTROL_DATA**'] = ctlbuffer

    # dump
    j = json.dumps(buffer, sort_keys=True, indent=2)

    f = open(file, 'w')
    f.write(j)
    f.close()
    
    
    
    
def importControlData(file, skipList=list(), selected=None, worldSpace=False):

    f = open(file, 'r')
    j = json.loads(f.read())
    f.close()

    if not '**CONTROL_DATA**' in j: return


    controlData = j['**CONTROL_DATA**']

    for shp in controlData:

        if not mc.objExists(shp):
            continue

        if selected:
            parent = mc.listRelatives(shp, p=True)[0]
            if parent not in selected: continue

        # Skip list.
        skip = False
        for skipItem in mc.ls(skipList):
            if shp == skipItem:
                skip = True
            elif mc.listRelatives(shp, p=True)[0] == skipItem:
                skip = True

        if skip:
            continue

        pointData = None
        if not ('objectSpace' in controlData[shp].keys() and 'worldSpace' in controlData[shp].keys()):
            worldSpace = True
            pointData = controlData[shp]

        else:
            if not worldSpace:
                pointData = controlData[shp]['objectSpace']
            else:
                pointData = controlData[shp]['worldSpace']

        for cv in pointData:
            mc.xform('%s.cv[%s]' % (shp, cv), t=pointData[cv], ws=worldSpace, os=abs(1 - worldSpace), a=True)    
    
    
    
    
def addAxisTemp(obj):
    curveData = ((13, 'mc.curve(d=1,p=((4.534,0,0.2),(5,0,0),(4.534,0,-0.2),(5,0,0),(0,0,0)))'),
                 (14, 'mc.curve(d=1,p=((0,4.534,-0.2),(0,5,0),(0,4.534,0.2),(0,5,0),(0,0,0)))'),
                 (6, 'mc.curve(d=1,p=((-0.2,0,4.534),(0,0,5),(0.2,0,4.534),(0,0,5),(0,0,0)))'))
    
    mc.addAttr(obj, sn='axisTemp', min=0, max=1, dv=0, k=True)
    mc.setAttr('%s.axisTemp'%obj, k=False, cb=True)    

    for colorV, makeCus in dict(curveData).iteritems():
        Cus = eval(makeCus)
        CusShape = mc.listRelatives(Cus, s=True, path=True)
        mc.setAttr('%s.ove'%CusShape[0], 1)
        mc.setAttr('%s.ovc'%CusShape[0], colorV)
        
        mc.parent(CusShape, obj, s=True, r=True)
        mc.delete(Cus)
        #-----
        mc.connectAttr('%s.axisTemp'%obj, '%s.v'%CusShape[0])
        
        
def makeTempLocators():
    locatorGroup = mc.group(em=True, name='TempLocator_grp')
    for ctl in mc.listRelatives(FACE_CONTROL_GRP, ad=True, type='transform'):
        if not re.search('_ctl_\d+$', ctl):continue
        if re.match('C_faceGUI_ctl_0', ctl):continue
        
        #- make locators
        locator = '%s_tempLoc'%ctl
        if mc.objExists(locator):return
        mc.spaceLocator(p=(0,0,0), name=locator)[0]
        
        #- match position
        mc.delete(mc.parentConstraint(ctl, locator))
        
        #- parent
        mc.parent(locator, locatorGroup)
        
        #- add Axis
        addAxisTemp(locator)



def importLocators(filePath):
    if not os.path.isfile(filePath):return
    mc.file(filePath, i=True)



def getTempLocators():
    sceneLocators = ' '.join(mc.listRelatives(mc.ls(type='locator'), p=True))
    tempLocators = re.findall('\S+_tempLoc', sceneLocators)
    return tempLocators




def mirrorTempLocators(sourceSide, targentSide, across='x', mirrorRotation=True):
    tempLocators = getTempLocators()
    
    for sourceloc in tempLocators:
        if sourceloc.startswith(targentSide):continue
        if sourceloc.startswith('C_'):continue
        
        targentloc = sourceloc.replace(sourceSide, targentSide)
        
        sourcelocPosition = mc.xform(sourceloc, q=True, ws=True, t=True)
        sourcelocPosition['xyz'.index(across)] = sourcelocPosition['xyz'.index(across)] * -1

        mc.xform(targentloc, ws=True, t=(sourcelocPosition[0] , sourcelocPosition[1], sourcelocPosition[2]))
        
        if not mirrorRotation:continue

        oldParent = mc.listRelatives(sourceloc, p=True, path=True)
        tempGrp = mc.group(em=True)
        mc.parent(sourceloc, tempGrp)
        
        mc.setAttr(tempGrp + '.sx', -1)
        mc.parent(sourceloc, w=True)
        mc.delete(mc.parentConstraint(sourceloc, targentloc))
        
        mc.parent(sourceloc, tempGrp)
        mc.setAttr(tempGrp + '.sx', 1)
        mc.parent(sourceloc, oldParent)
        mc.delete(tempGrp)
        


        
def publishTempLocators(character):
    tempLocators = getTempLocators()
    if len(tempLocators) == 0:return 

    mc.select(tempLocators)
    
    tempPath = tempfile.mkdtemp('.ma')
    mc.file(tempPath, typ='mayaAscii', f=True, es=True, ch=True, con=True, exp=True, sh=True)    
    
    
    newVersion = getTempLocatorNextVersion(character)
    newVersionFile = getVersiondTempLocatorFile(character, newVersion)

    shutil.copy(tempPath, newVersionFile)
    return newVersionFile



def makeControl(tempLoc):
    tempLocRealname = tempLoc.split(':')[-1]
    tempNameparts = tempLocRealname.split('_')
    ctlName = '%s_%s_Tctl_%s'%(tempNameparts[0], tempNameparts[1], tempNameparts[3])
    ctgName = '%s_%s_Tctg_%s'%(tempNameparts[0], tempNameparts[1], tempNameparts[3])
    cthName = '%s_%s_Tcth_%s'%(tempNameparts[0], tempNameparts[1], tempNameparts[3])
    
    basectl = ctlName.replace('_Tctl_', '_ctl_')
    basectg = ctgName.replace('_Tctg_', '_ctg_')
    basecth = cthName.replace('_Tcth_', '_cth_')
    

    if not mc.objExists(basectl):return

    # make control transform
    cthGrp = mc.group(mc.group(mc.group(em=True, name=ctlName), name=ctgName), name=cthName)
    
    # match positions
    mc.delete(mc.parentConstraint(tempLoc, cthGrp))
    
    # conform shapes
    ShapeParent = mc.duplicate(basectl)[0]
    shape = mc.listRelatives(ShapeParent, s=True, path=True)
    
    mc.parent(shape, ctlName, r=True, s=True)
    mc.delete(ShapeParent)
    
    mc.rename(shape[0], ctlName + 'Shape')
    
    # conform attributes
    defaultAttr = ('translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'visibility')
    usedAttr    = mc.listAttr(basectl, k=True)
    
    #- Lock Attribute -
    for attr in defaultAttr:
        if attr not in usedAttr:
            mc.setAttr('%s.%s'%(ctlName, attr), l=True, k=False)
        else:
            mc.connectAttr('%s.%s'%(ctlName, attr), '%s.%s'%(basectl, attr), f=True)
    
    #- limie Attribute -
    for a in 'trs':
        for b in 'xyz':
            minValue,  maxValue  = eval('mc.transformLimits("%s", q=True, %s%s=True)'%(basectl, a, b))
            enableMin, enableMax = eval('mc.transformLimits("%s", q=True, e%s%s=True)'%(basectl, a, b))
            eval('mc.transformLimits("%s", %s%s=(%s, %s), e%s%s=(%s, %s))'%(ctlName, a, b, minValue,  maxValue, a, b, enableMin, enableMax))

    #- copy attributes
    copyAttributes(basectl, ctlName)


    #- add control Range -
    mc.addAttr(ctlName, sn='range', min=0.01, max=20, dv=1, k=True)
    mc.setAttr('%s.range'%ctlName, k=False, cb=True)
    
    DivideNode = mc.createNode('multiplyDivide', name='%s_RDN'%ctlName)
    mc.setAttr('%s.op'%DivideNode, 2)
    for x in 'xyz':
        mc.connectAttr('%s.range'%ctlName, '%s.s%s'%(ctgName, x))
        
        mc.setAttr('%s.i1%s'%(DivideNode, x), 1)
        mc.connectAttr('%s.range'%ctlName, '%s.i2%s'%(DivideNode, x))
        mc.connectAttr('%s.o%s'%(DivideNode, x), '%s.s%s'%(ctlName, x))
        
        mc.setAttr('%s.s%s'%(ctlName, x), l=True, k=False)



def parentControl():
    transforms = ' '.join(mc.ls(type='transform'))
    baseCths   =  re.findall('\S+_cth_\d+', transforms)
    baseCths = dict().fromkeys(baseCths).keys()
    for baseCth in baseCths:
        cthParent = mc.listRelatives(baseCth, p=True, path=True)
        if not cthParent:continue
        
        newCth = baseCth.replace('_cth_', '_Tcth_')
        newCthParent = cthParent[0].replace('_ctl_', '_Tctl_')
        
        if not mc.objExists(newCth):continue
        if not mc.objExists(newCthParent):continue
        
        mc.parent(newCth, newCthParent)
    



def parentControlByData():
    ScriptPath = getScriptPath()
    
    f = open(os.path.join(ScriptPath, 'ControlParentData.json'), 'r')
    parentData = json.load(f)
    f.close()    
    # --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--
    for pnt, children in parentData.iteritems():
        if not mc.objExists(pnt):continue
        
        for child in children:
            if not mc.objExists(child):continue
            #- parent control
            mc.parent(child, pnt)





def copyAttributes(sourceOBJ, targentOBJ):
    def _copyAttr(sourceOBJ, targentOBJ, attr):
        args = {}
        args['ln'] = mc.addAttr('%s.%s'%(sourceOBJ, attr), q=True, ln=True)
        args['sn'] = mc.addAttr('%s.%s'%(sourceOBJ, attr), q=True, sn=True)
        args['nn'] = mc.addAttr('%s.%s'%(sourceOBJ, attr), q=True, nn=True)
        args['at'] = mc.addAttr('%s.%s'%(sourceOBJ, attr), q=True, at=True)
        
        if args['at'] == 'enum':
            args['en'] = mc.addAttr('%s.%s'%(sourceOBJ, attr), q=True, en=True)
        
        elif args['at'] == 'double' or args['at'] == 'long':
            minV     = mc.addAttr('%s.%s'%(sourceOBJ, attr), q=True, min=True)
            maxV     = mc.addAttr('%s.%s'%(sourceOBJ, attr), q=True, max=True)
            defaultV = mc.addAttr('%s.%s'%(sourceOBJ, attr), q=True, dv=True)
            if minV:
                args['min'] = minV
            if maxV:
                args['max'] = maxV  
            if defaultV:
                args['dv'] = defaultV
        else:
            pass
        
        #- add attribute
        mc.addAttr(targentOBJ, k=True, **args)
        
        
        #- connect
        attrIns = pymel.core.PyNode('%s.%s'%(sourceOBJ, attr))
        if not attrIns.isLocked():
            mc.connectAttr('%s.%s'%(targentOBJ, attr), '%s.%s'%(sourceOBJ, attr))
        #-------------------------------------------------------------------
        
    UDattr = mc.listAttr(sourceOBJ, ud=True)
    for attr in UDattr:
        if attr in ('keepMe', 'showFrame', 'faceRigGUIControl'):
            continue
        _copyAttr(sourceOBJ, targentOBJ, attr)




def drivenVisbility():
    ScriptPath = getScriptPath()
    VisbilityControlFile = os.path.join(ScriptPath, 'visibilityControl.ma')
    mc.file(VisbilityControlFile, i=True)
    
    #-------   Read Data  -------
    f = open(os.path.join(ScriptPath, 'ControlVisbilityData.json'), 'r')
    VisbilityData = json.load(f)
    f.close()
    #----  connect visbility  ----
    for driver, drivens in VisbilityData.iteritems():
        for driven in drivens:
            #- 1
            if not mc.objExists(driven):
                continue
            #- 2 
            if mc.listRelatives(driven, c=True, type='transform'):
                shape = mc.listRelatives(driven, c=True, path=True)
                mc.connectAttr('%s.ty'%driver, '%s.v'%shape[0])
            else:
                pnt = mc.listRelatives(driven, p=True, path=True)
                mc.connectAttr('%s.ty'%driver, '%s.v'%pnt[0])





#---------------------------------------------------------------------------------------------------------------------------------------------------
def buildControlOnFace(character, version):
    TempLocatorFile = getVersiondTempLocatorFile(character, version)
    if not os.path.isfile(TempLocatorFile):return
    
    # reference guide
    mc.file(TempLocatorFile, r=True, ns='TempLocGuide')
    #--------- build ---------
    
    # make control
    for locator in getTempLocators():
        makeControl(locator)
    
    # make hiy
    
    #- 1
    parentControl()
    #- 2
    parentControlByData()
    
    
    # driven visbility
    drivenVisbility()
    
    
    #-------------------------
    # remove guide
    mc.file(TempLocatorFile, rr=True)