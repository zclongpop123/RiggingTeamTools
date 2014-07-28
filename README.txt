import sys

Path = '//bjserver2/Temp Documents/Foley/RiggingTeamTools'
if Path not in sys.path:
    sys.path.append(Path)


import RootUI
reload(RootUI)
RootUI.PlugTool()

#