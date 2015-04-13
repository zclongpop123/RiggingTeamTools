import sys

Path = '//bjserver2/WScriptsTool/rig/RiggingTeamTools'
if Path not in sys.path:
    sys.path.append(Path)


import RootUI
reload(RootUI)
RootUI.PlugTool()

#