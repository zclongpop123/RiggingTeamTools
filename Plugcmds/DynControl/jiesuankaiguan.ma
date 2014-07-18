//Maya ASCII 2013ff10 scene
//Name: jiesuankaiguan.ma
//Last modified: Thu, Dec 26, 2013 03:56:20 PM
//Codeset: 936
requires maya "2013ff10";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2013";
fileInfo "version" "2013 x64";
fileInfo "cutIdentifier" "201209140124-844721";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "hair_ctrl_grp";
	setAttr ".t" -type "double3" 1.675984550037592e-015 18.231613159179673 0.91203022003173762 ;
	setAttr ".r" -type "double3" -5.1246158916214507e-015 -3.6688241060904878e-014 1.7049617267975087e-014 ;
	setAttr ".s" -type "double3" 0.46548191348305967 0.46548191348305984 0.46548191348305989 ;
createNode transform -n "hair_controller_grp" -p "hair_ctrl_grp";
createNode joint -n "hair_ctrl" -p "hair_controller_grp";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "___DYNAMICS___" -ln "___DYNAMICS___" -at "double";
	addAttr -ci true -sn "chainAttach" -ln "chainAttach" -dv 1 -min 0 -max 3 -en "No Attach:Base:Tip:Both End" 
		-at "enum";
	addAttr -ci true -sn "chainStartEnveloppe" -ln "chainStartEnveloppe" -dv 1 -min 
		0 -max 1 -at "double";
	addAttr -ci true -sn "chainStartFrame" -ln "chainStartFrame" -dv 1 -at "double";
	addAttr -ci true -sn "___BEHAVIOR___" -ln "___BEHAVIOR___" -at "double";
	addAttr -ci true -sn "chainStiffness" -ln "chainStiffness" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "chainDamping" -ln "chainDamping" -dv 0.2 -min 0 -at "double";
	addAttr -ci true -sn "chainGravity" -ln "chainGravity" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "chainIteration" -ln "chainIteration" -dv 1 -min 0 -at "long";
	addAttr -ci true -sn "___COLLISIONS___" -ln "___COLLISIONS___" -at "double";
	addAttr -ci true -sn "chainCollide" -ln "chainCollide" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "chainWidthBase" -ln "chainWidthBase" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "chainWidthExtremity" -ln "chainWidthExtremity" -dv 1 -min 
		0 -at "double";
	addAttr -ci true -sn "chainCollideGround" -ln "chainCollideGround" -min 0 -max 1 
		-at "bool";
	addAttr -ci true -sn "chainCollideGroundHeight" -ln "chainCollideGroundHeight" -at "double";
	addAttr -ci true -sn "StarCurveAttract" -ln "StarCurveAttract" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "Drag" -ln "Drag" -dv 0.05 -min 0 -max 1 -at "double";
	addAttr -ci true -sn "Friction" -ln "Friction" -dv 0.5 -min 0 -max 1 -at "double";
	addAttr -ci true -sn "Mass" -ln "Mass" -dv 1 -min 0 -max 10 -at "double";
	addAttr -ci true -sn "secondaryUp" -ln "secondaryUp" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "secondaryDn" -ln "secondaryDn" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "secondaryFrn" -ln "secondaryFrn" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "Hair_modle" -ln "Hair_modle" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "show_hairConstraint" -ln "show_hairConstraint" -min 0 -max 
		1 -at "double";
	addAttr -ci true -sn "Fringe" -ln "Fringe" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "HairBg" -ln "HairBg" -at "double";
	addAttr -ci true -sn "hairBg_Enveloppe" -ln "hairBg_Enveloppe" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "hairBgModle" -ln "hairBgModle" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "HairG" -ln "HairG" -at "double";
	addAttr -ci true -sn "Hair_G_Enveloppe" -ln "Hair_G_Enveloppe" -nn "Hair G Enveloppe" 
		-min 0 -max 1 -at "double";
	addAttr -ci true -sn "Hair_R_Offset" -ln "Hair_R_Offset" -nn "Hair R Offset" -dv 
		1 -min -90 -max 90 -at "double";
	addAttr -ci true -sn "Hair_L_Offset" -ln "Hair_L_Offset" -min -90 -max 90 -at "double";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.46548191348305967 1.3851436419045091e-016 2.9806231447568348e-016 0
		 -1.0122302798181744e-016 0.46548191348305984 -4.1633363423443592e-017 0 -2.6161215516581273e-016 4.163336342344337e-017 0.46548191348305989 0
		 1.675984550037592e-015 18.231613159179673 0.91203022003173762 1;
	setAttr -l on -cb off ".radi" 0.5;
	setAttr -l on -k on ".___DYNAMICS___";
	setAttr -l on ".chainAttach";
	setAttr -k on ".chainStartEnveloppe" 0;
	setAttr -k on ".chainStartFrame" 0;
	setAttr -l on -k on ".___BEHAVIOR___";
	setAttr -k on ".chainStiffness" 0.2;
	setAttr -k on ".chainDamping" 3;
	setAttr -k on ".chainGravity";
	setAttr -l on ".chainIteration";
	setAttr -l on -k on ".___COLLISIONS___";
	setAttr -k on ".chainCollide" yes;
	setAttr -l on ".chainWidthBase" 0.2;
	setAttr -l on ".chainWidthExtremity" 0.2;
	setAttr -l on ".chainCollideGround";
	setAttr -l on ".chainCollideGroundHeight";
	setAttr -k on ".StarCurveAttract" 1;
	setAttr -l on ".Drag";
	setAttr -l on ".Friction";
	setAttr -l on ".Mass";
	setAttr -l on ".secondaryUp";
	setAttr -l on ".secondaryDn";
	setAttr -l on ".secondaryFrn";
	setAttr -l on ".Hair_modle";
	setAttr -l on ".show_hairConstraint";
	setAttr -l on ".Fringe";
	setAttr -l on ".HairBg";
	setAttr -l on ".hairBg_Enveloppe";
	setAttr -l on ".hairBgModle";
	setAttr -l on ".HairG";
	setAttr -l on ".Hair_G_Enveloppe";
	setAttr -l on ".Hair_R_Offset" 0;
	setAttr -l on ".Hair_L_Offset";
