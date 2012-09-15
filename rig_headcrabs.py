# Headcrab rig - jimbomcb
import vs

# Helpers
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
	
# Main rig
			
def BuildRig():
    
    topLevelColor = vs.Color( 0, 128, 255, 255 )
    FrontLegColor = vs.Color( 255, 180, 180, 255 ) 
	
    shot = sfm.GetCurrentShot()
    animSet = sfm.GetCurrentAnimationSet()
    gameModel = animSet.gameModel
    rootGroup = animSet.GetRootControlGroup()
    
    rig = sfm.BeginRig( "rig_headcrab_" + animSet.GetName() );
    if ( rig == None ):
        return
    
    sfm.SetOperationMode( "Pass" )
    
    sfm.SelectAll()
    sfm.SetReferencePose()
	
    print "Starting..."
	
    hasHoleControl = False
    dagHoleControlL = [ "HoleControlL", "Whole_L" ]
    dagHoleControlR = [ "HoleControlR", "Whole_R" ]
    
    if ( sfmUtils.FindFirstDag( dagHoleControlL, False ) != None and sfmUtils.FindFirstDag( dagHoleControlR, False ) != None ):
        hasHoleControl = True
    	print "+ Hole Controllers"
    else:
        print "- Hole Controllers"
    
    hasDeformer1 = False
    hasDeformer2 = False
    hasDeformer3 = False
    hasDeformer4 = False
    dagDeformer1 = [ "Deform_Front", "wiggle_front" ]
    dagDeformer2 = [ "Deform_R", "wiggle_R" ]
    dagDeformer3 = [ "Deform_Rear", "wiggle_back" ]
    dagDeformer4 = [ "Deform_L", "wiggle_L" ]
    
    if ( sfmUtils.FindFirstDag( dagDeformer1, False ) != None ):
        hasDeformer1 = True
    if ( sfmUtils.FindFirstDag( dagDeformer2, False ) != None ):
        hasDeformer2 = True
    if ( sfmUtils.FindFirstDag( dagDeformer3, False ) != None ):
        hasDeformer3 = True
    if ( sfmUtils.FindFirstDag( dagDeformer4, False ) != None ):
        hasDeformer4 = True
		
    hasHeadControl = False
    dagHeadControl = [ "HeadControl", "Teeth" ]
    if ( sfmUtils.FindFirstDag( dagHeadControl, False ) != None ):
        hasHeadControl = True
		
    isBlackHeadcrab = False
    isNormalHeadcrab = False
	
    if ( sfmUtils.FindFirstDag( ["teeth_bone0_l"], False ) != None ):
        isBlackHeadcrab = True
    if ( sfmUtils.FindFirstDag( ["FangL_Bone1"], False ) != None ):
        isNormalHeadcrab = True
		
    boneRoot      = sfmUtils.FindFirstDag( [ "RootTransform" ], True )
    boneBody      = sfmUtils.FindFirstDag( [ "Body" ], True )
    boneChest      = sfmUtils.FindFirstDag( [ "chest" ], True )
    boneHips      = sfmUtils.FindFirstDag( [ "hips" ], True )
	
    boneArmR1      = sfmUtils.FindFirstDag( [ "UpperArmR_Bone" ], True )
    boneArmR2      = sfmUtils.FindFirstDag( [ "ForeArmR_Bone" ], True )
    boneArmR3      = sfmUtils.FindFirstDag( [ "HandR" ], True )
	
    boneArmL1      = sfmUtils.FindFirstDag( [ "UpperArmL_Bone" ], True )
    boneArmL2      = sfmUtils.FindFirstDag( [ "ForeArmL_Bone" ], True )
    boneArmL3      = sfmUtils.FindFirstDag( [ "HandL" ], True )
	
    boneLegL1      = sfmUtils.FindFirstDag( [ "ThighL_Bone" ], True )
    boneLegL2      = sfmUtils.FindFirstDag( [ "CalfL_Bone" ], True )
    boneLegL3      = sfmUtils.FindFirstDag( [ "FootL" ], True )
	
    boneLegR1      = sfmUtils.FindFirstDag( [ "ThighR_Bone" ], True )
    boneLegR2      = sfmUtils.FindFirstDag( [ "CalfR_Bone" ], True )
    boneLegR3      = sfmUtils.FindFirstDag( [ "FootR" ], True )
		
    if ( hasHoleControl == True ):	
		boneHoleControlL      = sfmUtils.FindFirstDag( dagHoleControlL, True )
		boneHoleControlR      = sfmUtils.FindFirstDag( dagHoleControlR, True )
		
    if ( hasDeformer1 == True ):	
		boneDeformer1      	= sfmUtils.FindFirstDag( dagDeformer1, True )
    if ( hasDeformer2 == True ):	
		boneDeformer2      	= sfmUtils.FindFirstDag( dagDeformer2, True )
    if ( hasDeformer3 == True ):	
		boneDeformer3      	= sfmUtils.FindFirstDag( dagDeformer3, True )
    if ( hasDeformer4 == True ):	
		boneDeformer4      	= sfmUtils.FindFirstDag( dagDeformer4, True )
	
    if ( hasHeadControl == True ):	
		boneHeadControl     = sfmUtils.FindFirstDag( dagHeadControl, True )
		
    if ( isBlackHeadcrab == True ):
		boneFangL1 = sfmUtils.FindFirstDag( [ "teeth_bone0_L" ], True )
		boneFangL2 = sfmUtils.FindFirstDag( [ "teeth_bone1_L" ], True )
		boneFangL3 = sfmUtils.FindFirstDag( [ "teeth_bone2_L" ], True )
		boneFangR1 = sfmUtils.FindFirstDag( [ "teeth_bone0_R" ], True )
		boneFangR2 = sfmUtils.FindFirstDag( [ "teeth_bone2_R" ], True )
		
    if ( isNormalHeadcrab == True ):
		boneFangL1 = sfmUtils.FindFirstDag( [ "FangL_Bone1" ], True )
		boneFangL2 = sfmUtils.FindFirstDag( [ "FangL_Bone2" ], True )
		boneFangR1 = sfmUtils.FindFirstDag( [ "FangR_Bone1" ], True )
		
    vOffsetRearKnee = vs.Vector( 0, 0, 7 )
	
    if ( isNormalHeadcrab == True ):
		vOffsetRearKnee = ComputeVectorBetweenBones( boneHips, boneChest, 4 )
	
    rigRoot     = sfmUtils.CreateConstrainedHandle( "rig_root",     boneRoot,    bCreateControls=False )
    rigBody     = sfmUtils.CreateConstrainedHandle( "rig_body",     boneBody,    bCreateControls=False )
    rigChest    = sfmUtils.CreateConstrainedHandle( "rig_chest",     boneChest,    bCreateControls=False )
    rigHips     = sfmUtils.CreateConstrainedHandle( "rig_hips",     boneHips,    bCreateControls=False )
    
    rigArmR1    = sfmUtils.CreateConstrainedHandle( "rig_arm_r1",      boneArmR1,    bCreateControls=False )
    rigArmR2    = sfmUtils.CreateConstrainedHandle( "rig_arm_r2",      boneArmR2,    bCreateControls=False )
    rigArmR3    = sfmUtils.CreateConstrainedHandle( "rig_arm_r3",      boneArmR3,    bCreateControls=False )
    rigArmRElbow = sfmUtils.CreateOffsetHandle( "rig_arm_relbow",  	   rigArmR2,  vs.Vector( 0, 0, 7 ),  bCreateControls=False )
	
    rigArmL1    = sfmUtils.CreateConstrainedHandle( "rig_arm_l1",      boneArmL1,    bCreateControls=False )
    rigArmL2    = sfmUtils.CreateConstrainedHandle( "rig_arm_l2",      boneArmL2,    bCreateControls=False )
    rigArmL3    = sfmUtils.CreateConstrainedHandle( "rig_arm_l3",      boneArmL3,    bCreateControls=False )
    rigArmLElbow = sfmUtils.CreateOffsetHandle( "rig_arm_lelbow",  	   rigArmL2,  vs.Vector( 0, 0, 7 ),  bCreateControls=False )
	
    rigLegR1    = sfmUtils.CreateConstrainedHandle( "rig_leg_r1",      boneLegR1,    bCreateControls=False )
    rigLegR2    = sfmUtils.CreateConstrainedHandle( "rig_leg_r2",      boneLegR2,    bCreateControls=False )
    rigLegR3    = sfmUtils.CreateConstrainedHandle( "rig_leg_r3",      boneLegR3,    bCreateControls=False )
    rigLegRElbow = sfmUtils.CreateOffsetHandle( "rig_leg_rknee",  	   rigLegR2,  	vOffsetRearKnee,  bCreateControls=False )
	
    rigLegL1    = sfmUtils.CreateConstrainedHandle( "rig_leg_l1",      boneLegL1,    bCreateControls=False )
    rigLegL2    = sfmUtils.CreateConstrainedHandle( "rig_leg_l2",      boneLegL2,    bCreateControls=False )
    rigLegL3    = sfmUtils.CreateConstrainedHandle( "rig_leg_l3",      boneLegL3,    bCreateControls=False )
    rigLegLElbow = sfmUtils.CreateOffsetHandle( "rig_leg_lknee",  	   rigLegL2,  	vOffsetRearKnee,  bCreateControls=False )
    
    if ( hasHoleControl == True ):	
		rigHoleControlL      = sfmUtils.CreateConstrainedHandle( "rig_holecontrol_l",      boneHoleControlL,    bCreateControls=False )
		rigHoleControlR      = sfmUtils.CreateConstrainedHandle( "rig_holecontrol_r",      boneHoleControlR,    bCreateControls=False )
		
    if ( hasDeformer1 == True ):	
		rigDeformer1      = sfmUtils.CreateConstrainedHandle( "rig_Deformer_Front",      boneDeformer1,    bCreateControls=False )
    if ( hasDeformer2 == True ):	
		rigDeformer2      = sfmUtils.CreateConstrainedHandle( "rig_Deformer_Right",      boneDeformer2,    bCreateControls=False )
    if ( hasDeformer3 == True ):	
		rigDeformer3      = sfmUtils.CreateConstrainedHandle( "rig_Deformer_Rear",      boneDeformer3,    bCreateControls=False )
    if ( hasDeformer4 == True ):	
		rigDeformer4      = sfmUtils.CreateConstrainedHandle( "rig_Deformer_Left",      boneDeformer4,    bCreateControls=False )
		
    if ( hasHeadControl == True ):	
		rigHeadControl     = sfmUtils.CreateConstrainedHandle( "rig_Head",      boneHeadControl,    bCreateControls=False )
		
    if ( isBlackHeadcrab == True ):
		rigFangL1 = sfmUtils.CreateConstrainedHandle( "rig_Fang_L1",      boneFangL1,    bCreateControls=False )
		rigFangL2 = sfmUtils.CreateConstrainedHandle( "rig_Fang_L2",      boneFangL2,    bCreateControls=False )
		rigFangL3 = sfmUtils.CreateConstrainedHandle( "rig_Fang_L3",      boneFangL3,    bCreateControls=False )
		rigFangR1 = sfmUtils.CreateConstrainedHandle( "rig_Fang_R1",      boneFangR1,    bCreateControls=False )
		rigFangR2 = sfmUtils.CreateConstrainedHandle( "rig_Fang_R2",      boneFangR2,    bCreateControls=False )
		
    if ( isNormalHeadcrab == True ):
		rigFangL1 = sfmUtils.CreateConstrainedHandle( "rig_Fang_L1",      boneFangL1,    bCreateControls=False )
		rigFangL2 = sfmUtils.CreateConstrainedHandle( "rig_Fang_L2",      boneFangL2,    bCreateControls=False )
		rigFangR1 = sfmUtils.CreateConstrainedHandle( "rig_Fang_R1",      boneFangR1,    bCreateControls=False )
		
    allRigHandles = [ rigRoot, rigBody, rigChest, rigHips,
    rigArmR1,rigArmR2,rigArmR3,rigArmRElbow,
    rigArmL1,rigArmL2,rigArmL3,rigArmLElbow,
    rigLegR1,rigLegR2,rigLegR3,rigLegRElbow,
    rigLegL1,rigLegL2,rigLegL3,rigLegLElbow
    ]
	
    if ( hasHoleControl == True ):	
		allRigHandles = allRigHandles + [rigHoleControlL]
		allRigHandles = allRigHandles + [rigHoleControlR]
		
    if ( hasDeformer1 == True ):	
		allRigHandles = allRigHandles + [rigDeformer1]
    if ( hasDeformer2 == True ):	
		allRigHandles = allRigHandles + [rigDeformer2]
    if ( hasDeformer3 == True ):	
		allRigHandles = allRigHandles + [rigDeformer3]
    if ( hasDeformer4 == True ):	
		allRigHandles = allRigHandles + [rigDeformer4]
		
    if ( hasHeadControl == True ):	
		allRigHandles = allRigHandles + [rigHeadControl]
		
    if ( isBlackHeadcrab == True ):
		allRigHandles = allRigHandles + [rigFangL1,rigFangL2,rigFangL3,rigFangR1,rigFangR2]
		
    if ( isNormalHeadcrab == True ):
		allRigHandles = allRigHandles + [rigFangL1,rigFangL2,rigFangR1]
	
    sfm.ClearSelection()
    sfmUtils.SelectDagList( allRigHandles )
    sfm.GenerateSamples()
    sfm.RemoveConstraints()    
    
	
    sfmUtils.ParentMaintainWorld( rigBody,        rigRoot )   
    sfmUtils.ParentMaintainWorld( rigChest,        rigBody )   
    sfmUtils.ParentMaintainWorld( rigHips,        rigBody )   
	
    sfmUtils.ParentMaintainWorld( rigArmR1,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigArmR2,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigArmR3,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigArmRElbow,     rigArmR3 )
	
    sfmUtils.ParentMaintainWorld( rigArmL1,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigArmL2,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigArmL3,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigArmLElbow,     rigArmL3 )
	
    sfmUtils.ParentMaintainWorld( rigLegR1,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLegR2,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLegR3,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLegRElbow,     rigLegR3 )
	
    sfmUtils.ParentMaintainWorld( rigLegL1,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLegL2,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLegL3,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLegLElbow,     rigLegL3 )
	
    if ( hasHoleControl == True ):	
		if ( isNormalHeadcrab == True ):
			sfmUtils.ParentMaintainWorld( rigHoleControlL,        rigChest )   
			sfmUtils.ParentMaintainWorld( rigHoleControlR,        rigChest )   
		if ( isBlackHeadcrab == True ):
			sfmUtils.ParentMaintainWorld( rigHoleControlL,        rigBody )   
			sfmUtils.ParentMaintainWorld( rigHoleControlR,        rigBody )   
	
    if ( hasDeformer1 == True ):	
		sfmUtils.ParentMaintainWorld( rigDeformer1,        rigBody )   
    if ( hasDeformer2 == True ):	
		sfmUtils.ParentMaintainWorld( rigDeformer2,        rigBody )   
    if ( hasDeformer3 == True ):	
		sfmUtils.ParentMaintainWorld( rigDeformer3,        rigBody )   
    if ( hasDeformer4 == True ):	
		sfmUtils.ParentMaintainWorld( rigDeformer4,        rigBody )  
		
    if ( hasHeadControl == True ):	
		sfmUtils.ParentMaintainWorld( rigHeadControl,        rigChest )   
		
    fangParent = rigChest
		
    if ( isBlackHeadcrab == True ):
		if ( hasHeadControl == True ):	
			fangParent = rigHeadControl			
		sfmUtils.ParentMaintainWorld( rigFangL1,        fangParent )   
		sfmUtils.ParentMaintainWorld( rigFangL2,        rigFangL1 )   
		sfmUtils.ParentMaintainWorld( rigFangL3,        rigFangL2 )   
		sfmUtils.ParentMaintainWorld( rigFangR1,        fangParent )   
		sfmUtils.ParentMaintainWorld( rigFangR2,        rigFangR1 )   
		
    if ( isNormalHeadcrab == True ):
		if ( hasHeadControl == True ):	
			fangParent = rigHeadControl		
		sfmUtils.ParentMaintainWorld( rigFangL1,        fangParent )   
		sfmUtils.ParentMaintainWorld( rigFangL2,        rigFangL1 )   
		sfmUtils.ParentMaintainWorld( rigFangR1,        fangParent )   
		
    	
    sfmUtils.CreatePointOrientConstraint( rigRoot,      boneRoot  )
    sfmUtils.CreatePointOrientConstraint( rigBody,      boneBody  )
    sfmUtils.CreatePointOrientConstraint( rigChest,      boneChest  )
    sfmUtils.CreatePointOrientConstraint( rigHips,      boneHips  )
	
    if ( hasHoleControl == True ):	
		sfmUtils.CreatePointOrientConstraint( rigHoleControlL,        boneHoleControlL )   
		sfmUtils.CreatePointOrientConstraint( rigHoleControlR,        boneHoleControlR )   
    
    if ( hasDeformer1 == True ):	
		sfmUtils.CreatePointOrientConstraint( rigDeformer1,        boneDeformer1 )    
    if ( hasDeformer2 == True ):	
		sfmUtils.CreatePointOrientConstraint( rigDeformer2,        boneDeformer2 )     
    if ( hasDeformer3 == True ):	
		sfmUtils.CreatePointOrientConstraint( rigDeformer3,        boneDeformer3 )    
    if ( hasDeformer4 == True ):	
		sfmUtils.CreatePointOrientConstraint( rigDeformer4,        boneDeformer4 )  
		
    if ( hasHeadControl == True ):	
		sfmUtils.CreatePointOrientConstraint( rigHeadControl,        boneHeadControl )   
		
    if ( isBlackHeadcrab == True ):
		sfmUtils.CreatePointOrientConstraint( rigFangL1,        boneFangL1 )   
		sfmUtils.CreatePointOrientConstraint( rigFangL2,        boneFangL2 )   
		sfmUtils.CreatePointOrientConstraint( rigFangL3,        boneFangL3 )   
		sfmUtils.CreatePointOrientConstraint( rigFangR1,        boneFangR1 )   
		sfmUtils.CreatePointOrientConstraint( rigFangR2,        boneFangR2 )   
		
    if ( isNormalHeadcrab == True ):
		sfmUtils.CreatePointOrientConstraint( rigFangL1,        boneFangL1 )   
		sfmUtils.CreatePointOrientConstraint( rigFangL2,        boneFangL2 )   
		sfmUtils.CreatePointOrientConstraint( rigFangR1,        boneFangR1 )  
		
	
    sfmUtils.BuildArmLeg( rigArmRElbow,  rigArmR3, boneArmR1,  boneArmR3, True )
    sfmUtils.BuildArmLeg( rigArmLElbow,  rigArmL3, boneArmL1,  boneArmL3, True )
    sfmUtils.BuildArmLeg( rigLegRElbow,  rigLegR3, boneLegR1,  boneLegR3, True )
    sfmUtils.BuildArmLeg( rigLegLElbow,  rigLegL3, boneLegL1,  boneLegL3, True )
    		
			
    rigBodyGroup = rootGroup.CreateControlGroup( "Rig Body" )    
    sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigBody, rigChest, rigHips )  
	
    if ( hasHoleControl == True ):	
		sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigHoleControlL, rigHoleControlR )  
	
    rigLegsGroup = rootGroup.CreateControlGroup( "Rig Legs" )
	
    LegFLGroup = rootGroup.CreateControlGroup( "Front Left" )
    LegRLGroup = rootGroup.CreateControlGroup( "Rear Left" )
    LegFRGroup = rootGroup.CreateControlGroup( "Front Right" )
    LegRRGroup = rootGroup.CreateControlGroup( "Rear Right" )
	
    sfmUtils.AddDagControlsToGroup( LegFLGroup, rigArmL1, rigArmL2, rigArmL3, rigArmLElbow )
    sfmUtils.AddDagControlsToGroup( LegFRGroup, rigArmR1, rigArmR2, rigArmR3, rigArmRElbow )
    sfmUtils.AddDagControlsToGroup( LegRLGroup, rigLegL1, rigLegL2, rigLegL3, rigLegLElbow )
    sfmUtils.AddDagControlsToGroup( LegRRGroup, rigLegR1, rigLegR2, rigLegR3, rigLegRElbow )
		
    rigLegsGroup.AddChild( LegFLGroup )
    rigLegsGroup.AddChild( LegFRGroup )
    rigLegsGroup.AddChild( LegRLGroup )
    rigLegsGroup.AddChild( LegRRGroup )
		
    if ( hasDeformer1 == True or hasDeformer2 == True or hasDeformer3 == True or hasDeformer4 == True ):
		rigDeformerGroup = rootGroup.CreateControlGroup( "Rig Deformers" )
		
		if ( hasDeformer1 == True ):	
			sfmUtils.AddDagControlsToGroup( rigDeformerGroup, rigDeformer1 )
		if ( hasDeformer2 == True ):	
			sfmUtils.AddDagControlsToGroup( rigDeformerGroup, rigDeformer2 )
		if ( hasDeformer3 == True ):	
			sfmUtils.AddDagControlsToGroup( rigDeformerGroup, rigDeformer3 )   
		if ( hasDeformer4 == True ):	
			sfmUtils.AddDagControlsToGroup( rigDeformerGroup, rigDeformer4 )
	    
    rigHeadGroup = rootGroup.CreateControlGroup( "Rig Head" )
	
    if ( hasHeadControl == True ):	
		sfmUtils.AddDagControlsToGroup( rigHeadGroup, rigHeadControl )
		
    if ( isBlackHeadcrab == True ):
		FangGroupL = rootGroup.CreateControlGroup( "Fangs Left" )
		FangGroupR = rootGroup.CreateControlGroup( "Fangs Right" )
		sfmUtils.AddDagControlsToGroup( FangGroupL, rigFangL1, rigFangL2, rigFangL3 )
		sfmUtils.AddDagControlsToGroup( FangGroupR, rigFangR1, rigFangR2 )  
		rigHeadGroup.AddChild( FangGroupL )
		rigHeadGroup.AddChild( FangGroupR )
		FangGroupL.SetGroupColor( FrontLegColor, False )
		FangGroupR.SetGroupColor( FrontLegColor, False )
		
    if ( isNormalHeadcrab == True ):
		FangGroupL = rootGroup.CreateControlGroup( "Fangs Left" )
		FangGroupR = rootGroup.CreateControlGroup( "Fangs Right" )
		sfmUtils.AddDagControlsToGroup( FangGroupL, rigFangL1, rigFangL2 )
		sfmUtils.AddDagControlsToGroup( FangGroupR, rigFangR1 ) 
		rigHeadGroup.AddChild( FangGroupL )
		rigHeadGroup.AddChild( FangGroupR )
		FangGroupL.SetGroupColor( FrontLegColor, False )
		FangGroupR.SetGroupColor( FrontLegColor, False )
	
		
    HideControlGroups( rig, rootGroup, "Body", "Arms", "Legs", "Unknown", "Other", "Root" )      
        
		
    rootGroup.MoveChildToBottom( rigBodyGroup )
    if ( hasDeformer1 == True or hasDeformer2 == True or hasDeformer3 == True or hasDeformer4 == True ):
		rootGroup.MoveChildToBottom( rigDeformerGroup )  
    rootGroup.MoveChildToBottom( rigHeadGroup )
    rootGroup.MoveChildToBottom( rigLegsGroup )  
    
    
    rigBodyGroup.SetGroupColor( topLevelColor, False )
    rigLegsGroup.SetGroupColor( topLevelColor, False )
    rigHeadGroup.SetGroupColor( topLevelColor, False )
	
    if ( hasDeformer1 == True or hasDeformer2 == True or hasDeformer3 == True or hasDeformer4 == True ):
		rigDeformerGroup.SetGroupColor( topLevelColor, False )
	   
    LegFLGroup.SetGroupColor( FrontLegColor, False )
    LegFRGroup.SetGroupColor( FrontLegColor, False )
    LegRLGroup.SetGroupColor( FrontLegColor, False )
    LegRRGroup.SetGroupColor( FrontLegColor, False )
	
    return
    
BuildRig();

