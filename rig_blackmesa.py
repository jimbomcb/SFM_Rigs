## Black Mesa Source Rigging Scripts
## - jimbomcb@gmail.com

import vs
import sfm
import os

from vs import dmeutils
animUtils = dmeutils.CDmAnimUtils

def AddValidObjectToList( objectList, obj ):
    if ( obj != None ): objectList.append( obj )
    
def HideControlGroups( rig, rootGroup, *groupNames ):
    for name in groupNames:    
        group = rootGroup.FindChildByName( name, False )
        if ( group != None ):
            rig.HideControlGroup( group )

def ComputeVectorBetweenBones( boneA, boneB, scaleFactor ):
    
    vPosA = vs.Vector( 0, 0, 0 )
    boneA.GetAbsPosition( vPosA )
    
    vPosB = vs.Vector( 0, 0, 0 )
    boneB.GetAbsPosition( vPosB )
    
    vDir = vs.Vector( 0, 0, 0 )
    vs.mathlib.VectorSubtract( vPosB, vPosA, vDir )
    vDir.NormalizeInPlace()
    
    vScaledDir = vs.Vector( 0, 0, 0 )
    vs.mathlib.VectorScale( vDir, scaleFactor, vScaledDir )    
    
    return vScaledDir
		
def CreateOrientConstraint( target, slave, bCreateControls=True, group=None ) :
    if ( target == None ):
        return

    targetDag = sfmUtils.GetDagFromNameOrObject( target )
    slaveDag = sfmUtils.GetDagFromNameOrObject( slave )
    
    sfm.PushSelection()
    sfmUtils.SelectDagList( [ targetDag, slaveDag ] )
    
    orientConstraintTarget = sfm.OrientConstraint( controls=bCreateControls )
    
    if ( group != None ):
        if ( orientConstraintTarget != None ):
            orientWeightControl = orientConstraintTarget.FindWeightControl()
            if ( orientWeightControl != None ):
                group.AddControl( orientWeightControl )
            
    sfm.PopSelection()
    return
	
def CreatePointConstraint( target, slave, bCreateControls=True, group=None ) :
    if ( target == None ):
        return

    targetDag = sfmUtils.GetDagFromNameOrObject( target )
    slaveDag = sfmUtils.GetDagFromNameOrObject( slave )
    
    sfm.PushSelection()
    sfmUtils.SelectDagList( [ targetDag, slaveDag ] )
    
    pointConstraintTarget = sfm.PointConstraint( controls=bCreateControls )
    
    if ( group != None ):
        if ( pointConstraintTarget != None ):
            pointWeightControl = pointConstraintTarget.FindWeightControl()
            if ( pointWeightControl != None ):
                group.AddControl( pointWeightControl )
            
    sfm.PopSelection()
    return
	
