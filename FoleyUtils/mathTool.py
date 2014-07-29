#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
#=============================================
import math
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def clamp(minV, maxV, value):
    '''
    0, 10,  5  ->   5
    0, 10, -1  ->   0
    0, 10, 11  ->  10
    '''
    return min(max(minV, value), maxV)




def setRange(oldMin, oldMax, newMin, newMax, value):
    '''
    0 - 10  --->  0 - 100
      |             |
      5      ->     50   
    '''
    result = ((float(value) - oldMin) / (oldMax - oldMin) * (newMax - newMin)) + newMin
    return result




def advanceSin(startValue, endValue, inputV):
    '''
    convert a range value to sin 0 - sin 180
    '''
    angleValue = setRange(startValue, endValue, 0, 180, inputV)
    sinValue = math.sin(angleValue * math.pi / 180.0)
    return sinValue




def converse(startValue, endValue, inputValue):
    '''
    0.0, 0.1, 0.2 ... 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.7, ... 0.2, 0.1, 0.0
    '''
    x = setRange(startValue, endValue, -1, 1, inputValue)
    result = 1 - abs(x)
    return result





def getPoleVectorPosition(Root, Mid, Tip):
    '''
    #  * (Root)
    #   *
    #    *
    #     *
    #      *
    #       *
    #        * (Mid) -----------> * (poleVector[X, Y, Z])
    #      *
    #    *
    #  * (Tip)
    '''
    #-----------------------------------------------------------
    A = mc.xform(Root, q=True, ws=True, t=True)
    B = mc.xform(Mid, q=True, ws=True, t=True)
    C = mc.xform(Tip, q=True, ws=True, t=True)
    
    AB = math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 + (A[2] - B[2]) ** 2)
    BC = math.sqrt((B[0] - C[0]) ** 2 + (B[1] - C[1]) ** 2 + (B[2] - C[2]) ** 2)
    AC = math.sqrt((A[0] - C[0]) ** 2 + (A[1] - C[1]) ** 2 + (A[2] - C[2]) ** 2)
    
    AD = (AB ** 2 + AC ** 2 - BC**2 ) / (AC * 2)
    ADpr = AD / AC
    
    D = ((C[0] - A[0]) * ADpr + A[0], (C[1] - A[1]) * ADpr + A[1], (C[2] - A[2]) * ADpr + A[2])
    BD = math.sqrt((B[0] - D[0]) ** 2 + (B[1] - D[1]) ** 2 + (B[2] - D[2]) ** 2)
    ScaleV = (AB + BC) / BD
    VectorPosition = ((B[0] - D[0]) * ScaleV + D[0], (B[1] - D[1]) * ScaleV + D[1], (B[2] - D[2]) * ScaleV + D[2])
    
    return VectorPosition