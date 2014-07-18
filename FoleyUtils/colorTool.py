#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
#   http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
#=============================================
import math, struct
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def hsv_to_rgb(h, s, v):
    '''
    import a HSV color, return RGB values..
    (0, 0, 100) -> (255, 255, 255)
    '''
    h, s, v = float(h), float(s), float(v)
    
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    
    color_dict = {0:(v, t, p), 1:(q, v, p), 2:(p, v, t), 3:(p, q, v), 4:(t, p, v), 5:(v, p, q)}
    r, g, b = color_dict.get(hi, (0, 0, 0))
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    
    return r, g, b




def rgb_to_hsv(r, g, b):
    '''
    import a RGB color, return HSV valus..
    (255, 255, 255) -> (0, 0, 100)
    '''
    r, g, b = r/255.0, g/255.0, b/255.0
    maxV = max(r, g, b)
    minV = min(r, g, b)
    df = maxV-minV
    if maxV == minV:
        h = 0
    elif maxV == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif maxV == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif maxV == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if maxV == 0:
        s = 0
    else:
        s = df/maxV
    v = maxV
    return h, s, v





def hex_to_rgb(rgbstr):
    '''
    return RGB value by hex string..
    5a5a5a -> (90, 90, 90)
    '''
    return struct.unpack('BBB',rgbstr.decode('hex'))




def rgb_to_hex(r, g, b):
    '''
    return hex string by RGB color Values..
    (90, 90, 90) -> 5a5a5a
    '''
    return struct.pack('BBB', r, g, b).encode('hex')