def BuildRig():
    
    # Get the currently selected animation set and shot
    shot = sfm.GetCurrentShot()
    animSet = sfm.GetCurrentAnimationSet()
    gameModel = animSet.gameModel
    rootGroup = animSet.GetRootControlGroup()
    
    # Start the biped rig to which all of the controls and constraints will be added
    rig = sfm.BeginRig( "rig_bms_" + animSet.GetName() );
    if ( rig == None ):
        return
    
    # Change the operation mode to passthrough so changes chan be made temporarily
    sfm.SetOperationMode( "Pass" )
    
    # Move everything into the reference pose
    sfm.SelectAll()
    sfm.SetReferencePose()

    isBullsquid = False
    isHoundeye = False
    isGarg = False
    isAGrunt = False
    isHAssassin = False
    isLoader = False
				
    if ( gameModel == None ) :
		raise Exception("Unable to find gameModel...")

    if ( gameModel.GetModelName() == "models/xenians/bullsquid.mdl" ) :
		isBullsquid = True
		
    if ( gameModel.GetModelName() == "models/xenians/houndeye.mdl" ) :
		isHoundeye = True
		
    if ( gameModel.GetModelName() == "models/xenians/garg.mdl" ) :
		isGarg = True
		
    if ( 	gameModel.GetModelName() == "models/xenians/agrunt.mdl" or
			gameModel.GetModelName() == "models/xenians/agrunt_02.mdl" or
			gameModel.GetModelName() == "models/xenians/agrunt_unarmored.mdl") :
		isAGrunt = True
		
    if ( gameModel.GetModelName() == "models/humans/hassassin.mdl" ) :
		isHAssassin = True
		
    if ( gameModel.GetModelName() == "models/props_vehicles/loader.mdl" ) :
		isLoader = True
		
    if ( isBullsquid == False 
	and isHoundeye == False 
	and isGarg == False 
	and isAGrunt == False 
	and isHAssassin == False
	and isLoader == False ) :
		raise Exception("Sorry! This either isn't a Black Mesa model or there's no rig support for it yet! (" + gameModel.GetModelName() + ")")
		
    if ( isBullsquid ):
		boneRoot      	= sfmUtils.FindFirstDag( [ "RootTransform" ], True )
		boneBase      	= sfmUtils.FindFirstDag( [ "joint_Base" ], True )
		
		boneHead      	= sfmUtils.FindFirstDag( [ "HEAD" ], True )
		boneJaw      	= sfmUtils.FindFirstDag( [ "LOWER_JAW" ], True )
		
		boneHipR    	= sfmUtils.FindFirstDag( [ "Hip_L" ], True )
		boneKneeR    	= sfmUtils.FindFirstDag( [ "Knee_L" ], True )
		boneAnkleR    	= sfmUtils.FindFirstDag( [ "Ankle_L" ], True )
		boneToeR    	= sfmUtils.FindFirstDag( [ "Toe_L" ], True )

		boneHipL    	= sfmUtils.FindFirstDag( [ "Hip_R" ], True )
		boneKneeL    	= sfmUtils.FindFirstDag( [ "Knee_R" ], True )
		boneAnkleL    	= sfmUtils.FindFirstDag( [ "Ankle_R" ], True )
		boneToeL    	= sfmUtils.FindFirstDag( [ "Toe_R" ], True )
		
		boneTent12_1	= sfmUtils.FindFirstDag( [ "Tentacle_1200_1" ], True )
		boneTent12_2	= sfmUtils.FindFirstDag( [ "Tentacle_1200_2" ], True )
		boneTent1_1		= sfmUtils.FindFirstDag( [ "Tentacle_100_1" ], True )
		boneTent1_2		= sfmUtils.FindFirstDag( [ "Tentacle_100_2" ], True )
		boneTent4_1		= sfmUtils.FindFirstDag( [ "Tentacle_400_1" ], True )
		boneTent4_2		= sfmUtils.FindFirstDag( [ "Tentacle_400_2" ], True )
		boneTent6_1		= sfmUtils.FindFirstDag( [ "Tentacle_600_1" ], True )
		boneTent6_2		= sfmUtils.FindFirstDag( [ "Tentacle_600_2" ], True )
		boneTent8_1		= sfmUtils.FindFirstDag( [ "Tentacle_800_1" ], True )
		boneTent8_2		= sfmUtils.FindFirstDag( [ "Tentacle_800_2" ], True )
		boneTent11_1	= sfmUtils.FindFirstDag( [ "Tentacle_1100_1" ], True )
		boneTent11_2	= sfmUtils.FindFirstDag( [ "Tentacle_1100_2" ], True )
    
		boneTail1      	= sfmUtils.FindFirstDag( [ "Tail_1" ], True )
		boneTail2      	= sfmUtils.FindFirstDag( [ "Tail_2" ], True )
		boneTail3      	= sfmUtils.FindFirstDag( [ "Tail_3" ], True )
		boneTail4      	= sfmUtils.FindFirstDag( [ "Tail_4" ], True )
		boneTail5      	= sfmUtils.FindFirstDag( [ "Tail_5" ], True )

    if ( isHoundeye ):
		boneRoot      	= sfmUtils.FindFirstDag( [ "RootTransform" ], True )
		boneBase      	= sfmUtils.FindFirstDag( [ "ROOT" ], True )
		boneHead      	= sfmUtils.FindFirstDag( [ "HEAD" ], True )
		boneMouth      	= sfmUtils.FindFirstDag( [ "Mouth" ], True )
		boneMouth1      = sfmUtils.FindFirstDag( [ "Mouth1" ], True )
		boneMouth2      = sfmUtils.FindFirstDag( [ "Mouth2" ], True )
		
		boneSpine1      = sfmUtils.FindFirstDag( [ "Spine1" ], True )
		boneSpine2      = sfmUtils.FindFirstDag( [ "Spine2" ], True )
		
		boneLegR1		= sfmUtils.FindFirstDag( [ "LegL1" ], True )
		boneLegR2		= sfmUtils.FindFirstDag( [ "LegL2" ], True )
		boneLegR3		= sfmUtils.FindFirstDag( [ "LegL3" ], True )
		
		boneLegL1		= sfmUtils.FindFirstDag( [ "LegR1" ], True )
		boneLegL2		= sfmUtils.FindFirstDag( [ "LegR2" ], True )
		boneLegL3		= sfmUtils.FindFirstDag( [ "LegR3" ], True )
		
		boneLegB1		= sfmUtils.FindFirstDag( [ "Leg_back1" ], True )
		boneLegB2		= sfmUtils.FindFirstDag( [ "Leg_back2" ], True )
		boneLegB3		= sfmUtils.FindFirstDag( [ "Leg_back3" ], True )
		
    if ( isGarg ):
		boneRoot      	= sfmUtils.FindFirstDag( [ "RootTransform" ], True )
		boneBase      	= sfmUtils.FindFirstDag( [ "Root" ], True )
		
		boneHead      	= sfmUtils.FindFirstDag( [ "Head" ], True )
		boneHeadNub     = sfmUtils.FindFirstDag( [ "HeadNub" ], True )
		boneJaw     	= sfmUtils.FindFirstDag( [ "JawLower" ], True )
		
		boneSpine1      = sfmUtils.FindFirstDag( [ "Spine01" ], True )
		boneSpine2      = sfmUtils.FindFirstDag( [ "Spine02" ], True )
		boneSpine3      = sfmUtils.FindFirstDag( [ "Spine03" ], True )
		boneSpine4      = sfmUtils.FindFirstDag( [ "Spine04" ], True )
		
		boneLegR1		= sfmUtils.FindFirstDag( [ "UpperLegR" ], True )
		boneLegR2		= sfmUtils.FindFirstDag( [ "MiddleLegR" ], True )
		boneLegR3		= sfmUtils.FindFirstDag( [ "LowerLegR" ], True )
		
		boneLegL1		= sfmUtils.FindFirstDag( [ "UpperLegL" ], True )
		boneLegL2		= sfmUtils.FindFirstDag( [ "MiddleLegL" ], True )
		boneLegL3		= sfmUtils.FindFirstDag( [ "LowerLegL" ], True )
		
		boneArmR1		= sfmUtils.FindFirstDag( [ "UpperArmR" ], True )
		boneArmR2		= sfmUtils.FindFirstDag( [ "LowerArmR" ], True )
		boneArmR3		= sfmUtils.FindFirstDag( [ "LowerArmRNub" ], True )
		boneArmRClaw1	= sfmUtils.FindFirstDag( [ "ClawUpperR" ], True )
		boneArmRClaw2	= sfmUtils.FindFirstDag( [ "ClawLowerR" ], True )
		
		boneArmL1		= sfmUtils.FindFirstDag( [ "UpperArmL" ], True )
		boneArmL2		= sfmUtils.FindFirstDag( [ "LowerArmL" ], True )
		boneArmL3		= sfmUtils.FindFirstDag( [ "LowerArmNubL" ], True )
		boneArmLClaw1	= sfmUtils.FindFirstDag( [ "ClawUpperL" ], True )
		boneArmLClaw2	= sfmUtils.FindFirstDag( [ "ClawLowerL" ], True )
		
		boneClawR1		= sfmUtils.FindFirstDag( [ "TinyArmUpperR" ], True )
		boneClawR2		= sfmUtils.FindFirstDag( [ "TinyArmLowerR" ], True )
		
		boneClawRFinger1_1	= sfmUtils.FindFirstDag( [ "FingerRUpperR01" ], True )
		boneClawRFinger1_2	= sfmUtils.FindFirstDag( [ "FingerRUpperR02" ], True )
		boneClawRFinger1_3	= sfmUtils.FindFirstDag( [ "FingerRUpperR03" ], True )
		boneClawRFinger2_1	= sfmUtils.FindFirstDag( [ "FingerRUpperL01" ], True )
		boneClawRFinger2_2	= sfmUtils.FindFirstDag( [ "FingerRUpperL02" ], True )
		boneClawRFinger2_3	= sfmUtils.FindFirstDag( [ "FingerRUpperL03" ], True )
		boneClawRFinger3_1	= sfmUtils.FindFirstDag( [ "FingerRLower01" ], True )
		boneClawRFinger3_2	= sfmUtils.FindFirstDag( [ "FingerRLower02" ], True )
		boneClawRFinger3_3	= sfmUtils.FindFirstDag( [ "FingerRLower03" ], True )
		
		boneClawL1		= sfmUtils.FindFirstDag( [ "TinyArmUpperL" ], True )
		boneClawL2		= sfmUtils.FindFirstDag( [ "TinyArmLowerL" ], True )
		
		boneClawLFinger1_1	= sfmUtils.FindFirstDag( [ "FingerLUpperR01" ], True )
		boneClawLFinger1_2	= sfmUtils.FindFirstDag( [ "FingerLUpperR02" ], True )
		boneClawLFinger1_3	= sfmUtils.FindFirstDag( [ "FingerLUpperR03" ], True )
		boneClawLFinger2_1	= sfmUtils.FindFirstDag( [ "FingerLUpperL01" ], True )
		boneClawLFinger2_2	= sfmUtils.FindFirstDag( [ "FingerLUpperL02" ], True )
		boneClawLFinger2_3	= sfmUtils.FindFirstDag( [ "FingerLUpperL03" ], True )
		boneClawLFinger3_1	= sfmUtils.FindFirstDag( [ "FingerLLower01" ], True )
		boneClawLFinger3_2	= sfmUtils.FindFirstDag( [ "FingerLLower02" ], True )
		boneClawLFinger3_3	= sfmUtils.FindFirstDag( [ "FingerLLower03" ], True )

    if ( isAGrunt ):
		boneRoot      	= sfmUtils.FindFirstDag( [ "RootTransform" ], True )
		boneBase      	= sfmUtils.FindFirstDag( [ "ValveBiped.hips" ], True )
		boneHead      	= sfmUtils.FindFirstDag( [ "ValveBiped.head" ], True )
		boneJawL1      	= sfmUtils.FindFirstDag( [ "jawLeft01" ], True )
		boneJawL2      	= sfmUtils.FindFirstDag( [ "jawLeft02" ], True )
		boneJawR1      	= sfmUtils.FindFirstDag( [ "jawRight01" ], True )
		boneJawR2      	= sfmUtils.FindFirstDag( [ "jawRight02" ], True )
		
		boneSpine1      = sfmUtils.FindFirstDag( [ "ValveBiped.Spine1" ], True )
		boneSpine2      = sfmUtils.FindFirstDag( [ "ValveBiped.Spine2" ], True )
		boneSpine3      = sfmUtils.FindFirstDag( [ "ValveBiped.Spine3" ], True )
		boneSpine4      = sfmUtils.FindFirstDag( [ "ValveBiped.Spine4" ], True )
		
		boneLegL1		= sfmUtils.FindFirstDag( [ "ValveBiped.leg_bone1_L" ], True )
		boneLegL2		= sfmUtils.FindFirstDag( [ "ValveBiped.leg_bone2_L" ], True )
		boneLegL3		= sfmUtils.FindFirstDag( [ "ValveBiped.leg_bone3_L" ], True )
		boneLegLToe		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Toe0" ], True )
		
		boneLegR1		= sfmUtils.FindFirstDag( [ "ValveBiped.leg_bone1_R" ], True )
		boneLegR2		= sfmUtils.FindFirstDag( [ "ValveBiped.leg_bone2_R" ], True )
		boneLegR3		= sfmUtils.FindFirstDag( [ "ValveBiped.leg_bone3_R" ], True )
		boneLegRToe		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Toe0" ], True )
		
		boneArmL1		= sfmUtils.FindFirstDag( [ "ValveBiped.arm1_L" ], True )
		boneArmL2		= sfmUtils.FindFirstDag( [ "ValveBiped.arm2_L" ], True )
		boneArmL3		= sfmUtils.FindFirstDag( [ "ValveBiped.hand1_L" ], True )
		
		boneArmR1		= sfmUtils.FindFirstDag( [ "ValveBiped.arm1_R" ], True )
		boneArmR2		= sfmUtils.FindFirstDag( [ "ValveBiped.arm2_R" ], True )
		boneArmR3		= sfmUtils.FindFirstDag( [ "ValveBiped.hand1_R" ], True )
		
		boneArmM1		= sfmUtils.FindFirstDag( [ "ValveBiped.bone" ], True )
		boneArmM2		= sfmUtils.FindFirstDag( [ "ValveBiped.bone1" ], True )
		boneArmM3		= sfmUtils.FindFirstDag( [ "ValveBiped.bone2" ], True )
		
    if ( isHAssassin ):
		boneRoot      	= sfmUtils.FindFirstDag( [ "RootTransform" ], True )
		boneBase      	= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Pelvis" ], True )
		boneHead      	= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Head1" ], True )
		
		boneSpine1      = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Spine" ], True )
		boneSpine2      = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Spine1" ], True )
		boneSpine3      = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Spine2" ], True )
		boneSpine4      = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Spine4" ], True )
		
		boneLegL1		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Thigh" ], True )
		boneLegL2		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Calf" ], True )
		boneLegL3		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Foot" ], True )
		
		boneLegR1		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Thigh" ], True )
		boneLegR2		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Calf" ], True )
		boneLegR3		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Foot" ], True )
		
		boneArmL1		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_UpperArm" ], True )
		boneArmL2		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Forearm" ], True )
		boneArmL3		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Hand" ], True )
		
		boneArmR1		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_UpperArm" ], True )
		boneArmR2		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Forearm" ], True )
		boneArmR3		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Hand" ], True )
		
    if ( isLoader ):
		boneRoot      	= sfmUtils.FindFirstDag( [ "RootTransform" ], True )
		boneBase      	= sfmUtils.FindFirstDag( [ "ROOT" ], True )
		boneLower      	= sfmUtils.FindFirstDag( [ "Lower_Body" ], True )
		boneUpper      	= sfmUtils.FindFirstDag( [ "UpperBody" ], True )
		
		boneLegFL_Swivel 	= sfmUtils.FindFirstDag( [ "LegFL_Swivel" ], True )
		boneLegFL_01 		= sfmUtils.FindFirstDag( [ "LegFL_01" ], True )
		boneLegFL_02 		= sfmUtils.FindFirstDag( [ "LegFL_02" ], True )
		boneLegFL_Piston1	= sfmUtils.FindFirstDag( [ "LegFL_Piston01" ], True )
		boneLegFL_Piston2	= sfmUtils.FindFirstDag( [ "LegFL_Piston02" ], True )
		boneLegFL_Extend	= sfmUtils.FindFirstDag( [ "LegFL_Extend" ], True )
		boneLegFL_Foot		= sfmUtils.FindFirstDag( [ "LegFL_Foot" ], True )
		
		boneLegFR_Swivel 	= sfmUtils.FindFirstDag( [ "LegFR_Swivel" ], True )
		boneLegFR_01 		= sfmUtils.FindFirstDag( [ "LegFR_01" ], True )
		boneLegFR_02 		= sfmUtils.FindFirstDag( [ "LegFR_02" ], True )
		boneLegFR_Piston1	= sfmUtils.FindFirstDag( [ "LegFR_Piston01" ], True )
		boneLegFR_Piston2	= sfmUtils.FindFirstDag( [ "LegFR_Piston02" ], True )
		boneLegFR_Extend	= sfmUtils.FindFirstDag( [ "LegFR_Extend" ], True )
		boneLegFR_Foot		= sfmUtils.FindFirstDag( [ "LegFR_Foot" ], True )
		
		boneLegBL_Swivel 	= sfmUtils.FindFirstDag( [ "LegBL_Swivel" ], True )
		boneLegBL_01 		= sfmUtils.FindFirstDag( [ "LegBL_01" ], True )
		boneLegBL_02 		= sfmUtils.FindFirstDag( [ "LegBL_02" ], True )
		boneLegBL_Piston1	= sfmUtils.FindFirstDag( [ "LegBL_Piston01" ], True )
		boneLegBL_Piston2	= sfmUtils.FindFirstDag( [ "LegBL_Piston02" ], True )
		boneLegBL_Extend	= sfmUtils.FindFirstDag( [ "LegBL_Extend" ], True )
		boneLegBL_Foot		= sfmUtils.FindFirstDag( [ "LegBL_Foot" ], True )
		
		boneLegBR_Swivel 	= sfmUtils.FindFirstDag( [ "LegBR_Swivel" ], True )
		boneLegBR_01 		= sfmUtils.FindFirstDag( [ "LegBR_01" ], True )
		boneLegBR_02 		= sfmUtils.FindFirstDag( [ "LegBR_02" ], True )
		boneLegBR_Piston1	= sfmUtils.FindFirstDag( [ "LegBR_Piston01" ], True )
		boneLegBR_Piston2	= sfmUtils.FindFirstDag( [ "LegBR_Piston02" ], True )
		boneLegBR_Extend	= sfmUtils.FindFirstDag( [ "LegBR_Extend" ], True )
		boneLegBR_Foot		= sfmUtils.FindFirstDag( [ "LegBR_Foot" ], True )
		
		boneArmL_1 			= sfmUtils.FindFirstDag( [ "ArmL_01" ], True )
		boneArmL_2 			= sfmUtils.FindFirstDag( [ "ArmL_02" ], True )
		boneArmL_3 			= sfmUtils.FindFirstDag( [ "ArmL_03" ], True )
		boneArmL_4 			= sfmUtils.FindFirstDag( [ "ArmL_04" ], True )
		boneArmL_5 			= sfmUtils.FindFirstDag( [ "ArmL_05" ], True )
		boneArmL_6 			= sfmUtils.FindFirstDag( [ "ArmL_06" ], True )
		
		boneArmR_1 			= sfmUtils.FindFirstDag( [ "ArmR_01" ], True )
		boneArmR_2 			= sfmUtils.FindFirstDag( [ "ArmR_02" ], True )
		boneArmR_3 			= sfmUtils.FindFirstDag( [ "ArmR_03" ], True )
		boneArmR_4 			= sfmUtils.FindFirstDag( [ "ArmR_04" ], True )
		boneArmR_5 			= sfmUtils.FindFirstDag( [ "ArmR_05" ], True )
		boneArmR_6 			= sfmUtils.FindFirstDag( [ "ArmR_06" ], True )
		
		
    if ( isBullsquid ):
		rigRoot    		= sfmUtils.CreateConstrainedHandle( "rig_root",     	boneRoot,    	bCreateControls=False )
		rigBase    		= sfmUtils.CreateConstrainedHandle( "rig_base",    		boneBase,    	bCreateControls=False )
		
		rigHead    		= sfmUtils.CreateConstrainedHandle( "rig_head",   		boneHead,    	bCreateControls=False )
		rigJaw    		= sfmUtils.CreateConstrainedHandle( "rig_jaw",   		boneJaw,    	bCreateControls=False )
		
		rigHipR    		= sfmUtils.CreateConstrainedHandle( "rig_hip_r",    	boneHipR,    	bCreateControls=False )
		rigKneeR    	= sfmUtils.CreateConstrainedHandle( "rig_knee_r",    	boneKneeR,    	bCreateControls=False )
		rigAnkleR    	= sfmUtils.CreateConstrainedHandle( "rig_ankle_r",    	boneAnkleR,    	bCreateControls=False )
		rigToeR    		= sfmUtils.CreateConstrainedHandle( "rig_toe_r",    	boneToeR,    	bCreateControls=False )
		
		rigHipL    		= sfmUtils.CreateConstrainedHandle( "rig_hip_l",    	boneHipL,    	bCreateControls=False )
		rigKneeL    	= sfmUtils.CreateConstrainedHandle( "rig_knee_l",    	boneKneeL,    	bCreateControls=False )
		rigAnkleL    	= sfmUtils.CreateConstrainedHandle( "rig_ankle_l",    	boneAnkleL,    	bCreateControls=False )
		rigToeL    		= sfmUtils.CreateConstrainedHandle( "rig_toe_l",    	boneToeL,    	bCreateControls=False )
		
		rigTent12_1    	= sfmUtils.CreateConstrainedHandle( "rig_tent_12_1", 	boneTent12_1, 	bCreateControls=False )
		rigTent12_2    	= sfmUtils.CreateConstrainedHandle( "rig_tent_12_2",  	boneTent12_2, 	bCreateControls=False )
		rigTent1_1    	= sfmUtils.CreateConstrainedHandle( "rig_tent_1_1", 	boneTent1_1, 	bCreateControls=False )
		rigTent1_2    	= sfmUtils.CreateConstrainedHandle( "rig_tent_1_2",  	boneTent1_2, 	bCreateControls=False )
		rigTent4_1    	= sfmUtils.CreateConstrainedHandle( "rig_tent_4_1", 	boneTent4_1, 	bCreateControls=False )
		rigTent4_2    	= sfmUtils.CreateConstrainedHandle( "rig_tent_4_2",  	boneTent4_2, 	bCreateControls=False )
		rigTent6_1    	= sfmUtils.CreateConstrainedHandle( "rig_tent_6_1", 	boneTent6_1, 	bCreateControls=False )
		rigTent6_2    	= sfmUtils.CreateConstrainedHandle( "rig_tent_6_2",  	boneTent6_2, 	bCreateControls=False )
		rigTent8_1    	= sfmUtils.CreateConstrainedHandle( "rig_tent_8_1", 	boneTent8_1, 	bCreateControls=False )
		rigTent8_2    	= sfmUtils.CreateConstrainedHandle( "rig_tent_8_2",  	boneTent8_2, 	bCreateControls=False )
		rigTent11_1    	= sfmUtils.CreateConstrainedHandle( "rig_tent_11_1", 	boneTent11_1, 	bCreateControls=False )
		rigTent11_2    	= sfmUtils.CreateConstrainedHandle( "rig_tent_11_2",  	boneTent11_2, 	bCreateControls=False ) 
		
		rigTail1 		= sfmUtils.CreateConstrainedHandle( "rig_tail_1",		boneTail1,		bCreateControls=False )
		rigTail2 		= sfmUtils.CreateConstrainedHandle( "rig_tail_2",		boneTail2,		bCreateControls=False )
		rigTail3 		= sfmUtils.CreateConstrainedHandle( "rig_tail_3",		boneTail3,		bCreateControls=False )
		rigTail4 		= sfmUtils.CreateConstrainedHandle( "rig_tail_4",		boneTail4,		bCreateControls=False )
		rigTail5 		= sfmUtils.CreateConstrainedHandle( "rig_tail_5",		boneTail5,		bCreateControls=False )
		
		vKneeOffset 	= ComputeVectorBetweenBones( boneBase, boneTail1, 16 )
		
		rigKneeHelperR   	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_r",  	rigKneeR, 	vKneeOffset,  	bCreateControls=False )     
		rigKneeHelperL   	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_l",  	rigKneeL, 	vKneeOffset,  	bCreateControls=False )  
		
		## All, except FOOT helpers.
		allRigHandles = [ 	rigRoot, rigBase, 
							rigHead, rigJaw,
							rigHipR, rigKneeR, rigAnkleR, rigToeR, rigKneeHelperR,
							rigHipL, rigKneeL, rigAnkleL, rigToeL, rigKneeHelperL,
							rigTent12_1, rigTent12_2, rigTent1_1, rigTent1_2, rigTent4_1, rigTent4_2, 
							rigTent6_1, rigTent6_2, rigTent8_1, rigTent8_2, rigTent11_1, rigTent11_2,
							rigTail1, rigTail2, rigTail3, rigTail4, rigTail5 ] ;
    
    if ( isHoundeye ):
		rigRoot    		= sfmUtils.CreateConstrainedHandle( "rig_root",     	boneRoot,    	bCreateControls=False )
		rigBase    		= sfmUtils.CreateConstrainedHandle( "rig_base",    		boneBase,    	bCreateControls=False )
		rigHead    		= sfmUtils.CreateConstrainedHandle( "rig_head",    		boneHead,    	bCreateControls=False )
		rigMouth   		= sfmUtils.CreateConstrainedHandle( "rig_mouth",    	boneMouth,    	bCreateControls=False )
		rigMouth1   	= sfmUtils.CreateConstrainedHandle( "rig_mouth_upper",  boneMouth1,    	bCreateControls=False )
		rigMouth2   	= sfmUtils.CreateConstrainedHandle( "rig_mouth_lower",  boneMouth2,    	bCreateControls=False )
		
		rigSpine1    	= sfmUtils.CreateConstrainedHandle( "rig_spine_1",    	boneSpine1,    	bCreateControls=False )
		rigSpine2    	= sfmUtils.CreateConstrainedHandle( "rig_spine_2",    	boneSpine2,    	bCreateControls=False )
		
		rigLegR1    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_1",    	boneLegR1,    	bCreateControls=False )
		rigLegR2    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_2",    	boneLegR2,    	bCreateControls=False )
		rigLegR3    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_3",    	boneLegR3,    	bCreateControls=False )
		
		rigLegL1    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_1",    	boneLegL1,    	bCreateControls=False )
		rigLegL2    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_2",    	boneLegL2,    	bCreateControls=False )
		rigLegL3    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_3",    	boneLegL3,    	bCreateControls=False )
		
		rigLegB1    	= sfmUtils.CreateConstrainedHandle( "rig_bleg_1",    	boneLegB1,    	bCreateControls=False )
		rigLegB2    	= sfmUtils.CreateConstrainedHandle( "rig_bleg_2",    	boneLegB2,    	bCreateControls=False )
		rigLegB3    	= sfmUtils.CreateConstrainedHandle( "rig_bleg_3",    	boneLegB3,    	bCreateControls=False )
		
		vKneeOffset 	= ComputeVectorBetweenBones( boneHead, boneBase, 16 )
		
		rigKneeHelperR   	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_r",  	rigLegR2, 	vKneeOffset,  	bCreateControls=False )   
		rigKneeHelperL   	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_l",  	rigLegL2, 	vKneeOffset,  	bCreateControls=False )   
		rigKneeHelperB   	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_b",  	rigLegB2, 	vKneeOffset,  	bCreateControls=False )   
		
		allRigHandles = [ 	rigRoot, rigBase, rigHead, rigMouth, rigMouth1, rigMouth2,
							rigSpine1, rigSpine2,
							rigLegR1, rigLegR2, rigLegR3, rigKneeHelperR ,	
							rigLegL1, rigLegL2, rigLegL3, rigKneeHelperL ,	
							rigLegB1, rigLegB2, rigLegB3, rigKneeHelperB ] ;	
    
    if ( isGarg ):
		rigRoot    		= sfmUtils.CreateConstrainedHandle( "rig_root",     	boneRoot,    	bCreateControls=False )
		rigBase    		= sfmUtils.CreateConstrainedHandle( "rig_base",    		boneBase,    	bCreateControls=False )
		
		rigHead    		= sfmUtils.CreateConstrainedHandle( "rig_head",    		boneHead,    	bCreateControls=False )
		rigHeadNub 		= sfmUtils.CreateConstrainedHandle( "rig_head_nub",   	boneHeadNub,    bCreateControls=False )
		rigJaw 			= sfmUtils.CreateConstrainedHandle( "rig_jaw",   		boneJaw,    	bCreateControls=False )
		
		rigSpine1    	= sfmUtils.CreateConstrainedHandle( "rig_spine_1",    	boneSpine1,    	bCreateControls=False )
		rigSpine2    	= sfmUtils.CreateConstrainedHandle( "rig_spine_2",    	boneSpine2,    	bCreateControls=False )
		rigSpine3    	= sfmUtils.CreateConstrainedHandle( "rig_spine_3",    	boneSpine3,    	bCreateControls=False )
		rigSpine4   	= sfmUtils.CreateConstrainedHandle( "rig_spine_4",    	boneSpine4,    	bCreateControls=False )
		
		rigLegR1    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_1",    	boneLegR1,    	bCreateControls=False )
		rigLegR2    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_2",    	boneLegR2,    	bCreateControls=False )
		rigLegR3    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_3",    	boneLegR3,    	bCreateControls=False )
		
		rigLegL1    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_1",    	boneLegL1,    	bCreateControls=False )
		rigLegL2    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_2",    	boneLegL2,    	bCreateControls=False )
		rigLegL3    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_3",    	boneLegL3,    	bCreateControls=False )
		
		rigArmR1    	= sfmUtils.CreateConstrainedHandle( "rig_rarm_1",    	boneArmR1,    	bCreateControls=False )
		rigArmR2    	= sfmUtils.CreateConstrainedHandle( "rig_rarm_2",    	boneArmR2,    	bCreateControls=False )
		rigArmR3    	= sfmUtils.CreateConstrainedHandle( "rig_rarm_3",    	boneArmR3,    	bCreateControls=False )
		rigArmRClaw1    = sfmUtils.CreateConstrainedHandle( "rig_rarm_claw_upper",   boneArmRClaw1,    	bCreateControls=False )
		rigArmRClaw2    = sfmUtils.CreateConstrainedHandle( "rig_rarm_claw_lower",   boneArmRClaw2,    	bCreateControls=False )
		
		rigArmL1    	= sfmUtils.CreateConstrainedHandle( "rig_larm_1",    	boneArmL1,    	bCreateControls=False )
		rigArmL2    	= sfmUtils.CreateConstrainedHandle( "rig_larm_2",    	boneArmL2,    	bCreateControls=False )
		rigArmL3    	= sfmUtils.CreateConstrainedHandle( "rig_larm_3",    	boneArmL3,    	bCreateControls=False )
		rigArmLClaw1    = sfmUtils.CreateConstrainedHandle( "rig_larm_claw_upper",   boneArmLClaw1,    	bCreateControls=False )
		rigArmLClaw2    = sfmUtils.CreateConstrainedHandle( "rig_larm_claw_lower",   boneArmLClaw2,    	bCreateControls=False )
		
		rigClawR1    	= sfmUtils.CreateConstrainedHandle( "rig_rclaw_1",    	boneClawR1,    	bCreateControls=False )
		rigClawR2    	= sfmUtils.CreateConstrainedHandle( "rig_rclaw_2",    	boneClawR2,    	bCreateControls=False )
		
		rigClawRFinger1_1   = sfmUtils.CreateConstrainedHandle( "rig_rclaw_finger1_1", boneClawRFinger1_1, bCreateControls=False )
		rigClawRFinger1_2   = sfmUtils.CreateConstrainedHandle( "rig_rclaw_finger1_2", boneClawRFinger1_2, bCreateControls=False )
		rigClawRFinger1_3   = sfmUtils.CreateConstrainedHandle( "rig_rclaw_finger1_3", boneClawRFinger1_3, bCreateControls=False )
		rigClawRFinger2_1   = sfmUtils.CreateConstrainedHandle( "rig_rclaw_finger2_1", boneClawRFinger2_1, bCreateControls=False )
		rigClawRFinger2_2   = sfmUtils.CreateConstrainedHandle( "rig_rclaw_finger2_2", boneClawRFinger2_2, bCreateControls=False )
		rigClawRFinger2_3   = sfmUtils.CreateConstrainedHandle( "rig_rclaw_finger2_3", boneClawRFinger2_3, bCreateControls=False )
		rigClawRFinger3_1   = sfmUtils.CreateConstrainedHandle( "rig_rclaw_finger3_1", boneClawRFinger3_1, bCreateControls=False )
		rigClawRFinger3_2   = sfmUtils.CreateConstrainedHandle( "rig_rclaw_finger3_2", boneClawRFinger3_2, bCreateControls=False )
		rigClawRFinger3_3   = sfmUtils.CreateConstrainedHandle( "rig_rclaw_finger3_3", boneClawRFinger3_3, bCreateControls=False )
		
		rigClawL1    	= sfmUtils.CreateConstrainedHandle( "rig_lclaw_1",    	boneClawL1,    	bCreateControls=False )
		rigClawL2    	= sfmUtils.CreateConstrainedHandle( "rig_lclaw_2",    	boneClawL2,    	bCreateControls=False )
		
		rigClawLFinger1_1   = sfmUtils.CreateConstrainedHandle( "rig_lclaw_finger1_1", boneClawLFinger1_1, bCreateControls=False )
		rigClawLFinger1_2   = sfmUtils.CreateConstrainedHandle( "rig_lclaw_finger1_2", boneClawLFinger1_2, bCreateControls=False )
		rigClawLFinger1_3   = sfmUtils.CreateConstrainedHandle( "rig_lclaw_finger1_3", boneClawLFinger1_3, bCreateControls=False )
		rigClawLFinger2_1   = sfmUtils.CreateConstrainedHandle( "rig_lclaw_finger2_1", boneClawLFinger2_1, bCreateControls=False )
		rigClawLFinger2_2   = sfmUtils.CreateConstrainedHandle( "rig_lclaw_finger2_2", boneClawLFinger2_2, bCreateControls=False )
		rigClawLFinger2_3   = sfmUtils.CreateConstrainedHandle( "rig_lclaw_finger2_3", boneClawLFinger2_3, bCreateControls=False )
		rigClawLFinger3_1   = sfmUtils.CreateConstrainedHandle( "rig_lclaw_finger3_1", boneClawLFinger3_1, bCreateControls=False )
		rigClawLFinger3_2   = sfmUtils.CreateConstrainedHandle( "rig_lclaw_finger3_2", boneClawLFinger3_2, bCreateControls=False )
		rigClawLFinger3_3   = sfmUtils.CreateConstrainedHandle( "rig_lclaw_finger3_3", boneClawLFinger3_3, bCreateControls=False )
		
		vKneeOffset 	= ComputeVectorBetweenBones( boneHead, boneHeadNub, 32 )
		vElbowOffset 	= ComputeVectorBetweenBones( boneArmR3, boneArmR2, 35 )
		
		rigKneeHelperR   	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_r",  	rigLegR2, 	vKneeOffset,  	bCreateControls=False )   
		rigKneeHelperL   	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_l",  	rigLegL2, 	vKneeOffset,  	bCreateControls=False )   
		
		rigElbowHelperR   	= sfmUtils.CreateOffsetHandle( "rig_eblow_helper_r",  	rigArmR2, 	vElbowOffset,  	bCreateControls=False )   
		rigElbowHelperL   	= sfmUtils.CreateOffsetHandle( "rig_eblow_helper_l",  	rigArmL2, 	vElbowOffset,  	bCreateControls=False )   
		
		allRigHandles = [ 	rigRoot, rigBase,
							rigHead, rigHeadNub, rigJaw,
							rigSpine1, rigSpine2, rigSpine3, rigSpine4,
							rigLegR1, rigLegR2, rigLegR3, rigKneeHelperR,	
							rigLegL1, rigLegL2, rigLegL3, rigKneeHelperL,
							rigArmR1, rigArmR2, rigArmR3, rigElbowHelperR , rigArmRClaw1, rigArmRClaw2,
							rigArmL1, rigArmL2, rigArmL3, rigElbowHelperL, rigArmLClaw1, rigArmLClaw2,
							rigClawR1, rigClawR2,
							rigClawRFinger1_1, rigClawRFinger1_2, rigClawRFinger1_3,
							rigClawRFinger2_1, rigClawRFinger2_2, rigClawRFinger2_3,
							rigClawRFinger3_1, rigClawRFinger3_2, rigClawRFinger3_3, 
							rigClawL1, rigClawL2,
							rigClawLFinger1_1, rigClawLFinger1_2, rigClawLFinger1_3,
							rigClawLFinger2_1, rigClawLFinger2_2, rigClawLFinger2_3,
							rigClawLFinger3_1, rigClawLFinger3_2, rigClawLFinger3_3, 
							] ;	
       
    if ( isAGrunt ):
		rigRoot    		= sfmUtils.CreateConstrainedHandle( "rig_root",     	boneRoot,    	bCreateControls=False )
		rigBase    		= sfmUtils.CreateConstrainedHandle( "rig_base",    		boneBase,    	bCreateControls=False )
		rigHead    		= sfmUtils.CreateConstrainedHandle( "rig_head",    		boneHead,    	bCreateControls=False )
		rigJawL1    	= sfmUtils.CreateConstrainedHandle( "rig_jaw_l1",    	boneJawL1,    	bCreateControls=False )
		rigJawL2    	= sfmUtils.CreateConstrainedHandle( "rig_jaw_l2",    	boneJawL2,    	bCreateControls=False )
		rigJawR1    	= sfmUtils.CreateConstrainedHandle( "rig_jaw_r1",    	boneJawR1,    	bCreateControls=False )
		rigJawR2    	= sfmUtils.CreateConstrainedHandle( "rig_jaw_r2",    	boneJawR2,    	bCreateControls=False )
		
		rigSpine1    	= sfmUtils.CreateConstrainedHandle( "rig_spine_1",    	boneSpine1,    	bCreateControls=False )
		rigSpine2    	= sfmUtils.CreateConstrainedHandle( "rig_spine_2",    	boneSpine2,    	bCreateControls=False )
		rigSpine3    	= sfmUtils.CreateConstrainedHandle( "rig_spine_3",    	boneSpine3,    	bCreateControls=False )
		rigSpine4    	= sfmUtils.CreateConstrainedHandle( "rig_spine_4",    	boneSpine4,    	bCreateControls=False )
		
		rigLegL1    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_1",    	boneLegL1,    	bCreateControls=False )
		rigLegL2    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_2",    	boneLegL2,    	bCreateControls=False )
		rigLegL3    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_3",    	boneLegL3,    	bCreateControls=False )
		rigLegLToe    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_toe",    	boneLegLToe,    bCreateControls=False )
		
		rigLegR1    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_1",    	boneLegR1,    	bCreateControls=False )
		rigLegR2    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_2",    	boneLegR2,    	bCreateControls=False )
		rigLegR3    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_3",    	boneLegR3,    	bCreateControls=False )	
		rigLegRToe    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_toe",    	boneLegRToe,    bCreateControls=False )	
		
		rigArmL1    	= sfmUtils.CreateConstrainedHandle( "rig_larm1",    	boneArmL1,    	bCreateControls=False )
		rigArmL2    	= sfmUtils.CreateConstrainedHandle( "rig_larm2",    	boneArmL2,    	bCreateControls=False )
		rigArmL3    	= sfmUtils.CreateConstrainedHandle( "rig_larm3",    	boneArmL3,    	bCreateControls=False )
		
		rigArmR1    	= sfmUtils.CreateConstrainedHandle( "rig_rarm1",    	boneArmR1,    	bCreateControls=False )
		rigArmR2    	= sfmUtils.CreateConstrainedHandle( "rig_rarm2",    	boneArmR2,    	bCreateControls=False )
		rigArmR3    	= sfmUtils.CreateConstrainedHandle( "rig_rarm3",    	boneArmR3,    	bCreateControls=False )
		
		rigArmM1    	= sfmUtils.CreateConstrainedHandle( "rig_marm1",    	boneArmM1,    	bCreateControls=False )
		rigArmM2    	= sfmUtils.CreateConstrainedHandle( "rig_marm2",    	boneArmM2,    	bCreateControls=False )
		rigArmM3    	= sfmUtils.CreateConstrainedHandle( "rig_marm3",    	boneArmM3,    	bCreateControls=False )
				
		vElbowOffset 		= ComputeVectorBetweenBones( boneSpine3, boneArmM1, 16 )
		
		rigKneeHelperL  = sfmUtils.CreateOffsetHandle( "rig_knee_helper_l", 	rigLegL2, 		vElbowOffset,	bCreateControls=False )   
		rigKneeHelperR  = sfmUtils.CreateOffsetHandle( "rig_knee_helper_r", 	rigLegR2, 		vElbowOffset,	bCreateControls=False )   
		rigElbowHelperL  = sfmUtils.CreateOffsetHandle( "rig_elbow_helper_l", 	rigArmL2, 		-vElbowOffset,	bCreateControls=False )   
		rigElbowHelperR  = sfmUtils.CreateOffsetHandle( "rig_elbow_helper_r", 	rigArmR2, 		-vElbowOffset,	bCreateControls=False )   
		rigElbowHelperM  = sfmUtils.CreateOffsetHandle( "rig_elbow_helper_m", 	rigArmM2, 		vs.Vector( 0, 0, -10 ),	bCreateControls=False )   
		
		allRigHandles = [ 	rigRoot, rigBase, rigHead, rigJawL1, rigJawL2, rigJawR1, rigJawR2,
							rigSpine1, rigSpine2, rigSpine3, rigSpine4,
							rigLegR1, rigLegR2, rigLegR3, rigLegRToe, rigKneeHelperR,	
							rigLegL1, rigLegL2, rigLegL3, rigLegLToe, rigKneeHelperL,
							rigArmL1, rigArmL2, rigArmL3, rigElbowHelperL,
							rigArmR1, rigArmR2, rigArmR3, rigElbowHelperR,	
							rigArmM1, rigArmM2, rigArmM3, rigElbowHelperM] ;	
    
    if ( isHAssassin ):
		rigRoot    		= sfmUtils.CreateConstrainedHandle( "rig_root",     	boneRoot,    	bCreateControls=False )
		rigBase    		= sfmUtils.CreateConstrainedHandle( "rig_base",    		boneBase,    	bCreateControls=False )
		rigHead    		= sfmUtils.CreateConstrainedHandle( "rig_head",    		boneHead,    	bCreateControls=False )
		
		rigSpine1    	= sfmUtils.CreateConstrainedHandle( "rig_spine_1",    	boneSpine1,    	bCreateControls=False )
		rigSpine2    	= sfmUtils.CreateConstrainedHandle( "rig_spine_2",    	boneSpine2,    	bCreateControls=False )
		rigSpine3    	= sfmUtils.CreateConstrainedHandle( "rig_spine_3",    	boneSpine3,    	bCreateControls=False )
		rigSpine4    	= sfmUtils.CreateConstrainedHandle( "rig_spine_4",    	boneSpine4,    	bCreateControls=False )
		
		rigLegL1    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_1",    	boneLegL1,    	bCreateControls=False )
		rigLegL2    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_2",    	boneLegL2,    	bCreateControls=False )
		rigLegL3    	= sfmUtils.CreateConstrainedHandle( "rig_lleg_3",    	boneLegL3,    	bCreateControls=False )
		
		rigLegR1    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_1",    	boneLegR1,    	bCreateControls=False )
		rigLegR2    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_2",    	boneLegR2,    	bCreateControls=False )
		rigLegR3    	= sfmUtils.CreateConstrainedHandle( "rig_rleg_3",    	boneLegR3,    	bCreateControls=False )	
		
		rigArmL1    	= sfmUtils.CreateConstrainedHandle( "rig_larm_1",    	boneArmL1,    	bCreateControls=False )
		rigArmL2    	= sfmUtils.CreateConstrainedHandle( "rig_larm_2",    	boneArmL2,    	bCreateControls=False )
		rigArmL3    	= sfmUtils.CreateConstrainedHandle( "rig_larm_3",    	boneArmL3,    	bCreateControls=False )
		
		rigArmR1    	= sfmUtils.CreateConstrainedHandle( "rig_rarm_1",    	boneArmR1,    	bCreateControls=False )
		rigArmR2    	= sfmUtils.CreateConstrainedHandle( "rig_rarm_2",    	boneArmR2,    	bCreateControls=False )
		rigArmR3    	= sfmUtils.CreateConstrainedHandle( "rig_rarm_3",    	boneArmR3,    	bCreateControls=False )		
		
		vKneeOffset 	= ComputeVectorBetweenBones( rigSpine1, rigBase, 16 )
		 
		rigKneeHelperL   	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_l",  	rigLegL2, 	vKneeOffset,  	bCreateControls=False ) 
		rigKneeHelperR   	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_r",  	rigLegR2, 	vKneeOffset,  	bCreateControls=False )  
		rigElbowHelperL   	= sfmUtils.CreateOffsetHandle( "rig_elbow_helper_l",  	rigArmL2, 	vKneeOffset,  	bCreateControls=False )    
		rigElbowHelperR   	= sfmUtils.CreateOffsetHandle( "rig_elbow_helper_r",  	rigArmR2, 	-vKneeOffset,  	bCreateControls=False )    
		
		allRigHandles = [ 	rigRoot, rigBase, rigHead,
							rigSpine1, rigSpine2, rigSpine3, rigSpine4,
							rigLegL1, rigLegL2, rigLegL3, rigKneeHelperL,
							rigLegR1, rigLegR2, rigLegR3, rigKneeHelperR,
							rigArmL1, rigArmL2, rigArmL3, rigElbowHelperL,
							rigArmR1, rigArmR2, rigArmR3, rigElbowHelperR ] ;	
    
    if ( isLoader ):
		rigRoot    		= sfmUtils.CreateConstrainedHandle( "rig_root",     	boneRoot,    	bCreateControls=False )
		rigBase    		= sfmUtils.CreateConstrainedHandle( "rig_base",    		boneBase,    	bCreateControls=False )
		rigLower    	= sfmUtils.CreateConstrainedHandle( "rig_lower",    	boneLower,    	bCreateControls=False )
		rigUpper   		= sfmUtils.CreateConstrainedHandle( "rig_upper",    	boneUpper,    	bCreateControls=False )
		
		rigLegFL_Swivel   	= sfmUtils.CreateConstrainedHandle( "rig_legFL_swivel",    	boneLegFL_Swivel,   bCreateControls=False )
		rigLegFL_01   		= sfmUtils.CreateConstrainedHandle( "rig_legFL_01",    		boneLegFL_01,    	bCreateControls=False )
		rigLegFL_02   		= sfmUtils.CreateConstrainedHandle( "rig_legFL_02",    		boneLegFL_02,    	bCreateControls=False )
		rigLegFL_Piston1   	= sfmUtils.CreateConstrainedHandle( "rig_legFL_Piston1",    boneLegFL_Piston1,    	bCreateControls=False )
		rigLegFL_Piston2   	= sfmUtils.CreateConstrainedHandle( "rig_legFL_Piston2",    boneLegFL_Piston2,    	bCreateControls=False )
		rigLegFL_Extend   	= sfmUtils.CreateConstrainedHandle( "rig_legFL_Extend",    	boneLegFL_Extend,    	bCreateControls=False )
		rigLegFL_Foot   	= sfmUtils.CreateConstrainedHandle( "rig_legFL_Foot",    	boneLegFL_Foot,    	bCreateControls=False )
		
		rigLegFR_Swivel   	= sfmUtils.CreateConstrainedHandle( "rig_legFR_swivel",    	boneLegFR_Swivel,   bCreateControls=False )
		rigLegFR_01   		= sfmUtils.CreateConstrainedHandle( "rig_legFR_01",    		boneLegFR_01,    	bCreateControls=False )
		rigLegFR_02   		= sfmUtils.CreateConstrainedHandle( "rig_legFR_02",    		boneLegFR_02,    	bCreateControls=False )
		rigLegFR_Piston1   	= sfmUtils.CreateConstrainedHandle( "rig_legFR_Piston1",    boneLegFR_Piston1,    	bCreateControls=False )
		rigLegFR_Piston2   	= sfmUtils.CreateConstrainedHandle( "rig_legFR_Piston2",    boneLegFR_Piston2,    	bCreateControls=False )
		rigLegFR_Extend   	= sfmUtils.CreateConstrainedHandle( "rig_legFR_Extend",    	boneLegFR_Extend,    	bCreateControls=False )
		rigLegFR_Foot   	= sfmUtils.CreateConstrainedHandle( "rig_legFR_Foot",    	boneLegFR_Foot,    	bCreateControls=False )
		
		rigLegBL_Swivel   	= sfmUtils.CreateConstrainedHandle( "rig_legBL_swivel",    	boneLegBL_Swivel,   bCreateControls=False )
		rigLegBL_01   		= sfmUtils.CreateConstrainedHandle( "rig_legBL_01",    		boneLegBL_01,    	bCreateControls=False )
		rigLegBL_02   		= sfmUtils.CreateConstrainedHandle( "rig_legBL_02",    		boneLegBL_02,    	bCreateControls=False )
		rigLegBL_Piston1   	= sfmUtils.CreateConstrainedHandle( "rig_legBL_Piston1",    boneLegBL_Piston1,    	bCreateControls=False )
		rigLegBL_Piston2   	= sfmUtils.CreateConstrainedHandle( "rig_legBL_Piston2",    boneLegBL_Piston2,    	bCreateControls=False )
		rigLegBL_Extend   	= sfmUtils.CreateConstrainedHandle( "rig_legBL_Extend",    	boneLegBL_Extend,    	bCreateControls=False )
		rigLegBL_Foot   	= sfmUtils.CreateConstrainedHandle( "rig_legBL_Foot",    	boneLegBL_Foot,    	bCreateControls=False )
		
		rigLegBR_Swivel   	= sfmUtils.CreateConstrainedHandle( "rig_legBR_swivel",    	boneLegBR_Swivel,   bCreateControls=False )
		rigLegBR_01   		= sfmUtils.CreateConstrainedHandle( "rig_legBR_01",    		boneLegBR_01,    	bCreateControls=False )
		rigLegBR_02   		= sfmUtils.CreateConstrainedHandle( "rig_legBR_02",    		boneLegBR_02,    	bCreateControls=False )
		rigLegBR_Piston1   	= sfmUtils.CreateConstrainedHandle( "rig_legBR_Piston1",    boneLegBR_Piston1,    	bCreateControls=False )
		rigLegBR_Piston2   	= sfmUtils.CreateConstrainedHandle( "rig_legBR_Piston2",    boneLegBR_Piston2,    	bCreateControls=False )
		rigLegBR_Extend   	= sfmUtils.CreateConstrainedHandle( "rig_legBR_Extend",    	boneLegBR_Extend,    	bCreateControls=False )
		rigLegBR_Foot   	= sfmUtils.CreateConstrainedHandle( "rig_legBR_Foot",    	boneLegBR_Foot,    	bCreateControls=False )
		
		rigArmL_1   		= sfmUtils.CreateConstrainedHandle( "rig_armL_1",    		boneArmL_1,   		bCreateControls=False )
		rigArmL_2   		= sfmUtils.CreateConstrainedHandle( "rig_armL_2",    		boneArmL_2,   		bCreateControls=False )
		rigArmL_3   		= sfmUtils.CreateConstrainedHandle( "rig_armL_3",    		boneArmL_3,   		bCreateControls=False )
		rigArmL_4   		= sfmUtils.CreateConstrainedHandle( "rig_armL_4",    		boneArmL_4,   		bCreateControls=False )
		rigArmL_5   		= sfmUtils.CreateConstrainedHandle( "rig_armL_5",    		boneArmL_5,   		bCreateControls=False )
		rigArmL_6   		= sfmUtils.CreateConstrainedHandle( "rig_armL_6",    		boneArmL_6,   		bCreateControls=False )
		
		rigArmR_1   		= sfmUtils.CreateConstrainedHandle( "rig_ArmR_1",    		boneArmR_1,   		bCreateControls=False )
		rigArmR_2   		= sfmUtils.CreateConstrainedHandle( "rig_ArmR_2",    		boneArmR_2,   		bCreateControls=False )
		rigArmR_3   		= sfmUtils.CreateConstrainedHandle( "rig_ArmR_3",    		boneArmR_3,   		bCreateControls=False )
		rigArmR_4   		= sfmUtils.CreateConstrainedHandle( "rig_ArmR_4",    		boneArmR_4,   		bCreateControls=False )
		rigArmR_5   		= sfmUtils.CreateConstrainedHandle( "rig_ArmR_5",    		boneArmR_5,   		bCreateControls=False )
		rigArmR_6   		= sfmUtils.CreateConstrainedHandle( "rig_ArmR_6",    		boneArmR_6,   		bCreateControls=False )
		
		vKneeOffset = vs.Vector( 0, 0, 35 )
		
		rigKneeHelperFL  	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_fl", 		rigLegFL_02, 		vKneeOffset,	bCreateControls=False ) 
		rigKneeHelperFR  	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_fr", 		rigLegFR_02, 		vKneeOffset,	bCreateControls=False ) 
		rigKneeHelperBL  	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_bl", 		rigLegBL_02, 		vKneeOffset,	bCreateControls=False ) 
		rigKneeHelperBR  	= sfmUtils.CreateOffsetHandle( "rig_knee_helper_br", 		rigLegBR_02, 		vKneeOffset,	bCreateControls=False ) 
		
		allRigHandles = [ 	rigRoot, rigBase, rigLower, rigUpper,
							rigLegFL_Swivel, rigLegFL_01, rigLegFL_02, rigLegFL_Piston1, rigLegFL_Piston2, rigLegFL_Extend, rigLegFL_Foot, rigKneeHelperFL,	
							rigLegFR_Swivel, rigLegFR_01, rigLegFR_02, rigLegFR_Piston1, rigLegFR_Piston2, rigLegFR_Extend, rigLegFR_Foot, rigKneeHelperFR,	
							rigLegBL_Swivel, rigLegBL_01, rigLegBL_02, rigLegBL_Piston1, rigLegBL_Piston2, rigLegBL_Extend, rigLegBL_Foot, rigKneeHelperBL,	
							rigLegBR_Swivel, rigLegBR_01, rigLegBR_02, rigLegBR_Piston1, rigLegBR_Piston2, rigLegBR_Extend, rigLegBR_Foot, rigKneeHelperBR,
							rigArmL_1, rigArmL_2, rigArmL_3, rigArmL_4, rigArmL_5, rigArmL_6,
							rigArmR_1, rigArmR_2, rigArmR_3, rigArmR_4, rigArmR_5, rigArmR_6
							] ;	
    
    sfm.ClearSelection()
    sfmUtils.SelectDagList( allRigHandles )
    sfm.GenerateSamples()
    sfm.RemoveConstraints()    
    
    if ( isBullsquid ):
		sfmUtils.ParentMaintainWorld( rigBase,        	rigRoot )
		
		sfmUtils.ParentMaintainWorld( rigHead,        	rigBase )
		sfmUtils.ParentMaintainWorld( rigJaw,        	rigHead )
				
		sfmUtils.ParentMaintainWorld( rigHipR,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeR,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigAnkleR,        rigRoot )
		sfmUtils.ParentMaintainWorld( rigToeR,        	rigAnkleR )		
		sfmUtils.ParentMaintainWorld( rigKneeHelperR,   rigKneeR )		
		
		sfmUtils.ParentMaintainWorld( rigHipL,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeL,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigAnkleL,        rigRoot )
		sfmUtils.ParentMaintainWorld( rigToeL,        	rigAnkleL )		
		sfmUtils.ParentMaintainWorld( rigKneeHelperL,   rigKneeL )	
		
		sfmUtils.ParentMaintainWorld( rigTent12_1,   	rigJaw )	
		sfmUtils.ParentMaintainWorld( rigTent12_2,   	rigTent12_1 )	
		sfmUtils.ParentMaintainWorld( rigTent1_1,   	rigJaw )	
		sfmUtils.ParentMaintainWorld( rigTent1_2,   	rigTent1_1 )	
		sfmUtils.ParentMaintainWorld( rigTent4_1,   	rigJaw )	
		sfmUtils.ParentMaintainWorld( rigTent4_2,   	rigTent4_1 )	
		sfmUtils.ParentMaintainWorld( rigTent6_1,   	rigJaw )	
		sfmUtils.ParentMaintainWorld( rigTent6_2,   	rigTent6_1 )	
		sfmUtils.ParentMaintainWorld( rigTent8_1,   	rigJaw )	
		sfmUtils.ParentMaintainWorld( rigTent8_2,   	rigTent8_1 )	
		sfmUtils.ParentMaintainWorld( rigTent11_1,   	rigJaw )	
		sfmUtils.ParentMaintainWorld( rigTent11_2,   	rigTent11_1 )	
		
		sfmUtils.ParentMaintainWorld( rigTail1,        	rigBase )
		sfmUtils.ParentMaintainWorld( rigTail2,        	rigTail1 )
		sfmUtils.ParentMaintainWorld( rigTail3,        	rigTail2 )
		sfmUtils.ParentMaintainWorld( rigTail4,        	rigTail3 )		
		sfmUtils.ParentMaintainWorld( rigTail5,   		rigTail4 )	
		          
    if ( isHoundeye ):
		sfmUtils.ParentMaintainWorld( rigBase,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigHead,        	rigBase )
		
		sfmUtils.ParentMaintainWorld( rigMouth,        	rigBase )
		sfmUtils.ParentMaintainWorld( rigMouth1,        rigMouth )
		sfmUtils.ParentMaintainWorld( rigMouth2,        rigMouth )
		
		sfmUtils.ParentMaintainWorld( rigSpine1,        rigBase )
		sfmUtils.ParentMaintainWorld( rigSpine2,        rigSpine1 )
		
		sfmUtils.ParentMaintainWorld( rigLegR1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeHelperR,   rigLegR2 )	
		
		sfmUtils.ParentMaintainWorld( rigLegL1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeHelperL,   rigLegL2 )	
		
		sfmUtils.ParentMaintainWorld( rigLegB1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegB2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegB3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeHelperB,   rigLegB2 )	
		
    if ( isGarg ):
		sfmUtils.ParentMaintainWorld( rigBase,        	rigRoot )
		
		sfmUtils.ParentMaintainWorld( rigHead,        	rigSpine4 )
		sfmUtils.ParentMaintainWorld( rigHeadNub,       rigHead )
		sfmUtils.ParentMaintainWorld( rigJaw,       	rigHead )
		
		sfmUtils.ParentMaintainWorld( rigSpine1,        rigBase )
		sfmUtils.ParentMaintainWorld( rigSpine2,        rigSpine1 )
		sfmUtils.ParentMaintainWorld( rigSpine3,        rigSpine2 )
		sfmUtils.ParentMaintainWorld( rigSpine4,        rigSpine3 )
		
		sfmUtils.ParentMaintainWorld( rigLegR1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeHelperR,   rigLegR2 )	
		
		sfmUtils.ParentMaintainWorld( rigLegL1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeHelperL,   rigLegL2 )
		
		sfmUtils.ParentMaintainWorld( rigArmR1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmR2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmR3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigElbowHelperR, 	rigArmR2 )	
		sfmUtils.ParentMaintainWorld( rigArmRClaw1,    	rigArmR3 )
		sfmUtils.ParentMaintainWorld( rigArmRClaw2,   	rigArmR3 )
		
		sfmUtils.ParentMaintainWorld( rigArmL1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmL2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmL3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigElbowHelperL,  rigArmL2 )	
		sfmUtils.ParentMaintainWorld( rigArmLClaw1,    	rigArmL3 )
		sfmUtils.ParentMaintainWorld( rigArmLClaw2,   	rigArmL3 )
		
		sfmUtils.ParentMaintainWorld( rigClawR1,        rigBase )
		sfmUtils.ParentMaintainWorld( rigClawR2,        rigClawR1 )
		
		sfmUtils.ParentMaintainWorld( rigClawRFinger1_1,	rigClawR2 )
		sfmUtils.ParentMaintainWorld( rigClawRFinger1_2,	rigClawRFinger1_1 )
		sfmUtils.ParentMaintainWorld( rigClawRFinger1_3,	rigClawRFinger1_2 )
		sfmUtils.ParentMaintainWorld( rigClawRFinger2_1,	rigClawR2 )
		sfmUtils.ParentMaintainWorld( rigClawRFinger2_2,	rigClawRFinger2_1 )
		sfmUtils.ParentMaintainWorld( rigClawRFinger2_3,	rigClawRFinger2_2 )
		sfmUtils.ParentMaintainWorld( rigClawRFinger3_1,	rigClawR2 )
		sfmUtils.ParentMaintainWorld( rigClawRFinger3_2,	rigClawRFinger3_1 )
		sfmUtils.ParentMaintainWorld( rigClawRFinger3_3,	rigClawRFinger3_2 )
		
		sfmUtils.ParentMaintainWorld( rigClawL1,        rigBase )
		sfmUtils.ParentMaintainWorld( rigClawL2,        rigClawL1 )
		
		sfmUtils.ParentMaintainWorld( rigClawLFinger1_1,	rigClawL2 )
		sfmUtils.ParentMaintainWorld( rigClawLFinger1_2,	rigClawLFinger1_1 )
		sfmUtils.ParentMaintainWorld( rigClawLFinger1_3,	rigClawLFinger1_2 )
		sfmUtils.ParentMaintainWorld( rigClawLFinger2_1,	rigClawL2 )
		sfmUtils.ParentMaintainWorld( rigClawLFinger2_2,	rigClawLFinger2_1 )
		sfmUtils.ParentMaintainWorld( rigClawLFinger2_3,	rigClawLFinger2_2 )
		sfmUtils.ParentMaintainWorld( rigClawLFinger3_1,	rigClawL2 )
		sfmUtils.ParentMaintainWorld( rigClawLFinger3_2,	rigClawLFinger3_1 )
		sfmUtils.ParentMaintainWorld( rigClawLFinger3_3,	rigClawLFinger3_2 )
		     
    if ( isAGrunt ):
		sfmUtils.ParentMaintainWorld( rigBase,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigHead,        	rigSpine4 )
		
		sfmUtils.ParentMaintainWorld( rigJawL1,        	rigHead )
		sfmUtils.ParentMaintainWorld( rigJawL2,        	rigJawL1 )
		sfmUtils.ParentMaintainWorld( rigJawR1,        	rigHead )
		sfmUtils.ParentMaintainWorld( rigJawR2,        	rigJawR1 )
		
		sfmUtils.ParentMaintainWorld( rigSpine1,        rigBase )
		sfmUtils.ParentMaintainWorld( rigSpine2,        rigSpine1 )
		sfmUtils.ParentMaintainWorld( rigSpine3,        rigSpine2 )
		sfmUtils.ParentMaintainWorld( rigSpine4,        rigSpine3 )
		
		sfmUtils.ParentMaintainWorld( rigLegL1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeHelperL,   rigLegL2 )
		sfmUtils.ParentMaintainWorld( rigLegLToe,   	rigLegL3 )	
		
		sfmUtils.ParentMaintainWorld( rigLegR1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeHelperR,   rigLegR2 )	
		sfmUtils.ParentMaintainWorld( rigLegRToe,   	rigLegR3 )
		
		sfmUtils.ParentMaintainWorld( rigArmL1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmL2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmL3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigElbowHelperL,  rigArmL2 )	
		
		sfmUtils.ParentMaintainWorld( rigArmR1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmR2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmR3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigElbowHelperR,  rigArmR2 )	
		
		sfmUtils.ParentMaintainWorld( rigArmM1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmM2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmM3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigElbowHelperM,  rigArmM2 )	
		
    if ( isHAssassin ):
		sfmUtils.ParentMaintainWorld( rigBase,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigHead,        	rigSpine4 )
				
		sfmUtils.ParentMaintainWorld( rigSpine1,        rigBase )
		sfmUtils.ParentMaintainWorld( rigSpine2,        rigSpine1 )
		sfmUtils.ParentMaintainWorld( rigSpine3,        rigSpine2 )
		sfmUtils.ParentMaintainWorld( rigSpine4,        rigSpine3 )
				
		sfmUtils.ParentMaintainWorld( rigLegL1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeHelperL,   rigLegL2 )	
		
		sfmUtils.ParentMaintainWorld( rigLegR1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigKneeHelperR,   rigLegR2 )
				
		sfmUtils.ParentMaintainWorld( rigArmL1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmL2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmL3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigElbowHelperL,  rigArmL2 )	
		
		sfmUtils.ParentMaintainWorld( rigArmR1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmR2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigArmR3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigElbowHelperR,  rigArmR2 )	
		
    if ( isLoader ):
		sfmUtils.ParentMaintainWorld( rigBase,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLower,        	rigBase )
		sfmUtils.ParentMaintainWorld( rigUpper,        	rigLower )
				
		sfmUtils.ParentMaintainWorld( rigLegFL_Swivel, 	rigBase )
		sfmUtils.ParentMaintainWorld( rigLegFR_Swivel, 	rigBase )
		sfmUtils.ParentMaintainWorld( rigLegBL_Swivel, 	rigBase )
		sfmUtils.ParentMaintainWorld( rigLegBR_Swivel, 	rigBase )
		
		sfmUtils.ParentMaintainWorld( rigLegFL_01, 		rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegFL_02, 		rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegFL_Piston1, rigLegFL_01 )
		sfmUtils.ParentMaintainWorld( rigLegFL_Piston2, rigLegFL_02 )
		sfmUtils.ParentMaintainWorld( rigLegFL_Extend, 	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegFL_Foot, 	rigLegFL_Extend )
		sfmUtils.ParentMaintainWorld( rigKneeHelperFL, 	rigLegFL_Extend )
		
		sfmUtils.ParentMaintainWorld( rigLegFR_01, 		rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegFR_02, 		rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegFR_Piston1, rigLegFR_01 )
		sfmUtils.ParentMaintainWorld( rigLegFR_Piston2, rigLegFR_02 )
		sfmUtils.ParentMaintainWorld( rigLegFR_Extend, 	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegFR_Foot, 	rigLegFR_Extend )
		sfmUtils.ParentMaintainWorld( rigKneeHelperFR, 	rigLegFR_Extend )
		
		sfmUtils.ParentMaintainWorld( rigLegBL_01, 		rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegBL_02, 		rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegBL_Piston1, rigLegBL_01 )
		sfmUtils.ParentMaintainWorld( rigLegBL_Piston2, rigLegBL_02 )
		sfmUtils.ParentMaintainWorld( rigLegBL_Extend, 	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegBL_Foot, 	rigLegBL_Extend )
		sfmUtils.ParentMaintainWorld( rigKneeHelperBL, 	rigLegBL_Extend )
		
		sfmUtils.ParentMaintainWorld( rigLegBR_01, 		rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegBR_02, 		rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegBR_Piston1, rigLegBR_01 )
		sfmUtils.ParentMaintainWorld( rigLegBR_Piston2, rigLegBR_02 )
		sfmUtils.ParentMaintainWorld( rigLegBR_Extend, 	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegBR_Foot, 	rigLegBR_Extend )
		sfmUtils.ParentMaintainWorld( rigKneeHelperBR, 	rigLegBR_Extend )
		
		sfmUtils.ParentMaintainWorld( rigArmL_1, 		rigUpper )
		sfmUtils.ParentMaintainWorld( rigArmL_2, 		rigArmL_1 )
		sfmUtils.ParentMaintainWorld( rigArmL_3, 		rigArmL_1 )
		sfmUtils.ParentMaintainWorld( rigArmL_4, 		rigArmL_3 )
		sfmUtils.ParentMaintainWorld( rigArmL_5, 		rigArmL_3 )
		sfmUtils.ParentMaintainWorld( rigArmL_6, 		rigArmL_5 )
		
		sfmUtils.ParentMaintainWorld( rigArmR_1, 		rigUpper )
		sfmUtils.ParentMaintainWorld( rigArmR_2, 		rigArmR_1 )
		sfmUtils.ParentMaintainWorld( rigArmR_3, 		rigArmR_1 )
		sfmUtils.ParentMaintainWorld( rigArmR_4, 		rigArmR_3 )
		sfmUtils.ParentMaintainWorld( rigArmR_5, 		rigArmR_3 )
		sfmUtils.ParentMaintainWorld( rigArmR_6, 		rigArmR_5 )
		
				
    sfm.SetDefault()
        
    if ( isBullsquid ):
		sfmUtils.CreatePointOrientConstraint( rigRoot,		boneRoot )
		sfmUtils.CreatePointOrientConstraint( rigBase,		boneBase )
		
		sfmUtils.CreatePointOrientConstraint( rigHead,		boneHead )
		sfmUtils.CreatePointOrientConstraint( rigJaw,		boneJaw )
				
		sfmUtils.CreatePointOrientConstraint( rigToeR,		boneToeR )
		sfmUtils.CreatePointOrientConstraint( rigToeL,    	boneToeL )
		
		sfmUtils.CreatePointOrientConstraint( rigTent12_1,	boneTent12_1 )
		sfmUtils.CreatePointOrientConstraint( rigTent12_2,	boneTent12_2 )
		sfmUtils.CreatePointOrientConstraint( rigTent1_1,	boneTent1_1 )
		sfmUtils.CreatePointOrientConstraint( rigTent1_2,	boneTent1_2 )
		sfmUtils.CreatePointOrientConstraint( rigTent4_1,	boneTent4_1 )
		sfmUtils.CreatePointOrientConstraint( rigTent4_2,	boneTent4_2 )
		sfmUtils.CreatePointOrientConstraint( rigTent6_1,	boneTent6_1 )
		sfmUtils.CreatePointOrientConstraint( rigTent6_2,	boneTent6_2 )
		sfmUtils.CreatePointOrientConstraint( rigTent8_1,	boneTent8_1 )
		sfmUtils.CreatePointOrientConstraint( rigTent8_2,	boneTent8_2 )
		sfmUtils.CreatePointOrientConstraint( rigTent11_1,	boneTent11_1 )
		sfmUtils.CreatePointOrientConstraint( rigTent11_2,	boneTent11_2 )
		
		sfmUtils.CreatePointOrientConstraint( rigTail1,		boneTail1 )
		sfmUtils.CreatePointOrientConstraint( rigTail2,		boneTail2 )
		sfmUtils.CreatePointOrientConstraint( rigTail3,		boneTail3 )
		sfmUtils.CreatePointOrientConstraint( rigTail4,		boneTail4 )
		sfmUtils.CreatePointOrientConstraint( rigTail5,		boneTail5 )
		
		sfmUtils.BuildArmLeg( rigKneeHelperR,  rigAnkleR, boneHipR, boneAnkleR, True )
		sfmUtils.BuildArmLeg( rigKneeHelperL,  rigAnkleL, boneHipL, boneAnkleL, True )
       
    if ( isHoundeye ):
		sfmUtils.CreatePointOrientConstraint( rigRoot,		boneRoot )
		sfmUtils.CreatePointOrientConstraint( rigBase,		boneBase )
		sfmUtils.CreatePointOrientConstraint( rigHead,		boneHead )
		sfmUtils.CreatePointOrientConstraint( rigMouth,		boneMouth )
		sfmUtils.CreatePointOrientConstraint( rigMouth1,	boneMouth1 )
		sfmUtils.CreatePointOrientConstraint( rigMouth2,	boneMouth2 )
		
		sfmUtils.CreatePointOrientConstraint( rigSpine1,	boneSpine1 )
		sfmUtils.CreatePointOrientConstraint( rigSpine2,	boneSpine2 )
		
		sfmUtils.BuildArmLeg( rigKneeHelperR,  rigLegR3, boneLegR1, boneLegR3, True )
		sfmUtils.BuildArmLeg( rigKneeHelperL,  rigLegL3, boneLegL1, boneLegL3, True )
		sfmUtils.BuildArmLeg( rigKneeHelperB,  rigLegB3, boneLegB1, boneLegB3, True )
    
    if ( isGarg ):
		sfmUtils.CreatePointOrientConstraint( rigRoot,		boneRoot )
		sfmUtils.CreatePointOrientConstraint( rigBase,		boneBase )
		
		sfmUtils.CreatePointOrientConstraint( rigHead,		boneHead )
		sfmUtils.CreatePointOrientConstraint( rigHeadNub,	boneHeadNub )
		sfmUtils.CreatePointOrientConstraint( rigJaw,		boneJaw )
		
		sfmUtils.CreatePointOrientConstraint( rigSpine1,	boneSpine1 )
		sfmUtils.CreatePointOrientConstraint( rigSpine2,	boneSpine2 )
		sfmUtils.CreatePointOrientConstraint( rigSpine3,	boneSpine3 )
		sfmUtils.CreatePointOrientConstraint( rigSpine4,	boneSpine4 )
		
		sfmUtils.CreatePointOrientConstraint( rigArmRClaw1,	boneArmRClaw1 )
		sfmUtils.CreatePointOrientConstraint( rigArmRClaw2,	boneArmRClaw2 )
		sfmUtils.CreatePointOrientConstraint( rigArmLClaw1,	boneArmLClaw1 )
		sfmUtils.CreatePointOrientConstraint( rigArmLClaw2,	boneArmLClaw2 )
		
		sfmUtils.CreatePointOrientConstraint( rigClawR1,	boneClawR1 )
		sfmUtils.CreatePointOrientConstraint( rigClawR2,	boneClawR2 )
		
		sfmUtils.CreatePointOrientConstraint( rigClawRFinger1_1,	boneClawRFinger1_1 )
		sfmUtils.CreatePointOrientConstraint( rigClawRFinger1_2,	boneClawRFinger1_2 )
		sfmUtils.CreatePointOrientConstraint( rigClawRFinger1_3,	boneClawRFinger1_3 )
		sfmUtils.CreatePointOrientConstraint( rigClawRFinger2_1,	boneClawRFinger2_1 )
		sfmUtils.CreatePointOrientConstraint( rigClawRFinger2_2,	boneClawRFinger2_2 )
		sfmUtils.CreatePointOrientConstraint( rigClawRFinger2_3,	boneClawRFinger2_3 )
		sfmUtils.CreatePointOrientConstraint( rigClawRFinger3_1,	boneClawRFinger3_1 )
		sfmUtils.CreatePointOrientConstraint( rigClawRFinger3_2,	boneClawRFinger3_2 )
		sfmUtils.CreatePointOrientConstraint( rigClawRFinger3_3,	boneClawRFinger3_3 )
		
		sfmUtils.CreatePointOrientConstraint( rigClawL1,	boneClawL1 )
		sfmUtils.CreatePointOrientConstraint( rigClawL2,	boneClawL2 )
		
		sfmUtils.CreatePointOrientConstraint( rigClawLFinger1_1,	boneClawLFinger1_1 )
		sfmUtils.CreatePointOrientConstraint( rigClawLFinger1_2,	boneClawLFinger1_2 )
		sfmUtils.CreatePointOrientConstraint( rigClawLFinger1_3,	boneClawLFinger1_3 )
		sfmUtils.CreatePointOrientConstraint( rigClawLFinger2_1,	boneClawLFinger2_1 )
		sfmUtils.CreatePointOrientConstraint( rigClawLFinger2_2,	boneClawLFinger2_2 )
		sfmUtils.CreatePointOrientConstraint( rigClawLFinger2_3,	boneClawLFinger2_3 )
		sfmUtils.CreatePointOrientConstraint( rigClawLFinger3_1,	boneClawLFinger3_1 )
		sfmUtils.CreatePointOrientConstraint( rigClawLFinger3_2,	boneClawLFinger3_2 )
		sfmUtils.CreatePointOrientConstraint( rigClawLFinger3_3,	boneClawLFinger3_3 )
		
		sfmUtils.BuildArmLeg( rigKneeHelperR,  rigLegR3, boneLegR1, boneLegR3, True )
		sfmUtils.BuildArmLeg( rigKneeHelperL,  rigLegL3, boneLegL1, boneLegL3, True )
		sfmUtils.BuildArmLeg( rigElbowHelperR,  rigArmR3, boneArmR1, boneArmR3, True )
		sfmUtils.BuildArmLeg( rigElbowHelperL,  rigArmL3, boneArmL1, boneArmL3, True )
    
    if ( isAGrunt ):
		sfmUtils.CreatePointOrientConstraint( rigRoot,		boneRoot )
		sfmUtils.CreatePointOrientConstraint( rigBase,		boneBase )
		sfmUtils.CreatePointOrientConstraint( rigHead,		boneHead )
		
		sfmUtils.CreatePointOrientConstraint( rigJawL1,		boneJawL1 )
		sfmUtils.CreatePointOrientConstraint( rigJawL2,		boneJawL2 )
		sfmUtils.CreatePointOrientConstraint( rigJawR1,		boneJawR1 )
		sfmUtils.CreatePointOrientConstraint( rigJawR1,		boneJawR1 )
		
		sfmUtils.CreatePointOrientConstraint( rigSpine1,	boneSpine1 )
		sfmUtils.CreatePointOrientConstraint( rigSpine2,	boneSpine2 )
		sfmUtils.CreatePointOrientConstraint( rigSpine3,	boneSpine3 )
		sfmUtils.CreatePointOrientConstraint( rigSpine4,	boneSpine4 )
		
		sfmUtils.CreatePointOrientConstraint( rigLegLToe,	boneLegLToe )
		sfmUtils.CreatePointOrientConstraint( rigLegRToe,	boneLegRToe )
		
		sfmUtils.BuildArmLeg( rigKneeHelperR,  rigLegR3, boneLegR1, boneLegR3, True )
		sfmUtils.BuildArmLeg( rigKneeHelperL,  rigLegL3, boneLegL1, boneLegL3, True )
		sfmUtils.BuildArmLeg( rigElbowHelperL, rigArmL3, boneArmL1, boneArmL3, True )
		sfmUtils.BuildArmLeg( rigElbowHelperR, rigArmR3, boneArmR1, boneArmR3, True )
		sfmUtils.BuildArmLeg( rigElbowHelperM, rigArmM3, boneArmM1, boneArmM3, True )
    
    if ( isHAssassin ):
		sfmUtils.CreatePointOrientConstraint( rigRoot,		boneRoot )
		sfmUtils.CreatePointOrientConstraint( rigBase,		boneBase )
		sfmUtils.CreatePointOrientConstraint( rigHead,		boneHead )
		
		sfmUtils.CreatePointOrientConstraint( rigSpine1,	boneSpine1 )
		sfmUtils.CreatePointOrientConstraint( rigSpine2,	boneSpine2 )
		sfmUtils.CreatePointOrientConstraint( rigSpine3,	boneSpine3 )
		sfmUtils.CreatePointOrientConstraint( rigSpine4,	boneSpine4 )
		
		sfmUtils.BuildArmLeg( rigKneeHelperL,  rigLegL3, boneLegL1, boneLegL3, True )
		sfmUtils.BuildArmLeg( rigKneeHelperR,  rigLegR3, boneLegR1, boneLegR3, True )
		sfmUtils.BuildArmLeg( rigElbowHelperL,  rigArmL3, boneArmL1, boneArmL3, True )
		sfmUtils.BuildArmLeg( rigElbowHelperR,  rigArmR3, boneArmR1, boneArmR3, True )
    
    if ( isLoader ):
		sfmUtils.CreatePointOrientConstraint( rigRoot,		boneRoot )
		sfmUtils.CreatePointOrientConstraint( rigBase,		boneBase )
		sfmUtils.CreatePointOrientConstraint( rigLower,		boneLower )
		sfmUtils.CreatePointOrientConstraint( rigUpper,		boneUpper )
		
		CreateOrientConstraint( rigLegFL_Piston1,	boneLegFL_Piston1 )
		CreateOrientConstraint( rigLegFL_Piston2,	boneLegFL_Piston2 )
		CreateOrientConstraint( rigLegFR_Piston1,	boneLegFR_Piston1 )
		CreateOrientConstraint( rigLegFR_Piston2,	boneLegFR_Piston2 )
		CreateOrientConstraint( rigLegBL_Piston1,	boneLegBL_Piston1 )
		CreateOrientConstraint( rigLegBL_Piston2,	boneLegBL_Piston2 )
		CreateOrientConstraint( rigLegBR_Piston1,	boneLegBR_Piston1 )
		CreateOrientConstraint( rigLegBR_Piston2,	boneLegBR_Piston2 )
		
		sfmUtils.CreatePointOrientConstraint( rigLegFL_Swivel,	boneLegFL_Swivel )
		CreateOrientConstraint( rigLegFL_Foot,	boneLegFL_Foot )
		sfmUtils.CreatePointOrientConstraint( rigLegFR_Swivel,	boneLegFR_Swivel )
		CreateOrientConstraint( rigLegFR_Foot,	boneLegFR_Foot )		
		sfmUtils.CreatePointOrientConstraint( rigLegBL_Swivel,	boneLegBL_Swivel )
		CreateOrientConstraint( rigLegBL_Foot,	boneLegBL_Foot )
		sfmUtils.CreatePointOrientConstraint( rigLegBR_Swivel,	boneLegBR_Swivel )
		CreateOrientConstraint( rigLegBR_Foot,	boneLegBR_Foot )
		
		sfmUtils.BuildArmLeg( rigKneeHelperFL,  rigLegFL_Extend, boneLegFL_01, boneLegFL_Extend, False )
		sfmUtils.BuildArmLeg( rigKneeHelperFR,  rigLegFR_Extend, boneLegFR_01, boneLegFR_Extend, False )
		sfmUtils.BuildArmLeg( rigKneeHelperBL,  rigLegBL_Extend, boneLegBL_01, boneLegBL_Extend, False )
		sfmUtils.BuildArmLeg( rigKneeHelperBR,  rigLegBR_Extend, boneLegBR_01, boneLegBR_Extend, False )
				
		sfmUtils.CreatePointOrientConstraint( rigArmL_1,		boneArmL_1 )
		sfmUtils.CreatePointOrientConstraint( rigArmL_2,		boneArmL_2 )
		sfmUtils.CreatePointOrientConstraint( rigArmL_3,		boneArmL_3 )
		sfmUtils.CreatePointOrientConstraint( rigArmL_4,		boneArmL_4 )
		sfmUtils.CreatePointOrientConstraint( rigArmL_5,		boneArmL_5 )
		sfmUtils.CreatePointOrientConstraint( rigArmL_6,		boneArmL_6 )
		
		sfmUtils.CreatePointOrientConstraint( rigArmR_1,		boneArmR_1 )
		sfmUtils.CreatePointOrientConstraint( rigArmR_2,		boneArmR_2 )
		sfmUtils.CreatePointOrientConstraint( rigArmR_3,		boneArmR_3 )
		sfmUtils.CreatePointOrientConstraint( rigArmR_4,		boneArmR_4 )
		sfmUtils.CreatePointOrientConstraint( rigArmR_5,		boneArmR_5 )
		sfmUtils.CreatePointOrientConstraint( rigArmR_6,		boneArmR_6 )
    
	
	
    if ( isBullsquid ):
		rigBodyGroup = rootGroup.CreateControlGroup( "RigBody" )
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigBase)  
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigTail1, rigTail2, rigTail3, rigTail4, rigTail5 )  
		
		rigHeadGroup = rootGroup.CreateControlGroup( "RigHead" )
		rigTentGroup = rootGroup.CreateControlGroup( "RigTentacles" )		
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigHead, rigJaw )  	  		
		rigHeadGroup.AddChild( rigTentGroup )		
		sfmUtils.AddDagControlsToGroup( rigTentGroup, rigTent12_1, rigTent12_2 )  
		sfmUtils.AddDagControlsToGroup( rigTentGroup, rigTent1_1, rigTent1_2 )  
		sfmUtils.AddDagControlsToGroup( rigTentGroup, rigTent4_1, rigTent4_2 )  
		sfmUtils.AddDagControlsToGroup( rigTentGroup, rigTent6_1, rigTent6_2 )  
		sfmUtils.AddDagControlsToGroup( rigTentGroup, rigTent8_1, rigTent8_2 )  
		sfmUtils.AddDagControlsToGroup( rigTentGroup, rigTent11_1, rigTent11_2 )  
		
		rigLegsGroup = rootGroup.CreateControlGroup( "RigLegs" )
		RightLegGroup = rootGroup.CreateControlGroup( "Right Leg" )
		LeftLegGroup = rootGroup.CreateControlGroup( "Left Leg" )   				  		
		rigLegsGroup.AddChild( RightLegGroup )
		rigLegsGroup.AddChild( LeftLegGroup )
		
		sfmUtils.AddDagControlsToGroup( RightLegGroup, rigHipR, rigKneeR, rigAnkleR, rigToeR, rigKneeHelperR )
		sfmUtils.AddDagControlsToGroup( LeftLegGroup, rigHipL, rigKneeL, rigAnkleL, rigToeL, rigKneeHelperL )
		
    if ( isHoundeye ):
		rigBodyGroup = rootGroup.CreateControlGroup( "RigBody" )
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigBase)   
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigSpine1, rigSpine2 )   
		
		rigHeadGroup = rootGroup.CreateControlGroup( "RigHead" )	
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigHead )  
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigMouth, rigMouth1, rigMouth2 )  
		
		rigLegsGroup = rootGroup.CreateControlGroup( "RigLegs" )
		RightLegGroup = rootGroup.CreateControlGroup( "Right Leg" )
		LeftLegGroup = rootGroup.CreateControlGroup( "Left Leg" )   				  		
		BackLegGroup = rootGroup.CreateControlGroup( "Rear Leg" )   				  		
		rigLegsGroup.AddChild( RightLegGroup )
		rigLegsGroup.AddChild( LeftLegGroup )
		rigLegsGroup.AddChild( BackLegGroup )
		
		sfmUtils.AddDagControlsToGroup( RightLegGroup, rigLegR1, rigLegR2, rigLegR3, rigKneeHelperR )
		sfmUtils.AddDagControlsToGroup( LeftLegGroup, rigLegL1, rigLegL2, rigLegL3, rigKneeHelperL )
		sfmUtils.AddDagControlsToGroup( BackLegGroup, rigLegB1, rigLegB2, rigLegB3, rigKneeHelperB )
		
    if ( isGarg ):
		rigBodyGroup = rootGroup.CreateControlGroup( "RigBody" )
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigBase)   
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigSpine1, rigSpine2, rigSpine3, rigSpine4 )   
		
		rigHeadGroup = rootGroup.CreateControlGroup( "RigHead" )	
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigHead, rigHeadNub )  
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigJaw )  
		
		rigLegsGroup = rootGroup.CreateControlGroup( "RigLegs" )
		RightLegGroup = rootGroup.CreateControlGroup( "Right Leg" )
		LeftLegGroup = rootGroup.CreateControlGroup( "Left Leg" )   				  		
		rigLegsGroup.AddChild( RightLegGroup )
		rigLegsGroup.AddChild( LeftLegGroup )
		
		sfmUtils.AddDagControlsToGroup( RightLegGroup, rigLegR1, rigLegR2, rigLegR3, rigKneeHelperR )
		sfmUtils.AddDagControlsToGroup( LeftLegGroup, rigLegL1, rigLegL2, rigLegL3, rigKneeHelperL )
		
		rigArmsGroup = rootGroup.CreateControlGroup( "RigArms" )
		RightArmGroup = rootGroup.CreateControlGroup( "Right Arm" )
		LeftArmGroup = rootGroup.CreateControlGroup( "Left Arm" )   				  		
		rigArmsGroup.AddChild( RightArmGroup )
		rigArmsGroup.AddChild( LeftArmGroup )
		
		sfmUtils.AddDagControlsToGroup( RightArmGroup, rigArmR1, rigArmR2, rigArmR3, rigElbowHelperR, rigArmRClaw1, rigArmRClaw2 )
		sfmUtils.AddDagControlsToGroup( LeftArmGroup, rigArmL1, rigArmL2, rigArmL3, rigElbowHelperL, rigArmLClaw1, rigArmLClaw2 )
		
		rigTinyArmsGroup = rootGroup.CreateControlGroup( "RigTinyArms" )
		
		RightTinyArmGroup = rootGroup.CreateControlGroup( "Right Tiny Arm" )
		RightTinyArmFingersGroup = rootGroup.CreateControlGroup( "Right Tiny Fingers" )
		LeftTinyArmGroup = rootGroup.CreateControlGroup( "Left Tiny Arm" )   				  		
		LeftTinyArmFingersGroup = rootGroup.CreateControlGroup( "Left Tiny Fingers" )   
		
		rigTinyArmsGroup.AddChild( RightTinyArmGroup )
		rigTinyArmsGroup.AddChild( LeftTinyArmGroup )
		RightTinyArmGroup.AddChild( RightTinyArmFingersGroup )
		LeftTinyArmGroup.AddChild( LeftTinyArmFingersGroup )
		
		sfmUtils.AddDagControlsToGroup( RightTinyArmGroup, rigClawR1, rigClawR2 )
		sfmUtils.AddDagControlsToGroup( RightTinyArmFingersGroup, rigClawRFinger1_1, rigClawRFinger1_2, rigClawRFinger1_3 )
		sfmUtils.AddDagControlsToGroup( RightTinyArmFingersGroup, rigClawRFinger2_1, rigClawRFinger2_2, rigClawRFinger2_3 )
		sfmUtils.AddDagControlsToGroup( RightTinyArmFingersGroup, rigClawRFinger3_1, rigClawRFinger3_2, rigClawRFinger3_3 )
		sfmUtils.AddDagControlsToGroup( LeftTinyArmGroup, rigClawL1, rigClawL2 )
		sfmUtils.AddDagControlsToGroup( LeftTinyArmFingersGroup, rigClawLFinger1_1, rigClawLFinger1_2, rigClawLFinger1_3 )
		sfmUtils.AddDagControlsToGroup( LeftTinyArmFingersGroup, rigClawLFinger2_1, rigClawLFinger2_2, rigClawLFinger2_3 )
		sfmUtils.AddDagControlsToGroup( LeftTinyArmFingersGroup, rigClawLFinger3_1, rigClawLFinger3_2, rigClawLFinger3_3 )
		
    if ( isAGrunt ):
		rigBodyGroup = rootGroup.CreateControlGroup( "RigBody" )
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigBase)   
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigSpine1, rigSpine2, rigSpine3, rigSpine4 )   
		
		rigHeadGroup = rootGroup.CreateControlGroup( "RigHead" )	
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigHead )  
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigJawL1, rigJawL2 )  
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigJawR1, rigJawR2 )  
		
		rigLegsGroup = rootGroup.CreateControlGroup( "RigLegs" )
		RightLegGroup = rootGroup.CreateControlGroup( "Right Leg" )
		LeftLegGroup = rootGroup.CreateControlGroup( "Left Leg" )   				  		
		rigLegsGroup.AddChild( RightLegGroup )
		rigLegsGroup.AddChild( LeftLegGroup )
		
		sfmUtils.AddDagControlsToGroup( LeftLegGroup, rigLegL1, rigLegL2, rigLegL3, rigKneeHelperL, rigLegLToe )
		sfmUtils.AddDagControlsToGroup( RightLegGroup, rigLegR1, rigLegR2, rigLegR3, rigKneeHelperR, rigLegRToe )
		
		rigArmsGroup = rootGroup.CreateControlGroup( "RigArms" )
		RightArmGroup = rootGroup.CreateControlGroup( "Right Arm" )
		LeftArmGroup = rootGroup.CreateControlGroup( "Left Arm" )   				  		
		MiddleArmGroup = rootGroup.CreateControlGroup( "Middle Arm" )   				  		
		rigArmsGroup.AddChild( RightArmGroup )
		rigArmsGroup.AddChild( LeftArmGroup )
		rigArmsGroup.AddChild( MiddleArmGroup )
		
		sfmUtils.AddDagControlsToGroup( LeftArmGroup, rigArmL1, rigArmL2, rigArmL3, rigElbowHelperL )
		sfmUtils.AddDagControlsToGroup( RightArmGroup, rigArmR1, rigArmR2, rigArmR3, rigElbowHelperR )
		sfmUtils.AddDagControlsToGroup( MiddleArmGroup, rigArmM1, rigArmM2, rigArmM3, rigElbowHelperM )
		
    if ( isHAssassin ):
		rigBodyGroup = rootGroup.CreateControlGroup( "RigBody" )
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigBase )   
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigSpine1, rigSpine2, rigSpine3, rigSpine4 )   
		
		rigHeadGroup = rootGroup.CreateControlGroup( "RigHead" )	
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigHead )
		
		rigLegsGroup = rootGroup.CreateControlGroup( "RigLegs" )
		RightLegGroup = rootGroup.CreateControlGroup( "Right Leg" )
		LeftLegGroup = rootGroup.CreateControlGroup( "Left Leg" )   				  		
		rigLegsGroup.AddChild( RightLegGroup )
		rigLegsGroup.AddChild( LeftLegGroup )
		
		sfmUtils.AddDagControlsToGroup( RightLegGroup, rigLegR1, rigLegR2, rigLegR3, rigKneeHelperR )
		sfmUtils.AddDagControlsToGroup( LeftLegGroup, rigLegL1, rigLegL2, rigLegL3, rigKneeHelperL )
		
		rigArmsGroup = rootGroup.CreateControlGroup( "RigArms" )
		RightArmGroup = rootGroup.CreateControlGroup( "Right Arm" )
		LeftArmGroup = rootGroup.CreateControlGroup( "Left Arm" ) 
		rigArmsGroup.AddChild( RightArmGroup )
		rigArmsGroup.AddChild( LeftArmGroup )
		
		sfmUtils.AddDagControlsToGroup( LeftArmGroup, rigArmL1, rigArmL2, rigArmL3, rigElbowHelperL )
		sfmUtils.AddDagControlsToGroup( RightArmGroup, rigArmR1, rigArmR2, rigArmR3, rigElbowHelperR )

    if ( isLoader ):	
		rigHelpersGroup = rootGroup.CreateControlGroup( "RigHidden" )
		rigHelpersGroup.SetVisible( False )
		rigHelpersGroup.SetSnappable( False )
		sfmUtils.AddDagControlsToGroup( rigHelpersGroup, rigLegFL_01, rigLegFL_02 )
		sfmUtils.AddDagControlsToGroup( rigHelpersGroup, rigLegFR_01, rigLegFR_02 )
		sfmUtils.AddDagControlsToGroup( rigHelpersGroup, rigLegBL_01, rigLegBL_02 )
		sfmUtils.AddDagControlsToGroup( rigHelpersGroup, rigLegBR_01, rigLegBR_02 )
		
		sfmUtils.AddDagControlsToGroup( rigHelpersGroup, rigKneeHelperFL )
		sfmUtils.AddDagControlsToGroup( rigHelpersGroup, rigKneeHelperFR )
		sfmUtils.AddDagControlsToGroup( rigHelpersGroup, rigKneeHelperBL )
		sfmUtils.AddDagControlsToGroup( rigHelpersGroup, rigKneeHelperBR )
	
		rigBodyGroup = rootGroup.CreateControlGroup( "RigBody" )
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigBase )   
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigLower, rigUpper )   
				
		rigLegsGroup = rootGroup.CreateControlGroup( "RigLegs" )
		FrontLeftLegGroup = rootGroup.CreateControlGroup( "Front Left Leg" )		  		
		FrontRightLegGroup = rootGroup.CreateControlGroup( "Front Right Leg" )		
		BackLeftLegGroup = rootGroup.CreateControlGroup( "Back Left Leg" )		  		
		BackRightLegGroup = rootGroup.CreateControlGroup( "Back Right Leg" )		  		
		rigLegsGroup.AddChild( FrontLeftLegGroup )
		rigLegsGroup.AddChild( FrontRightLegGroup )
		rigLegsGroup.AddChild( BackLeftLegGroup )
		rigLegsGroup.AddChild( BackRightLegGroup )
		
		sfmUtils.AddDagControlsToGroup( FrontLeftLegGroup, 
			rigLegFL_Swivel, rigLegFL_Extend, rigLegFL_Foot, rigLegFL_Piston1, rigLegFL_Piston2 )
		sfmUtils.AddDagControlsToGroup( FrontRightLegGroup, 
			rigLegFR_Swivel, rigLegFR_Extend, rigLegFR_Foot, rigLegFR_Piston1, rigLegFR_Piston2 )
		sfmUtils.AddDagControlsToGroup( BackLeftLegGroup, 
			rigLegBL_Swivel, rigLegBL_Extend, rigLegBL_Foot, rigLegBL_Piston1, rigLegBL_Piston2 )
		sfmUtils.AddDagControlsToGroup( BackRightLegGroup, 
			rigLegBR_Swivel, rigLegBR_Extend, rigLegBR_Foot, rigLegBR_Piston1, rigLegBR_Piston2 )

		rigArmsGroup = rootGroup.CreateControlGroup( "RigArms" )
		LeftArmGroup = rootGroup.CreateControlGroup( "Left Arm" )		  		
		RightArmGroup = rootGroup.CreateControlGroup( "Right Arm" )		  		
		rigArmsGroup.AddChild( LeftArmGroup )
		rigArmsGroup.AddChild( RightArmGroup )
		
		sfmUtils.AddDagControlsToGroup( LeftArmGroup, rigArmL_1, rigArmL_2, rigArmL_3, rigArmL_4, rigArmL_5, rigArmL_6 )
		sfmUtils.AddDagControlsToGroup( RightArmGroup, rigArmR_1, rigArmR_2, rigArmR_3, rigArmR_4, rigArmR_5, rigArmR_6 )
		
		
    # Set the control group visiblity, this is done through the rig so it can track which
    # groups it hid, so they can be set back to being visible when the rig is detached.
    HideControlGroups( rig, rootGroup, "Body", "Arms", "Legs", "Unknown", "Other", "Root" )      
        
    if ( isBullsquid ):
		#Re-order the groups
		rootGroup.MoveChildToBottom( rigBodyGroup )
		rootGroup.MoveChildToBottom( rigHeadGroup )
		rootGroup.MoveChildToBottom( rigLegsGroup )   
		
    if ( isHoundeye ):
		#Re-order the groups
		rootGroup.MoveChildToBottom( rigBodyGroup )
		rootGroup.MoveChildToBottom( rigHeadGroup )
		rootGroup.MoveChildToBottom( rigLegsGroup )    
		
    if ( isGarg ):
		#Re-order the groups
		rootGroup.MoveChildToBottom( rigBodyGroup )
		rootGroup.MoveChildToBottom( rigHeadGroup )
		rootGroup.MoveChildToBottom( rigArmsGroup )    
		rootGroup.MoveChildToBottom( rigTinyArmsGroup )    
		rootGroup.MoveChildToBottom( rigLegsGroup )    
        
    if ( isAGrunt ):
		#Re-order the groups
		rootGroup.MoveChildToBottom( rigHeadGroup )
		rootGroup.MoveChildToBottom( rigBodyGroup )
		rootGroup.MoveChildToBottom( rigArmsGroup )
		rootGroup.MoveChildToBottom( rigLegsGroup )    
		
    if ( isHAssassin ):
		#Re-order the groups
		rootGroup.MoveChildToBottom( rigHeadGroup )
		rootGroup.MoveChildToBottom( rigBodyGroup )
		rootGroup.MoveChildToBottom( rigArmsGroup )
		rootGroup.MoveChildToBottom( rigLegsGroup )    
		
    if ( isLoader ):
		#Re-order the groups
		rootGroup.MoveChildToBottom( rigBodyGroup )
		rootGroup.MoveChildToBottom( rigArmsGroup )
		rootGroup.MoveChildToBottom( rigLegsGroup )    
		
    topLevelColor = vs.Color( 0, 128, 255, 255 )
    RightColor = vs.Color( 255, 100, 100, 255 )
    LeftColor = vs.Color( 100, 255, 100, 255 )
    BackColor = vs.Color( 100, 100, 255, 255 )
    
    if ( isBullsquid ):
		rigBodyGroup.SetGroupColor( topLevelColor, False )
		rigHeadGroup.SetGroupColor( topLevelColor, False )
		rigTentGroup.SetGroupColor( topLevelColor, False )
		rigLegsGroup.SetGroupColor( topLevelColor, False )
		RightLegGroup.SetGroupColor( RightColor, False )
		LeftLegGroup.SetGroupColor( LeftColor, False )
				
    if ( isHoundeye ):
		rigBodyGroup.SetGroupColor( topLevelColor, False )
		rigHeadGroup.SetGroupColor( topLevelColor, False )
		rigLegsGroup.SetGroupColor( topLevelColor, False )
		RightLegGroup.SetGroupColor( RightColor, False )
		LeftLegGroup.SetGroupColor( LeftColor, False )
		BackLegGroup.SetGroupColor( BackColor, False )
		
    if ( isGarg ):
		rigBodyGroup.SetGroupColor( topLevelColor, False )
		rigHeadGroup.SetGroupColor( topLevelColor, False )
		rigLegsGroup.SetGroupColor( topLevelColor, False )
		rigTinyArmsGroup.SetGroupColor( topLevelColor, False )
		rigArmsGroup.SetGroupColor( topLevelColor, False )
		RightLegGroup.SetGroupColor( RightColor, False )
		LeftLegGroup.SetGroupColor( LeftColor, False )
		RightTinyArmGroup.SetGroupColor( RightColor, False )
		RightTinyArmFingersGroup.SetGroupColor( RightColor, False )
		LeftTinyArmGroup.SetGroupColor( LeftColor, False )
		LeftTinyArmFingersGroup.SetGroupColor( LeftColor, False )
		RightArmGroup.SetGroupColor( RightColor, False )
		LeftArmGroup.SetGroupColor( LeftColor, False )
        
    if ( isAGrunt ):
		rigBodyGroup.SetGroupColor( topLevelColor, False )
		rigHeadGroup.SetGroupColor( topLevelColor, False )
		rigArmsGroup.SetGroupColor( topLevelColor, False )
		rigLegsGroup.SetGroupColor( topLevelColor, False )
		RightLegGroup.SetGroupColor( RightColor, False )
		LeftLegGroup.SetGroupColor( LeftColor, False )
		LeftArmGroup.SetGroupColor( LeftColor, False )
		RightArmGroup.SetGroupColor( RightColor, False )
		MiddleArmGroup.SetGroupColor( BackColor, False )
		
    if ( isHAssassin ):
		rigBodyGroup.SetGroupColor( topLevelColor, False )
		rigHeadGroup.SetGroupColor( topLevelColor, False )
		rigLegsGroup.SetGroupColor( topLevelColor, False )
		rigArmsGroup.SetGroupColor( topLevelColor, False )
		RightLegGroup.SetGroupColor( RightColor, False )
		LeftLegGroup.SetGroupColor( LeftColor, False )
		RightArmGroup.SetGroupColor( RightColor, False )
		LeftArmGroup.SetGroupColor( LeftColor, False )
		
    if ( isLoader ):
		rigBodyGroup.SetGroupColor( topLevelColor, False )
		rigLegsGroup.SetGroupColor( topLevelColor, False )
		rigArmsGroup.SetGroupColor( topLevelColor, False )
		FrontLeftLegGroup.SetGroupColor( LeftColor, False )
		FrontRightLegGroup.SetGroupColor( RightColor, False )
		BackLeftLegGroup.SetGroupColor( LeftColor, False )
		BackRightLegGroup.SetGroupColor( RightColor, False )
		LeftArmGroup.SetGroupColor( LeftColor, False )
		RightArmGroup.SetGroupColor( RightColor, False )
		
    # End the rig definition
    sfm.EndRig()
		
    if ( isHAssassin and animSet.FindControlGroup( 'Cloaking' ) == None ):
		print 'Adding assassin cloaking...'
		
		cloakingControl = animSet.FindOrAddControlGroup( animSet.GetRootControlGroup(), 'Cloaking' )
		cloakingControl.SetGroupColor( topLevelColor, False )	
		
		cloakMaster, cloakMasterValue = sfmUtils.CreateControlledValue("AssassinCloak", "value", vs.AT_FLOAT, 0.0, animSet, shot)	
		cloakingControl.AddControl(cloakMaster)	
		cloakMasterConnection = sfmUtils.CreateConnection( "cloakMasterConnection", cloakMasterValue, "value", animSet )	
	
		gameModel.AddAttribute( 'materials', vs.AT_ELEMENT_ARRAY )
		
		cloak_1 = vs.CreateElement('DmeMaterial', 'femassassin_body_leather', shot.GetFileId() )
		cloak_1.SetValue('mtlName', "models/humans/femassassin/femassassin_body_leather" )
		cloak_1.SetValue( '$cloakfactor', 0.0 )
		animSet.gameModel.materials.AddToTail(cloak_1)
		
		cloak_2 = vs.CreateElement('DmeMaterial', 'femassassin_body_d', shot.GetFileId() )
		cloak_2.SetValue('mtlName', "models/humans/femassassin/femassassin_body_d" )
		cloak_2.SetValue( '$cloakfactor', 0.0 )
		animSet.gameModel.materials.AddToTail(cloak_2)
		
		control = sfmUtils.CreateControlAndChannel('AssassinCloak1', vs.AT_FLOAT, 0.0, animSet, shot)
		control.channel.SetOutput(cloak_1, '$cloakfactor')
		cloakMasterConnection.AddOutput(cloak_1, '$cloakfactor')
		
		control = sfmUtils.CreateControlAndChannel('AssassinCloak2', vs.AT_FLOAT, 0.0, animSet, shot)
		control.channel.SetOutput(cloak_2, '$cloakfactor')	
		cloakMasterConnection.AddOutput(cloak_2, '$cloakfactor')
			
    #if ( isLoader  ):		
		#sfm.AimConstraint( "rigLegFL_Piston1", "rigLegFL_Piston2", wu=[ 0, -1, 0 ], wuSpace="refObject", refObject="rig_pelvis", mo=True )
		
	
    return
    
BuildRig();
