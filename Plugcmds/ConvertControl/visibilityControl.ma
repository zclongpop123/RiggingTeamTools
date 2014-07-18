//Maya ASCII 2013ff10 scene
//Name: visibilityControl.ma
//Last modified: Mon, Mar 10, 2014 09:49:34 AM
//Codeset: 936
requires maya "2013ff10";
requires "Mayatomr" "2013.0 - 3.10.1.11 ";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2013";
fileInfo "version" "2013 x64";
fileInfo "cutIdentifier" "201209140124-844721";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "Face_Display_Control_G";
createNode transform -n "Face_Display_Control" -p "Face_Display_Control_G";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
createNode nurbsCurve -n "Face_Display_ControlShape" -p "Face_Display_Control";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-2 0 0
		2 0 0
		2 3 0
		-2 3 0
		-2 0 0
		;
createNode transform -n "Face_Display_TempA" -p "Face_Display_Control";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr ".rp" -type "double3" -1 1.5 0 ;
	setAttr ".sp" -type "double3" -1 1.5 0 ;
createNode nurbsCurve -n "Face_Display_TempAShape" -p "Face_Display_TempA";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		-1 0.16195563215367317 0
		-1 2.8380443678463267 0
		;
createNode transform -n "Face_Display_TempB" -p "Face_Display_Control";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr ".rp" -type "double3" 0 1.5 0 ;
	setAttr ".sp" -type "double3" 0 1.5 0 ;
createNode nurbsCurve -n "Face_Display_TempBShape" -p "Face_Display_TempB";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 0.16195563215367317 0
		0 2.8380443678463267 0
		;
createNode transform -n "Face_Display_TempC" -p "Face_Display_Control";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr ".rp" -type "double3" 1 1.5 0 ;
	setAttr ".sp" -type "double3" 1 1.5 0 ;
createNode nurbsCurve -n "Face_Display_TempCShape" -p "Face_Display_TempC";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		1 2.8380443678463267 0
		1 0.16195563215367317 0
		;
createNode transform -n "VisControl_A_G" -p "Face_Display_Control";
	setAttr ".t" -type "double3" -1 0.25 0 ;
	setAttr ".s" -type "double3" 2.5 2.5 2.5 ;
createNode transform -n "VisControl_A" -p "VisControl_A_G";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mntl" -type "double3" -1 0 -1 ;
	setAttr ".mtye" yes;
	setAttr ".xtye" yes;
createNode nurbsCurve -n "VisControl_AShape" -p "VisControl_A";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.078361162489122491 0.078361162489122185 0
		-1.2643170607829328e-017 0.11081941875543871 0
		-0.078361162489122449 0.07836116248912256 0
		-0.1108194187554388 0 0
		-0.078361162489122449 -0.07836116248912238 0
		-3.3392053635905197e-017 -0.11081941875543871 0
		0.078361162489122393 -0.07836116248912256 0
		0.1108194187554388 -1.7763568394002508e-016 0
		0.078361162489122491 0.078361162489122185 0
		-1.2643170607829328e-017 0.11081941875543871 0
		-0.078361162489122449 0.07836116248912256 0
		;
createNode transform -n "VisControl_B_G" -p "Face_Display_Control";
	setAttr ".t" -type "double3" 0 0.25 0 ;
	setAttr ".s" -type "double3" 2.5 2.5 2.5 ;
createNode transform -n "VisControl_B" -p "VisControl_B_G";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mntl" -type "double3" -1 0 -1 ;
	setAttr ".mtye" yes;
	setAttr ".xtye" yes;
createNode nurbsCurve -n "VisControl_BShape" -p "VisControl_B";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.078361162489122491 0.078361162489122185 0
		-1.2643170607829328e-017 0.11081941875543871 0
		-0.078361162489122449 0.07836116248912256 0
		-0.1108194187554388 0 0
		-0.078361162489122449 -0.07836116248912238 0
		-3.3392053635905197e-017 -0.11081941875543871 0
		0.078361162489122393 -0.07836116248912256 0
		0.1108194187554388 -1.7763568394002508e-016 0
		0.078361162489122491 0.078361162489122185 0
		-1.2643170607829328e-017 0.11081941875543871 0
		-0.078361162489122449 0.07836116248912256 0
		;
createNode transform -n "VisControl_C_G" -p "Face_Display_Control";
	setAttr ".t" -type "double3" 1 0.25 0 ;
	setAttr ".s" -type "double3" 2.5 2.5 2.5 ;
createNode transform -n "VisControl_C" -p "VisControl_C_G";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mntl" -type "double3" -1 0 -1 ;
	setAttr ".mtye" yes;
	setAttr ".xtye" yes;
createNode nurbsCurve -n "VisControl_CShape" -p "VisControl_C";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.078361162489122491 0.078361162489122185 0
		-1.2643170607829328e-017 0.11081941875543871 0
		-0.078361162489122449 0.07836116248912256 0
		-0.1108194187554388 0 0
		-0.078361162489122449 -0.07836116248912238 0
		-3.3392053635905197e-017 -0.11081941875543871 0
		0.078361162489122393 -0.07836116248912256 0
		0.1108194187554388 -1.7763568394002508e-016 0
		0.078361162489122491 0.078361162489122185 0
		-1.2643170607829328e-017 0.11081941875543871 0
		-0.078361162489122449 0.07836116248912256 0
		;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -av -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultObjectSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off ".ctrs" 256;
	setAttr -av -k off ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 18 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surfaces" "Particles" "Fluids" "Image Planes" "UI:" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 18 0 1 1 1 1 1
		 1 1 0 1 0 0 0 0 0 0 0 0 ;
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -k on ".ex";
	setAttr -av -k on ".es";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bf";
	setAttr -k on ".fii";
	setAttr -av -k on ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -k on ".mb";
	setAttr -k on ".ti";
	setAttr -k on ".txt";
	setAttr -k on ".mpr";
	setAttr -k on ".wzd";
	setAttr -k on ".fn" -type "string" "im";
	setAttr -k on ".if";
	setAttr -k on ".res" -type "string" "ntsc_4d 646 485 1.333";
	setAttr -k on ".as";
	setAttr -k on ".ds";
	setAttr -k on ".lm";
	setAttr -k on ".fir";
	setAttr -k on ".aap";
	setAttr -k on ".gh";
	setAttr -cb on ".sd";
// End of visibilityControl.ma
