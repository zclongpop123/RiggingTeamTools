import maya.cmds as mc

class ColorButton(object):
    def __init__(self, colorID, RGBvalue=(0.0,0.0,0.0)):
        self.color = colorID
        self.Btn = mc.iconTextButton(w=20, h=20,l='', bgc=RGBvalue, c=self.setColor)

    
    def setColor(self):
        selectOBJs = mc.ls(sl=True)
        for OBJ in selectOBJs:
            for shp in mc.listRelatives(OBJ, s=True, path=True) or []:
                mc.setAttr(shp + '.ove', 1)
                mc.setAttr(shp + '.ovc', self.color)        


    def changeImage(self, Image=None):
        if Image == None:return
        #if not os.path.isfile(Image):return
        mc.iconTextButton(self.Btn, e=True, i=Image)




class ControlColorWindow(object):
    ColorRGBIndeX = ((0.267, 0.267, 0.267),(0.000, 0.000, 0.000),(0.251, 0.251, 0.251),(0.500, 0.500, 0.500),(0.608, 0.000, 0.157),(0.000, 0.016, 0.376),(0.000, 0.000, 1.000),(0.000, 0.275, 0.098),(0.149, 0.000, 0.263),(0.784, 0.000, 0.784),(0.541, 0.282, 0.200),(0.247, 0.137, 0.122),(0.600, 0.149, 0.000),(1.000, 0.000, 0.000),(0.000, 1.000, 0.000),(0.000, 0.255, 0.600),(1.000, 1.000, 1.000),(1.000, 1.000, 0.000),(0.392, 0.863, 1.000),(0.263, 1.000, 0.639),(1.000, 0.690, 0.690),(0.894, 0.675, 0.475),(1.000, 1.000, 0.388),(0.000, 0.600, 0.329),(0.631, 0.412, 0.188),(0.624, 0.631, 0.188),(0.408, 0.631, 0.188),(0.188, 0.631, 0.365),(0.188, 0.631, 0.631),(0.188, 0.404, 0.631),(0.435, 0.188, 0.631),(0.631, 0.188, 0.412))
    
    
    def __init__(self):
        if mc.window("ControlColors", ex=True):mc.deleteUI("ControlColors", wnd=True)
        if mc.windowPref("ControlColors", ex=True):mc.windowPref("ControlColors", r=True)           
        #----
        mc.window("ControlColors", t="Control   Colors", w=320, h=45, menuBar=True)
        mc.rowColumnLayout(w=320, nc=16, cw=[(i, 20) for i in range(1,17)])
        #----
        for i in range(32):
            clickButton = ColorButton(i, self.ColorRGBIndeX[i])
            if i > 0:continue
            clickButton.changeImage('fpe_brokenPaths.png')
        #----
        mc.showWindow("ControlColors")
        
        
        
        
if __name__ == '__main__':ControlColorWindow()

