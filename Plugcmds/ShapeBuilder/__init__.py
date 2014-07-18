import os,inspect

initfile = inspect.getfile(inspect.currentframe())
initdir  = os.path.dirname(initfile)
contents = os.listdir(initdir)
modules = []
for m in contents:
    if m[-3:] != '.py' or '__init__' in m:
        continue
    modules.append(m[:-3])
__all__ = modules