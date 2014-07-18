//Maya ASCII 2013ff10 scene
//Name: guide.ma
//Last modified: Thu, Mar 13, 2014 05:50:20 PM
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
createNode transform -n "link_gui_grp";
createNode transform -n "link_start_gui_g" -p "link_gui_grp";
createNode joint -n "link_start_gui" -p "link_start_gui_g";
	addAttr -ci true -sn "jointCount" -ln "jointCount" -dv 2 -min 2 -at "long";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".rx";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -l on -cb off ".radi" 0;
	setAttr -k on ".jointCount";
createNode nurbsCurve -n "nurbsCircleShape4" -p "link_start_gui";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.39207187014239153 2.4007478040279789e-017 -0.3920718701423907
		-6.3258780080362606e-017 3.3951701042937951e-017 -0.55447335618035298
		-0.39207187014239087 2.4007478040279801e-017 -0.39207187014239087
		-0.55447335618035298 9.8383535577486679e-033 -1.8320543434235623e-016
		-0.39207187014239114 -2.4007478040279792e-017 0.3920718701423907
		-1.670736433847792e-016 -3.3951701042937951e-017 0.55447335618035298
		0.3920718701423907 -2.4007478040279801e-017 0.39207187014239087
		0.55447335618035298 -1.8235524860915387e-032 2.7527579368535218e-016
		0.39207187014239153 2.4007478040279789e-017 -0.3920718701423907
		-6.3258780080362606e-017 3.3951701042937951e-017 -0.55447335618035298
		-0.39207187014239087 2.4007478040279801e-017 -0.39207187014239087
		;
createNode nurbsCurve -n "nurbsCircleShape2" -p "link_start_gui";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.39237760646115277 0.392377606461152 -8.5660452119742395e-017
		-6.3308109063194328e-017 0.55490573262885501 -1.1179696820972101e-016
		-0.39237760646115222 0.39237760646115222 -8.566045211974242e-017
		-0.55490573262885501 1.8335911917266018e-016 -2.2561320502134134e-017
		-0.39237760646115222 -0.39237760646115216 4.0537811115474201e-017
		-1.6720392684702262e-016 -0.55490573262885501 6.6674327205452827e-017
		0.392377606461152 -0.39237760646115222 4.0537811115474201e-017
		0.55490573262885501 -2.7547963096656135e-016 -2.2561320502134075e-017
		0.39237760646115277 0.392377606461152 -8.5660452119742395e-017
		-6.3308109063194328e-017 0.55490573262885501 -1.1179696820972101e-016
		-0.39237760646115222 0.39237760646115222 -8.566045211974242e-017
		;
createNode nurbsCurve -n "nurbsCircleShape3" -p "link_start_gui";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		6.3099131617608628e-017 0.39237760646115277 -0.392377606461152
		-3.3978176464622177e-017 -4.0746788561060284e-017 -0.55490573262885501
		-1.1115152959858341e-016 -0.39237760646115222 -0.39237760646115222
		-1.2321382417220917e-016 -0.55490573262885501 -1.8335911917266018e-016
		-6.3099131617608529e-017 -0.39237760646115222 0.39237760646115216
		3.3978176464622115e-017 -1.446426063448885e-016 0.55490573262885501
		1.1115152959858336e-016 0.392377606461152 0.39237760646115222
		1.2321382417220917e-016 0.55490573262885501 2.7547963096656135e-016
		6.3099131617608628e-017 0.39237760646115277 -0.392377606461152
		-3.3978176464622177e-017 -4.0746788561060284e-017 -0.55490573262885501
		-1.1115152959858341e-016 -0.39237760646115222 -0.39237760646115222
		;
createNode aimConstraint -n "link_start_gui_aimConstraint1" -p "link_start_gui";
	addAttr -ci true -sn "w0" -ln "link_end_guiW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode joint -n "link_startRotate_gui" -p "link_start_gui";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -l on -cb off ".radi" 0;
createNode nurbsCurve -n "curveShape2" -p "link_startRotate_gui";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".cc" -type "nurbsCurve" 
		1 5 0 no 3
		6 0 1 2 3 4 5
		6
		0 2.9763632803314488 0
		-0.19549566772084104 2.9763632803314488 0
		0 3.5842501341148196 0
		0.19549566772084237 2.9763632803314488 0
		0 2.9763632803314488 0
		0 0.5 -2.2561320502134122e-017
		;
createNode nurbsCurve -n "curveShape3" -p "link_startRotate_gui";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 5 0 no 3
		6 0 1 2 3 4 5
		6
		1.7753530657219945 4.4096463111455182e-016 0
		1.7753530657219945 0.12941344980380529 0
		2.1034383921998607 5.144587363003106e-016 0
		1.7753530657219945 -0.12941344980380529 0
		1.7753530657219945 4.4096463111455182e-016 0
		0.5 2.2561320502134122e-017 -2.2561320502134122e-017
		;
createNode transform -n "link_up_gui_gup" -p "link_startRotate_gui";
	setAttr ".t" -type "double3" 0 2.9 0 ;
