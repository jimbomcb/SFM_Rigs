## Blacklight Ret Rigging Scripts
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
    rig = sfm.BeginRig( "rig_blr_" + animSet.GetName() );
    if ( rig == None ):
        return
    
    # Change the operation mode to passthrough so changes chan be made temporarily
    sfm.SetOperationMode( "Pass" )
    
    # Move everything into the reference pose
    sfm.SelectAll()
    sfm.SetReferencePose()

    isMech = False
				
    if ( gameModel == None ) :
		raise Exception("Unable to find gameModel...")

    if ( gameModel.GetModelName() == "models/blr/mech/hard_suit.mdl" ) :
		isMech = True
		
    if ( gameModel.GetModelName() == "models/blr/mech/hard_suitb.mdl" ) :
		isMech = True
				
    if ( isMech == False  ) :
		raise Exception("Sorry! This model isn't supported with this rig. (" + gameModel.GetModelName() + ")")
		
    if ( isMech ):
		boneRoot      	= sfmUtils.FindFirstDag( [ "RootTransform" ], True )
		boneBase      	= sfmUtils.FindFirstDag( [ "ValveBiped.Base" ], True )
		boneBack      	= sfmUtils.FindFirstDag( [ "ValveBiped.back1" ], True )
		bonePelvis      = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Pelvis" ], True )
		
		boneSpine1      = sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_Spine" ], True )
		boneSpine2      = sfmUtils.FindFirstDag( [ "ValveBiped.back4" ], True )
		
		boneHead		= sfmUtils.FindFirstDag( [ "ValveBiped.Head" ], True )
		boneOptic1		= sfmUtils.FindFirstDag( [ "ValveBiped.optic1" ], True )
		boneOptic2		= sfmUtils.FindFirstDag( [ "ValveBiped.optic2" ], True )
		
		boneBoostL		= sfmUtils.FindFirstDag( [ "ValveBiped.l_boost" ], True )
		boneBoostR		= sfmUtils.FindFirstDag( [ "ValveBiped.r_boost" ], True )
		
		boneFlapL1		= sfmUtils.FindFirstDag( [ "ValveBiped.l_flap1" ], True )
		boneFlapL2		= sfmUtils.FindFirstDag( [ "ValveBiped.l_flap2" ], True )
		boneFlapR1		= sfmUtils.FindFirstDag( [ "ValveBiped.r_flap1" ], True )
		boneFlapR2		= sfmUtils.FindFirstDag( [ "ValveBiped.r_flap2" ], True )
				
		boneLegL1		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Thigh" ], True )
		boneLegL2		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Calf" ], True )
		boneLegL3		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Calf1" ], True )
		boneLegL4		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Foot" ], True )		
		
		boneLegR1		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Thigh" ], True )
		boneLegR2		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Calf" ], True )
		boneLegR3		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Calf1" ], True )
		boneLegR4		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Foot" ], True )
		
		boneArmL11		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Finger4" ], True )		
		boneArmL12		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Finger41" ], True )		
		boneArmL13		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Finger42" ], True )	
		boneArmL21		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_UpperArm" ], True )		
		boneArmL22		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_UpperArm1" ], True )		
		boneArmL23		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_L_Forearm" ], True )		
		
		boneArmR11		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Finger4" ], True )		
		boneArmR12		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Finger41" ], True )		
		boneArmR13		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Finger42" ], True )	
		boneArmR21		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_UpperArm" ], True )		
		boneArmR22		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_UpperArm1" ], True )		
		boneArmR23		= sfmUtils.FindFirstDag( [ "ValveBiped.Bip01_R_Forearm" ], True )		
		
    if ( isMech ):
		rigRoot    		= sfmUtils.CreateConstrainedHandle( "rig_root",     	boneRoot,    	bCreateControls=False )
		rigBase    		= sfmUtils.CreateConstrainedHandle( "rig_base",    		boneBase,    	bCreateControls=False )
		rigBack    		= sfmUtils.CreateConstrainedHandle( "rig_back",    		boneBack,    	bCreateControls=False )
		rigPelvis  		= sfmUtils.CreateConstrainedHandle( "rig_pelvis",    	bonePelvis,    	bCreateControls=False )
		
		rigSpine1    	= sfmUtils.CreateConstrainedHandle( "rig_spine1",   	boneSpine1,    	bCreateControls=False )
		rigSpine2    	= sfmUtils.CreateConstrainedHandle( "rig_spine2",   	boneSpine2,    	bCreateControls=False )
		
		rigHead    		= sfmUtils.CreateConstrainedHandle( "rig_head",   		boneHead,    	bCreateControls=False )
		rigOptic1    	= sfmUtils.CreateConstrainedHandle( "rig_optics_1",   	boneOptic1,    	bCreateControls=False )
		rigOptic2    	= sfmUtils.CreateConstrainedHandle( "rig_optics_2",   	boneOptic2,    	bCreateControls=False )
		
		rigBoostL    	= sfmUtils.CreateConstrainedHandle( "rig_boost_l",   	boneBoostL,    	bCreateControls=False )
		rigBoostR    	= sfmUtils.CreateConstrainedHandle( "rig_boost_r",   	boneBoostR,    	bCreateControls=False )
		
		rigFlapL1    	= sfmUtils.CreateConstrainedHandle( "rig_flapL_1",   	boneFlapL1,    	bCreateControls=False )
		rigFlapL2    	= sfmUtils.CreateConstrainedHandle( "rig_flapL_2",   	boneFlapL2,    	bCreateControls=False )
		rigFlapR1    	= sfmUtils.CreateConstrainedHandle( "rig_flapR_1",   	boneFlapR1,    	bCreateControls=False )
		rigFlapR2    	= sfmUtils.CreateConstrainedHandle( "rig_flapR_2",   	boneFlapR2,    	bCreateControls=False )
		
		rigLegL1    	= sfmUtils.CreateConstrainedHandle( "rig_legL_1",    	boneLegL1,    	bCreateControls=False )
		rigLegL2    	= sfmUtils.CreateConstrainedHandle( "rig_legL_2",    	boneLegL2,    	bCreateControls=False )
		rigLegL3    	= sfmUtils.CreateConstrainedHandle( "rig_legL_3",    	boneLegL3,    	bCreateControls=False )
		rigLegL4    	= sfmUtils.CreateConstrainedHandle( "rig_legL_4",    	boneLegL4,    	bCreateControls=False )
		
		rigLegR1    	= sfmUtils.CreateConstrainedHandle( "rig_LegR_1",    	boneLegR1,    	bCreateControls=False )
		rigLegR2    	= sfmUtils.CreateConstrainedHandle( "rig_LegR_2",    	boneLegR2,    	bCreateControls=False )
		rigLegR3    	= sfmUtils.CreateConstrainedHandle( "rig_LegR_3",    	boneLegR3,    	bCreateControls=False )
		rigLegR4    	= sfmUtils.CreateConstrainedHandle( "rig_LegR_4",    	boneLegR4,    	bCreateControls=False )
		
		rigArmL11    	= sfmUtils.CreateConstrainedHandle( "rig_ArmL1_1",    	boneArmL11,    	bCreateControls=False )
		rigArmL12    	= sfmUtils.CreateConstrainedHandle( "rig_ArmL1_2",    	boneArmL12,    	bCreateControls=False )
		rigArmL13    	= sfmUtils.CreateConstrainedHandle( "rig_ArmL1_3",    	boneArmL13,    	bCreateControls=False )
		rigArmL21    	= sfmUtils.CreateConstrainedHandle( "rig_ArmL2_1",    	boneArmL21,    	bCreateControls=False )
		rigArmL22    	= sfmUtils.CreateConstrainedHandle( "rig_ArmL2_2",    	boneArmL22,    	bCreateControls=False )
		rigArmL23    	= sfmUtils.CreateConstrainedHandle( "rig_ArmL2_3",    	boneArmL23,    	bCreateControls=False )
		
		rigArmR11    	= sfmUtils.CreateConstrainedHandle( "rig_ArmR1_1",    	boneArmR11,    	bCreateControls=False )
		rigArmR12    	= sfmUtils.CreateConstrainedHandle( "rig_ArmR1_2",    	boneArmR12,    	bCreateControls=False )
		rigArmR13    	= sfmUtils.CreateConstrainedHandle( "rig_ArmR1_3",    	boneArmR13,    	bCreateControls=False )
		rigArmR21    	= sfmUtils.CreateConstrainedHandle( "rig_ArmR2_1",    	boneArmR21,    	bCreateControls=False )
		rigArmR22    	= sfmUtils.CreateConstrainedHandle( "rig_ArmR2_2",    	boneArmR22,    	bCreateControls=False )
		rigArmR23    	= sfmUtils.CreateConstrainedHandle( "rig_ArmR2_3",    	boneArmR23,    	bCreateControls=False )
				
		vKneeOffset 	= ComputeVectorBetweenBones( boneBack, boneBase, 24 )
		vElbow1Offset 	= ComputeVectorBetweenBones( boneLegL1, boneLegR1, 24 )
		  
		rigKneeHelperL   = sfmUtils.CreateOffsetHandle( "rig_knee_helper_l",  	rigLegL2, 	vKneeOffset,  	bCreateControls=False )  
		rigKneeHelperR   = sfmUtils.CreateOffsetHandle( "rig_knee_helper_r",  	rigLegR2, 	vKneeOffset,  	bCreateControls=False )  
		
		rigArmL1Helper   = sfmUtils.CreateOffsetHandle( "rig_elbow_L1_helper",  	rigArmL12, 	-vElbow1Offset,  	bCreateControls=False )  
		rigArmL2Helper   = sfmUtils.CreateOffsetHandle( "rig_elbow_L2_helper",  	rigArmL22, 	-vKneeOffset,  	bCreateControls=False )  
		rigArmR1Helper   = sfmUtils.CreateOffsetHandle( "rig_elbow_R1_helper",  	rigArmR12, 	vElbow1Offset,  	bCreateControls=False )  
		rigArmR2Helper   = sfmUtils.CreateOffsetHandle( "rig_elbow_R2_helper",  	rigArmR22, 	-vKneeOffset,  	bCreateControls=False )  
		
		## All, except FOOT helpers.
		allRigHandles = [ 	rigRoot, rigBase, 
							rigBack, rigPelvis,
							rigSpine1, rigSpine2, 
							rigHead, rigOptic1, rigOptic2,
							rigBoostL, rigBoostR,
							rigFlapL1, rigFlapL2,
							rigFlapR1, rigFlapR2,
							rigLegL1, rigLegL2, rigLegL3, rigLegL4, rigKneeHelperL,
							rigLegR1, rigLegR2, rigLegR3, rigLegR4, rigKneeHelperR,
							rigArmL11, rigArmL12, rigArmL13, rigArmL1Helper,
							rigArmL21, rigArmL22, rigArmL23, rigArmL2Helper,
							rigArmR11, rigArmR12, rigArmR13, rigArmR1Helper,
							rigArmR21, rigArmR22, rigArmR23, rigArmR2Helper
							] ;
							        
    sfm.ClearSelection()
    sfmUtils.SelectDagList( allRigHandles )
    sfm.GenerateSamples()
    sfm.RemoveConstraints()    
    
    if ( isMech ):
		sfmUtils.ParentMaintainWorld( rigBase,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigBack,        	rigBase )
		sfmUtils.ParentMaintainWorld( rigPelvis,        rigBack )
		
		sfmUtils.ParentMaintainWorld( rigSpine1,        rigPelvis )
		sfmUtils.ParentMaintainWorld( rigSpine2,        rigSpine1 )
		
		sfmUtils.ParentMaintainWorld( rigHead,        	rigSpine2 )
		sfmUtils.ParentMaintainWorld( rigOptic1,        rigSpine2 )
		sfmUtils.ParentMaintainWorld( rigOptic2,        rigOptic1 )
		
		sfmUtils.ParentMaintainWorld( rigBoostL,        rigSpine2 )
		sfmUtils.ParentMaintainWorld( rigBoostR,        rigSpine2 )
		
		sfmUtils.ParentMaintainWorld( rigFlapL1,        rigSpine2 )
		sfmUtils.ParentMaintainWorld( rigFlapL2,        rigFlapL1 )
		sfmUtils.ParentMaintainWorld( rigFlapR1,        rigSpine2 )
		sfmUtils.ParentMaintainWorld( rigFlapR2,        rigFlapR1 )
		
		sfmUtils.ParentMaintainWorld( rigLegL1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegL4,        	rigRoot )		
		sfmUtils.ParentMaintainWorld( rigKneeHelperL,   rigLegL3 )	
		
		sfmUtils.ParentMaintainWorld( rigLegR1,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR2,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR3,        	rigRoot )
		sfmUtils.ParentMaintainWorld( rigLegR4,        	rigRoot )		
		sfmUtils.ParentMaintainWorld( rigKneeHelperR,   rigLegR3 )	
		
		sfmUtils.ParentMaintainWorld( rigArmL11,   rigSpine1 )	
		sfmUtils.ParentMaintainWorld( rigArmL12,   rigArmL11 )	
		sfmUtils.ParentMaintainWorld( rigArmL13,   rigRoot )	
		sfmUtils.ParentMaintainWorld( rigArmL1Helper,   rigArmL13 )	
		
		sfmUtils.ParentMaintainWorld( rigArmL21,   rigSpine2 )	
		sfmUtils.ParentMaintainWorld( rigArmL22,   rigArmL21 )	
		sfmUtils.ParentMaintainWorld( rigArmL23,   rigRoot )	
		sfmUtils.ParentMaintainWorld( rigArmL2Helper,   rigBase )	
		
		sfmUtils.ParentMaintainWorld( rigArmR11,   rigSpine1 )	
		sfmUtils.ParentMaintainWorld( rigArmR12,   rigArmR11 )	
		sfmUtils.ParentMaintainWorld( rigArmR13,   rigRoot )	
		sfmUtils.ParentMaintainWorld( rigArmR1Helper,   rigArmR13 )	
		
		sfmUtils.ParentMaintainWorld( rigArmR21,   rigSpine2 )	
		sfmUtils.ParentMaintainWorld( rigArmR22,   rigArmR21 )	
		sfmUtils.ParentMaintainWorld( rigArmR23,   rigRoot )	
		sfmUtils.ParentMaintainWorld( rigArmR2Helper,   rigBase )	
										
    sfm.SetDefault()
        
    if ( isMech ):
		sfmUtils.CreatePointOrientConstraint( rigRoot,		boneRoot )
		sfmUtils.CreatePointOrientConstraint( rigBase,		boneBase )
		sfmUtils.CreatePointOrientConstraint( rigBack,		boneBack )
		sfmUtils.CreatePointOrientConstraint( rigPelvis,	bonePelvis )
		
		sfmUtils.CreatePointOrientConstraint( rigSpine1,	boneSpine1 )
		sfmUtils.CreatePointOrientConstraint( rigSpine2,	boneSpine2 )
		
		sfmUtils.CreatePointOrientConstraint( rigHead,		boneHead )
		sfmUtils.CreatePointOrientConstraint( rigOptic1,	boneOptic1 )
		sfmUtils.CreatePointOrientConstraint( rigOptic2,	boneOptic2 )
		
		sfmUtils.CreatePointOrientConstraint( rigBoostL,	boneBoostL )
		sfmUtils.CreatePointOrientConstraint( rigBoostR,	boneBoostR )
		
		sfmUtils.CreatePointOrientConstraint( rigFlapL1,	boneFlapL1 )
		sfmUtils.CreatePointOrientConstraint( rigFlapL2,	boneFlapL2 )
		sfmUtils.CreatePointOrientConstraint( rigFlapR1,	boneFlapR1 )
		sfmUtils.CreatePointOrientConstraint( rigFlapR2,	boneFlapR2 )
		
		sfmUtils.BuildArmLeg( rigKneeHelperL,  rigLegL3, boneLegL1, boneLegL3, True )
		sfmUtils.BuildArmLeg( rigKneeHelperR,  rigLegR3, boneLegR1, boneLegR3, True )
		
		sfmUtils.BuildArmLeg( rigArmL1Helper,  rigArmL13, boneArmL11, boneArmL13, True )
		sfmUtils.BuildArmLeg( rigArmL2Helper,  rigArmL23, boneArmL21, boneArmL23, True )
		
		sfmUtils.BuildArmLeg( rigArmR1Helper,  rigArmR13, boneArmR11, boneArmR13, True )
		sfmUtils.BuildArmLeg( rigArmR2Helper,  rigArmR23, boneArmR21, boneArmR23, True )
       
	
    if ( isMech ):
		rigBodyGroup = rootGroup.CreateControlGroup( "RigBody" )
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigBase)  
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigBack, rigPelvis)  
		
		rigHeadGroup = rootGroup.CreateControlGroup( "RigHead" )
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigHead )
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigOptic1, rigOptic2 )
				
		rigLegsGroup = rootGroup.CreateControlGroup( "RigLegs" )
		RightLegGroup = rootGroup.CreateControlGroup( "Right Leg" )
		LeftLegGroup = rootGroup.CreateControlGroup( "Left Leg" )   				  		
		rigLegsGroup.AddChild( RightLegGroup )
		rigLegsGroup.AddChild( LeftLegGroup )
		
		sfmUtils.AddDagControlsToGroup( LeftLegGroup, rigLegL1, rigLegL2, rigLegL3, rigLegL4, rigKneeHelperL )
		sfmUtils.AddDagControlsToGroup( RightLegGroup, rigLegR1, rigLegR2, rigLegR3, rigLegR4, rigKneeHelperR )
		
		rigArmsGroup = rootGroup.CreateControlGroup( "RigArms" )
		RightArmGroup = rootGroup.CreateControlGroup( "Right Arm" )
		LeftArmGroup = rootGroup.CreateControlGroup( "Left Arm" )   
		RightMechArmGroup = rootGroup.CreateControlGroup( "Right Mech Arm" )
		LeftMechArmGroup = rootGroup.CreateControlGroup( "Left Mech Arm" )   			
		rigArmsGroup.AddChild( LeftArmGroup )		  		
		rigArmsGroup.AddChild( RightArmGroup )	  
		rigArmsGroup.AddChild( LeftMechArmGroup )		
		rigArmsGroup.AddChild( RightMechArmGroup )
		
		sfmUtils.AddDagControlsToGroup( LeftArmGroup, rigArmL11, rigArmL12, rigArmL13, rigArmL1Helper )
		sfmUtils.AddDagControlsToGroup( LeftMechArmGroup, rigArmL21, rigArmL22, rigArmL23, rigArmL2Helper )
		
		sfmUtils.AddDagControlsToGroup( RightArmGroup, rigArmR11, rigArmR12, rigArmR13, rigArmR1Helper )
		sfmUtils.AddDagControlsToGroup( RightMechArmGroup, rigArmR21, rigArmR22, rigArmR23, rigArmR2Helper )
		
		rigOtherGroup = rootGroup.CreateControlGroup( "RigOther" )
		sfmUtils.AddDagControlsToGroup( rigOtherGroup, rigBoostL, rigBoostR )
		sfmUtils.AddDagControlsToGroup( rigOtherGroup, rigFlapL1, rigFlapL2 )
		sfmUtils.AddDagControlsToGroup( rigOtherGroup, rigFlapR1, rigFlapR2 )
		
		
		
		
    # Set the control group visiblity, this is done through the rig so it can track which
    # groups it hid, so they can be set back to being visible when the rig is detached.
    HideControlGroups( rig, rootGroup, "Body", "Arms", "Legs", "Unknown", "Other", "Root" )      
        
    if ( isMech ):
		#Re-order the groups
		rootGroup.MoveChildToBottom( rigHeadGroup )
		rootGroup.MoveChildToBottom( rigBodyGroup )
		rootGroup.MoveChildToBottom( rigArmsGroup )
		rootGroup.MoveChildToBottom( rigLegsGroup )   
		rootGroup.MoveChildToBottom( rigOtherGroup )
		
		
    topLevelColor = vs.Color( 0, 128, 255, 255 )
    RightColor = vs.Color( 255, 100, 100, 255 )
    LeftColor = vs.Color( 100, 255, 100, 255 )
    BackColor = vs.Color( 100, 100, 255, 255 )
    
    if ( isMech ):
		rigBodyGroup.SetGroupColor( topLevelColor, False )
		rigHeadGroup.SetGroupColor( topLevelColor, False )
		rigArmsGroup.SetGroupColor( topLevelColor, False )
		rigLegsGroup.SetGroupColor( topLevelColor, False )
		rigOtherGroup.SetGroupColor( topLevelColor, False )
		RightLegGroup.SetGroupColor( RightColor, False )
		LeftLegGroup.SetGroupColor( LeftColor, False )
		RightArmGroup.SetGroupColor( RightColor, False )
		LeftArmGroup.SetGroupColor( LeftColor, False )
		RightMechArmGroup.SetGroupColor( RightColor, False )
		LeftMechArmGroup.SetGroupColor( LeftColor, False )
				
    # End the rig definition
    sfm.EndRig()
			
    return
    
BuildRig();