createNode nurbsCurve -n "hair_ctrlShape" -p "hair_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 12 0 no 3
		13 0 4 8 12 16 24.485281000000001 32.970562999999999 36.970562999999999 45.455843999999999
		 53.941125 57.941125 66.426406999999998 74.911687999999998
		13
		0.51041844208980558 3.8238459757939038 -0.51041844208980491
		-0.51041844208980558 3.8238459757939038 -0.51041844208980491
		-0.51041844208980558 3.8238459757939056 0.51041844208980625
		0.51041844208980558 3.8238459757939056 0.51041844208980625
		0.51041844208980558 3.8238459757939038 -0.51041844208980491
		8.5750151422752852e-016 2.2072345676631446 1.8960669974995766e-015
		-0.51041844208980558 3.8238459757939038 -0.51041844208980491
		-0.51041844208980558 3.8238459757939056 0.51041844208980625
		8.5750151422752852e-016 2.2072345676631446 1.8960669974995766e-015
		0.51041844208980558 3.8238459757939056 0.51041844208980625
		0.51041844208980558 3.8238459757939038 -0.51041844208980491
		8.5750151422752852e-016 2.2072345676631446 1.8960669974995766e-015
		-0.51041844208980558 3.8238459757939038 -0.51041844208980491
		;
createNode transform -n "attractionScale_grp" -p "hair_ctrl";
	setAttr ".t" -type "double3" -4.7277507287548217e-016 -2.174092693697169 -4.4408920985006262e-016 ;
	setAttr ".r" -type "double3" 5.1246158916214444e-015 3.6688241060904871e-014 -1.7049617267975087e-014 ;
	setAttr ".s" -type "double3" 0.96546087498618594 0.96546087498618571 0.96546087498618549 ;
createNode transform -n "attractionScale" -p "attractionScale_grp";
	addAttr -ci true -sn "hairAttract_button" -ln "hairAttract_button" -dt "string";
	addAttr -ci true -sn "notes" -ln "notes" -dt "string";
	addAttr -ci true -sn "hairSystem" -ln "hairSystem" -at "message";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr -l on ".hairAttract_button" -type "string" "name";
	setAttr ".notes" -type "string" "editRampAttribute";
createNode nurbsCurve -n "attractionScaleShape" -p "attractionScale";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.29723460772062055 4.2578777315019147 0.2972346077206221
		-0.29723460772062055 4.2578777315019147 -0.29723460772062077
		0.29723460772062232 4.2578777315019147 -0.29723460772062077
		0.29723460772062232 4.2578777315019147 0.2972346077206221
		-0.29723460772062055 4.2578777315019147 0.2972346077206221
		-0.29723460772062055 3.6634085160606729 0.2972346077206221
		-0.29723460772062055 3.6634085160606729 -0.29723460772062077
		-0.29723460772062055 4.2578777315019147 -0.29723460772062077
		-0.29723460772062055 4.2578777315019147 0.2972346077206221
		-0.29723460772062055 3.6634085160606729 0.2972346077206221
		0.29723460772062232 3.6634085160606729 0.2972346077206221
		0.29723460772062232 4.2578777315019147 0.2972346077206221
		0.29723460772062232 4.2578777315019147 -0.29723460772062077
		0.29723460772062232 3.6634085160606729 -0.29723460772062077
		0.29723460772062232 3.6634085160606729 0.2972346077206221
		0.29723460772062232 3.6634085160606729 -0.29723460772062077
		-0.29723460772062055 3.6634085160606729 -0.29723460772062077
		;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultShaderList1;
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :renderGlobalsList1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 18 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surfaces" "Particles" "Fluids" "Image Planes" "UI:" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 18 0 1 1 1 1 1
		 1 1 0 1 0 0 0 0 0 0 0 0 ;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
// End of jiesuankaiguan.ma