createNode transform -n "link_up_gui_g" -p "link_up_gui_gup";
createNode joint -n "link_up_gui" -p "link_up_gui_g";
	setAttr ".v" no;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
createNode transform -n "link_end_gui_g" -p "link_gui_grp";
	setAttr ".t" -type "double3" 10 0 0 ;
createNode joint -n "link_end_gui" -p "link_end_gui_g";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -l on -cb off ".radi" 0;
createNode nurbsCurve -n "nurbsCircleShape1" -p "link_end_gui";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.39180581244561247 2.3991186704942341e-017 -0.39180581244561191
		-6.321585303914663e-017 3.3928661615554567e-017 -0.55409709377719396
		-0.39180581244561213 2.3991186704942356e-017 -0.39180581244561213
		-0.55409709377719396 9.8316773080939295e-033 -1.605634753618615e-016
		-0.39180581244561224 -2.399118670494235e-017 0.39180581244561202
		-1.6696026817952597e-016 -3.3928661615554573e-017 0.55409709377719407
		0.39180581244561191 -2.3991186704942363e-017 0.39180581244561213
		0.55409709377719396 -1.8223150339523958e-032 2.9760662996402936e-016
		0.39180581244561247 2.3991186704942341e-017 -0.39180581244561191
		-6.321585303914663e-017 3.3928661615554567e-017 -0.55409709377719396
		-0.39180581244561213 2.3991186704942356e-017 -0.39180581244561213
		;
createNode nurbsCurve -n "nurbsCircleShape2" -p "link_end_gui";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		6.3007180126874609e-017 0.39180581244561247 -0.39180581244561191
		-3.3928661615554579e-017 -6.3215853039146618e-017 -0.55409709377719396
		-1.1098955353675919e-016 -0.39180581244561213 -0.39180581244561213
		-1.2303427027786506e-016 -0.55409709377719396 -1.605634753618615e-016
		-6.3007180126874535e-017 -0.39180581244561224 0.39180581244561202
		3.3928661615554536e-017 -1.6696026817952597e-016 0.55409709377719407
		1.1098955353675916e-016 0.39180581244561191 0.39180581244561213
		1.2303427027786508e-016 0.55409709377719396 2.9760662996402936e-016
		6.3007180126874609e-017 0.39180581244561247 -0.39180581244561191
		-3.3928661615554579e-017 -6.3215853039146618e-017 -0.55409709377719396
		-1.1098955353675919e-016 -0.39180581244561213 -0.39180581244561213
		;
createNode nurbsCurve -n "nurbsCircleShape3" -p "link_end_gui";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.39180581244561191 0.39180581244561247 -1.5000554695869142e-016
		-0.55409709377719396 -6.3215853039146618e-017 -8.9105608662310477e-017
		-0.39180581244561213 -0.39180581244561213 2.3991186704942363e-017
		-1.6056347536186152e-016 -0.55409709377719396 1.2303427027786503e-016
		0.39180581244561202 -0.39180581244561224 1.5000554695869135e-016
		0.55409709377719407 -1.6696026817952597e-016 8.9105608662310551e-017
		0.39180581244561213 0.39180581244561191 -2.3991186704942301e-017
		2.9760662996402936e-016 0.55409709377719396 -1.2303427027786501e-016
		-0.39180581244561191 0.39180581244561247 -1.5000554695869142e-016
		-0.55409709377719396 -6.3215853039146618e-017 -8.9105608662310477e-017
		-0.39180581244561213 -0.39180581244561213 2.3991186704942363e-017
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
connectAttr "link_start_gui_aimConstraint1.cry" "link_start_gui.ry" -l on;
connectAttr "link_start_gui_aimConstraint1.crz" "link_start_gui.rz" -l on;
connectAttr "link_start_gui_aimConstraint1.crx" "link_start_gui.rx" -l on;
connectAttr "link_start_gui.pim" "link_start_gui_aimConstraint1.cpim";
connectAttr "link_start_gui.t" "link_start_gui_aimConstraint1.ct";
connectAttr "link_start_gui.rp" "link_start_gui_aimConstraint1.crp";
connectAttr "link_start_gui.rpt" "link_start_gui_aimConstraint1.crt";
connectAttr "link_start_gui.ro" "link_start_gui_aimConstraint1.cro";
connectAttr "link_start_gui.jo" "link_start_gui_aimConstraint1.cjo";
connectAttr "link_end_gui.t" "link_start_gui_aimConstraint1.tg[0].tt";
connectAttr "link_end_gui.rp" "link_start_gui_aimConstraint1.tg[0].trp";
connectAttr "link_end_gui.rpt" "link_start_gui_aimConstraint1.tg[0].trt";
connectAttr "link_end_gui.pm" "link_start_gui_aimConstraint1.tg[0].tpm";
connectAttr "link_start_gui_aimConstraint1.w0" "link_start_gui_aimConstraint1.tg[0].tw"
		;
connectAttr "link_start_gui.s" "link_startRotate_gui.is";
connectAttr "link_startRotate_gui.s" "link_up_gui.is";
// End of guide.ma
