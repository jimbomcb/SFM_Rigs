import vs

#==================================================================================================
def AddValidObjectToList( objectList, obj ):
    if ( obj != None ): objectList.append( obj )
    

#==================================================================================================
def HideControlGroups( rig, rootGroup, *groupNames ):
    for name in groupNames:    
        group = rootGroup.FindChildByName( name, False )
        if ( group != None ):
            rig.HideControlGroup( group )

def BuildTurretLeg( rigPVTarget, rigEndTarget, bipStart, bipMiddle, bipEnd, constrainEnd, group=None ) :
    ''' Method for constraining an arm or leg to a set of handles '''
    pvTargetDag = sfmUtils.GetDagFromNameOrObject( rigPVTarget )
    endTargetDag = sfmUtils.GetDagFromNameOrObject( rigEndTarget )
	
    startBoneDag = sfmUtils.GetDagFromNameOrObject( bipStart )
    middleBoneDag = sfmUtils.GetDagFromNameOrObject( bipMiddle )
    endBoneDag = sfmUtils.GetDagFromNameOrObject( bipEnd )
    
    sfm.PushSelection()    
    
    # Create a 2 bone ik constraint that constrains the two bones connecting the start and end
    sfm.SelectDag( endTargetDag )
    sfm.SelectDag( startBoneDag )
    sfm.SelectDag( middleBoneDag )
    sfm.SelectDag( endBoneDag )
    constraintTarget = sfm.IKConstraint( pvTarget=pvTargetDag, mo=True )

    # Add the control to the group if specified
    if ( ( group != None ) and ( constraintTarget != None ) ):
        control = constraintTarget.FindWeightControl()
        if ( control != None ):
            group.AddControl( control )
          
    

    # Orient constrain the foot to the rig handle so that it's rotation will not be effected by the ik
    if ( constrainEnd ) :
        sfm.ClearSelection()
        sfm.SelectDag( endTargetDag )
        sfm.SelectDag( endBoneDag )
        constraintTarget = sfm.OrientConstraint( mo=True )
        
        if ( ( group != None ) and ( constraintTarget != None ) ):
            control = constraintTarget.FindWeightControl()
            if ( control != None ):
                group.AddControl( control )
                
                                     
    sfm.PopSelection()
        
    return
    
#==================================================================================================
# Create the reverse foot control and operators for the foot on the specified side
#==================================================================================================
def CreateReverseFoot( controlName, sideName, gameModel, animSet, shot, helperControlGroup, footControlGroup ) :
    
    # Cannot create foot controls without heel position, so check for that first
    heelAttachName = "pvt_heel_" + sideName
    if ( gameModel.FindAttachment( heelAttachName ) == 0 ):
        print "Could not create foot control " + controlName + ", model is missing heel attachment point: " + heelAttachName;
        return None
    
    footRollDefault = 0.5
    rotationAxis = vs.Vector( 1, 0, 0 )
        
    # Construct the name of the dag nodes of the foot and toe for the specified side
    footName = "rig_foot_" + sideName
    toeName = "rig_toe_" + sideName    
    
    # Get the world space position and orientation of the foot and toe
    footPos = sfm.GetPosition( footName )
    footRot = sfm.GetRotation( footName )
    toePos = sfm.GetPosition( toeName )
    
    # Setup the reverse foot hierarchy such that the foot is the parent of all the foot transforms, the 
    # reverse heel is the parent of the heel, so it can be used for rotations around the ball of the 
    # foot that will move the heel, the heel is the parent of the foot IK handle so that it can perform
    # rotations around the heel and move the foot IK handle, resulting in moving all the foot bones.
    # root
    #   + rig_foot_R
    #       + rig_knee_R
    #       + rig_reverseHeel_R
    #           + rig_heel_R
    #               + rig_footIK_R
    
  
    # Construct the reverse heel joint this will be used to rotate the heel around the toe, and as
    # such is positioned at the toe, but using the rotation of the foot which will be its parent, 
    # so that it has no local rotation once parented to the foot.
    reverseHeelName = "rig_reverseHeel_" + sideName
    reverseHeelDag = sfm.CreateRigHandle( reverseHeelName, pos=toePos, rot=footRot, rotControl=False )
    sfmUtils.Parent( reverseHeelName, footName, vs.REPARENT_LOGS_OVERWRITE )
    
    
    
    # Construct the heel joint, this will be used to rotate the foot around the back of the heel so it 
    # is created at the heel location (offset from the foot) and also given the rotation of its parent.
    heelName = "rig_heel_" + sideName
    vecHeelPos = gameModel.ComputeAttachmentPosition( heelAttachName )
    heelPos = [ vecHeelPos.x, vecHeelPos.y, vecHeelPos.z ]     
    heelRot = sfm.GetRotation( reverseHeelName )
    heelDag = sfm.CreateRigHandle( heelName, pos=heelPos, rot=heelRot, posControl=True, rotControl=False )
    sfmUtils.Parent( heelName, reverseHeelName, vs.REPARENT_LOGS_OVERWRITE )
    
    # Create the ik handle which will be used as the target for the ik chain for the leg
    ikHandleName = "rig_footIK_" + sideName   
    ikHandleDag = sfmUtils.CreateHandleAt( ikHandleName, footName )
    sfmUtils.Parent( ikHandleName, heelName, vs.REPARENT_LOGS_OVERWRITE )
                    
    # Create an orient constraint which causes the toe's orientation to match the foot's orientation
    footRollControlName = controlName + "_" + sideName
    toeOrientTarget = sfm.OrientConstraint( footName, toeName, mo=True, controls=False )
    footRollControl, footRollValue = sfmUtils.CreateControlledValue( footRollControlName, "value", vs.AT_FLOAT, footRollDefault, animSet, shot )
    
    # Create the expressions to re-map the footroll slider value for use in the constraint and rotation operators
    toeOrientExprName = "expr_toeOrientEnable_" + sideName    
    toeOrientExpr = sfmUtils.CreateExpression( toeOrientExprName, "inrange( footRoll, 0.5001, 1.0 )", animSet )
    toeOrientExpr.SetValue( "footRoll", footRollDefault )
    
    toeRotateExprName = "expr_toeRotation_" + sideName
    toeRotateExpr = sfmUtils.CreateExpression( toeRotateExprName, "max( 0, (footRoll - 0.5) ) * 140", animSet )
    toeRotateExpr.SetValue( "footRoll", footRollDefault )
                            
    heelRotateExprName = "expr_heelRotation_" + sideName
    heelRotateExpr = sfmUtils.CreateExpression( heelRotateExprName, "max( 0, (0.5 - footRoll) ) * -100", animSet )
    heelRotateExpr.SetValue( "footRoll", footRollDefault )
        
    # Create a connection from the footroll value to all of the expressions that require it
    footRollConnName = "conn_footRoll_" + sideName
    footRollConn = sfmUtils.CreateConnection( footRollConnName, footRollValue, "value", animSet )
    footRollConn.AddOutput( toeOrientExpr, "footRoll" )
    footRollConn.AddOutput( toeRotateExpr, "footRoll" )
    footRollConn.AddOutput( heelRotateExpr, "footRoll" )
    
    # Create the connection from the toe orientation enable expression to the target weight of the 
    # toe orientation constraint, this will turn the constraint on an off based on the footRoll value
    toeOrientConnName = "conn_toeOrientExpr_" + sideName;
    toeOrientConn = sfmUtils.CreateConnection( toeOrientConnName, toeOrientExpr, "result", animSet )
    toeOrientConn.AddOutput( toeOrientTarget, "targetWeight" )
    
    # Create a rotation constraint to drive the toe rotation and connect its input to the 
    # toe rotation expression and connect its output to the reverse heel dag's orientation
    toeRotateConstraintName = "rotationConstraint_toe_" + sideName
    toeRotateConstraint = sfmUtils.CreateRotationConstraint( toeRotateConstraintName, rotationAxis, reverseHeelDag, animSet )
    
    toeRotateExprConnName = "conn_toeRotateExpr_" + sideName
    toeRotateExprConn = sfmUtils.CreateConnection( toeRotateExprConnName, toeRotateExpr, "result", animSet )
    toeRotateExprConn.AddOutput( toeRotateConstraint, "rotations", 0 );

    # Create a rotation constraint to drive the heel rotation and connect its input to the 
    # heel rotation expression and connect its output to the heel dag's orientation 
    heelRotateConstraintName = "rotationConstraint_heel_" + sideName
    heelRotateConstraint = sfmUtils.CreateRotationConstraint( heelRotateConstraintName, rotationAxis, heelDag, animSet )
    
    heelRotateExprConnName = "conn_heelRotateExpr_" + sideName
    heelRotateExprConn = sfmUtils.CreateConnection( heelRotateExprConnName, heelRotateExpr, "result", animSet )
    heelRotateExprConn.AddOutput( heelRotateConstraint, "rotations", 0 )
    
    if ( helperControlGroup != None ):
        sfmUtils.AddDagControlsToGroup( helperControlGroup, reverseHeelDag, ikHandleDag, heelDag )       
    
    if ( footControlGroup != None ):
        footControlGroup.AddControl( footRollControl )
        
    return ikHandleDag


#==================================================================================================
# Compute the direction from boneA to boneB
#==================================================================================================
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
    
   
#==================================================================================================
# Build a simple ik rig for the currently selected animation set
#==================================================================================================
def BuildRig():
    
    # Get the currently selected animation set and shot
    shot = sfm.GetCurrentShot()
    animSet = sfm.GetCurrentAnimationSet()
    gameModel = animSet.gameModel
    rootGroup = animSet.GetRootControlGroup()
    
    # Start the biped rig to which all of the controls and constraints will be added
    rig = sfm.BeginRig( "rig_babyturret_" + animSet.GetName() );
    if ( rig == None ):
        return
    
    # Change the operation mode to passthrough so changes chan be made temporarily
    sfm.SetOperationMode( "Pass" )
    
    # Move everything into the reference pose
    sfm.SelectAll()
    sfm.SetReferencePose()
    
    #==============================================================================================
    # Find the dag nodes for all of the bones in the model which will be used by the script
    #==============================================================================================
    boneRoot      = sfmUtils.FindFirstDag( [ "RootTransform" ], True )
    boneBody      = sfmUtils.FindFirstDag( [ "Base" ], True )
    
    boneRightLegUpper = sfmUtils.FindFirstDag( [ "Right_leg" ], True )
    boneRightLegLower = sfmUtils.FindFirstDag( [ "Right_rotator" ], True )
    boneRightLegFoot = sfmUtils.FindFirstDag( [ "Right_foot" ], True )
    boneRightLegToe = sfmUtils.FindFirstDag( [ "Right_toe" ], True )
    
    boneLeftLegUpper = sfmUtils.FindFirstDag( [ "Left_leg" ], True )
    boneLeftLegLower = sfmUtils.FindFirstDag( [ "Left_rotator" ], True )
    boneLeftLegFoot = sfmUtils.FindFirstDag( [ "Left_foot" ], True )
    boneLeftLegToe = sfmUtils.FindFirstDag( [ "Left_toe" ], True )
    
    boneBackLegUpper = sfmUtils.FindFirstDag( [ "back_leg" ], True )
    boneBackLegLower = sfmUtils.FindFirstDag( [ "back_leg_rotate" ], True )
    boneBackLegFoot = sfmUtils.FindFirstDag( [ "back_leg_foot1" ], True )
    boneBackLegToe = sfmUtils.FindFirstDag( [ "back_toe" ], True )
    
    boneEyelid1 = sfmUtils.FindFirstDag( [ "eyelid_upper_bone" ], True )
    boneEyelid2 = sfmUtils.FindFirstDag( [ "eyelid_lower_bone" ], True )
	
    boneEye = sfmUtils.FindFirstDag( [ "eyeball_background" ], True )
    boneEyeLight = sfmUtils.FindFirstDag( [ "eyeball_light" ], True )

    #==============================================================================================
    # Create the rig handles and constrain them to existing bones
    #==============================================================================================
    rigRoot            = sfmUtils.CreateConstrainedHandle( "rig_root",     boneRoot,    bCreateControls=False )
    rigBody         = sfmUtils.CreateConstrainedHandle( "rig_body",     boneBody,    bCreateControls=False )
    
    rigRLeg1     = sfmUtils.CreateConstrainedHandle( "rig_lleg_thigh",      boneRightLegUpper,    bCreateControls=False )
    rigRLeg2     = sfmUtils.CreateConstrainedHandle( "rig_lleg_knee",       boneRightLegLower,    bCreateControls=False )
    rigRLeg3     = sfmUtils.CreateConstrainedHandle( "rig_lleg_foot",       boneRightLegFoot,    bCreateControls=False )
    rigRLeg4     = sfmUtils.CreateConstrainedHandle( "rig_lleg_toe",       	boneRightLegToe,    bCreateControls=False )

    rigLLeg1     = sfmUtils.CreateConstrainedHandle( "rig_rleg_thigh",      boneLeftLegUpper,    bCreateControls=False )
    rigLLeg2     = sfmUtils.CreateConstrainedHandle( "rig_rleg_knee",       boneLeftLegLower,    bCreateControls=False )
    rigLLeg3     = sfmUtils.CreateConstrainedHandle( "rig_rleg_foot",       boneLeftLegFoot,    bCreateControls=False )
    rigLLeg4     = sfmUtils.CreateConstrainedHandle( "rig_rleg_toe",       boneLeftLegToe,    bCreateControls=False )
    
    rigBLeg1     = sfmUtils.CreateConstrainedHandle( "rig_bleg_thigh",      boneBackLegUpper,    bCreateControls=False )
    rigBLeg2     = sfmUtils.CreateConstrainedHandle( "rig_bleg_knee",       boneBackLegLower,    bCreateControls=False )
    rigBLeg3     = sfmUtils.CreateConstrainedHandle( "rig_bleg_foot",       boneBackLegFoot,    bCreateControls=False )
    rigBLeg4     = sfmUtils.CreateConstrainedHandle( "rig_bleg_toe",       boneBackLegToe,    bCreateControls=False )

    rigRLegKnee   = sfmUtils.CreateOffsetHandle( "rig_lleg_IK_knee",  boneRightLegFoot, vs.Vector( 0, 0, 3 ),  bCreateControls=False )   
    rigLLegKnee   = sfmUtils.CreateOffsetHandle( "rig_rleg_IK_knee",  boneLeftLegFoot, vs.Vector( 0, 0, 3 ),  bCreateControls=False )   
    rigBLegKnee   = sfmUtils.CreateOffsetHandle( "rig_bleg_IK_knee",  boneBackLegFoot, vs.Vector( 0, 0, 3 ),  bCreateControls=False )   
    
    rigEyelid1     = sfmUtils.CreateConstrainedHandle( "rig_eyelid_upper",       boneEyelid1,    bCreateControls=False )
    rigEyelid2     = sfmUtils.CreateConstrainedHandle( "rig_eyelid_lower",       boneEyelid2,    bCreateControls=False )
	
    rigEye     = sfmUtils.CreateConstrainedHandle( "rig_eye",       boneEye,    bCreateControls=False )
    rigEyeLight     = sfmUtils.CreateConstrainedHandle( "rig_eye_light",       boneEyeLight,    bCreateControls=False )
    
    ## Create a list of all of the rig dags
    allRigHandles = [ rigRoot, rigBody, 
    rigRLeg1, rigRLeg2, rigRLeg3, rigRLeg4, rigRLegKnee,
    rigLLeg1, rigLLeg2, rigLLeg3, rigLLeg4, rigLLegKnee,
    rigBLeg1, rigBLeg2, rigBLeg3, rigBLeg4, rigBLegKnee,
    rigEyelid1, rigEyelid2, rigEye, rigEyeLight
    ];
    
    #==============================================================================================
    # Generate the world space logs for the rig handles and remove the constraints
    #==============================================================================================
    sfm.ClearSelection()
    sfmUtils.SelectDagList( allRigHandles )
    sfm.GenerateSamples()
    sfm.RemoveConstraints()    
    
    
    #==============================================================================================
    # Build the rig handle hierarchy
    #==============================================================================================
    sfmUtils.ParentMaintainWorld( rigBody,        rigRoot )
    
    sfmUtils.ParentMaintainWorld( rigRLeg1,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigRLeg2,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigRLeg3,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigRLeg4,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigRLegKnee,     rigRLeg3 )
	
    sfmUtils.ParentMaintainWorld( rigLLeg1,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLLeg2,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLLeg3,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLLeg4,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigLLegKnee,     rigLLeg3 )
	
    sfmUtils.ParentMaintainWorld( rigBLeg1,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigBLeg2,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigBLeg3,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigBLeg4,        rigRoot )
    sfmUtils.ParentMaintainWorld( rigBLegKnee,     rigBLeg3 )
	
    sfmUtils.ParentMaintainWorld( rigEyelid1,      rigBody )
    sfmUtils.ParentMaintainWorld( rigEyelid2,      rigBody )
    sfmUtils.ParentMaintainWorld( rigEye,     	   rigBody )
    sfmUtils.ParentMaintainWorld( rigEyeLight,     rigEye )
    
    # Create the hips control, this allows a pelvis rotation that does not effect the spine,
    # it is only used for rotation so a position control is not created. Additionally add the
    # new control to the selection so the that set default call operates on it too.
    #rigHips = sfmUtils.CreateHandleAt( "rig_hips", rigPelvis, False, True )
    #sfmUtils.Parent( rigHips, rigPelvis, vs.REPARENT_LOGS_OVERWRITE )
    #sfm.SelectDag( rigHips )

    # Set the defaults of the rig transforms to the current locations. Defaults are stored in local
    # space, so while the parent operation tries to preserve default values it is cleaner to just
    # set them once the final hierarchy is constructed.
    #sfm.SetDefault()
        
    #==============================================================================================
    # Create the reverse foot controls for both the left and right foot
    #==============================================================================================
    rigLegsGroup = rootGroup.CreateControlGroup( "Rig Legs" )
	
    footIKTargetR = rigRLeg3
    footIKTargetL = rigLLeg3
    footIKTargetB = rigBLeg3
	
    
    #==============================================================================================
    # Create constraints to drive the bone transforms using the rig handles
    #==============================================================================================
    
    # The following bones are simply constrained directly to a rig handle
    sfmUtils.CreatePointOrientConstraint( rigRoot,      boneRoot  )
    sfmUtils.CreatePointOrientConstraint( rigBody,      boneBody  )
    sfmUtils.CreatePointOrientConstraint( rigEyelid1,   boneEyelid1  )
    sfmUtils.CreatePointOrientConstraint( rigEyelid2,   boneEyelid2  )
    sfmUtils.CreatePointOrientConstraint( rigEye,   	boneEye  )
    sfmUtils.CreatePointOrientConstraint( rigEyeLight,   boneEyeLight  )
    
    # Create ik constraints for the arms and legs that will control the rotation of the hip / knee and 
    # upper arm / elbow joints based on the position of the foot and hand respectively.
    # def BuildArmLeg( rigPVTarget, rigEndTarget, bipStart, bipEnd, constrainEnd, group=None ) :
    sfmUtils.BuildArmLeg( rigRLegKnee,  footIKTargetR, boneRightLegUpper,  boneRightLegFoot, True )
    sfmUtils.BuildArmLeg( rigLLegKnee,  footIKTargetL, boneLeftLegUpper,  boneLeftLegFoot, True )
    sfmUtils.BuildArmLeg( rigBLegKnee,  footIKTargetB, boneBackLegUpper,  boneBackLegFoot, True )
    
    
    #==============================================================================================
    # Create handles for the important attachment points 
    #==============================================================================================    
    #attachmentGroup = rootGroup.CreateControlGroup( "Attachments" )  
    #attachmentGroup.SetVisible( False )
    
    #sfmUtils.CreateAttachmentHandleInGroup( "pvt_heel_R",       attachmentGroup )
    #sfmUtils.CreateAttachmentHandleInGroup( "pvt_toe_R",        attachmentGroup )
    #sfmUtils.CreateAttachmentHandleInGroup( "pvt_outerFoot_R",  attachmentGroup )
    #sfmUtils.CreateAttachmentHandleInGroup( "pvt_innerFoot_R",  attachmentGroup )
    
    #sfmUtils.CreateAttachmentHandleInGroup( "pvt_heel_L",       attachmentGroup )
    #sfmUtils.CreateAttachmentHandleInGroup( "pvt_toe_L",        attachmentGroup )
    #sfmUtils.CreateAttachmentHandleInGroup( "pvt_outerFoot_L",  attachmentGroup )
    #sfmUtils.CreateAttachmentHandleInGroup( "pvt_innerFoot_L",  attachmentGroup )
    
    #==============================================================================================
    # Re-organize the selection groups
    #==============================================================================================  
	
    rigMiscGroup = rootGroup.CreateControlGroup( "Rig Junk" )
    rigMiscGroup.SetVisible( False )
    rigMiscGroup.SetSnappable( False )
    sfmUtils.AddDagControlsToGroup( rigMiscGroup, rigRLeg4, rigLLeg4, rigBLeg4 )
	
    rigBodyGroup = rootGroup.CreateControlGroup( "Rig Body" )    
    sfmUtils.AddDagControlsToGroup( rigBodyGroup, rigRoot, rigBody )  
	
    RightLegGroup = rootGroup.CreateControlGroup( "Left" )
    LeftLegGroup = rootGroup.CreateControlGroup( "Right" )         
    BackLegGroup = rootGroup.CreateControlGroup( "Back" )         
    rigLegsGroup.AddChild( RightLegGroup )
    rigLegsGroup.AddChild( LeftLegGroup )
    rigLegsGroup.AddChild( BackLegGroup )
    sfmUtils.AddDagControlsToGroup( RightLegGroup, rigRLeg1, rigRLeg2, rigRLeg3, rigRLegKnee )
    sfmUtils.AddDagControlsToGroup( LeftLegGroup, rigLLeg1, rigLLeg2, rigLLeg3, rigLLegKnee )
    sfmUtils.AddDagControlsToGroup( BackLegGroup, rigBLeg1, rigBLeg2, rigBLeg3, rigBLegKnee )
	
    rigMiscGroup = rootGroup.CreateControlGroup( "Rig Misc" ) 
    sfmUtils.AddDagControlsToGroup( rigMiscGroup, rigEyelid1, rigEyelid2, rigEye, rigEyeLight )
    
    # Set the control group visiblity, this is done through the rig so it can track which
    # groups it hid, so they can be set back to being visible when the rig is detached.
    HideControlGroups( rig, rootGroup, "Body", "Arms", "Legs", "Unknown", "Other", "Root" )      
        
    #Re-order the groups
    rootGroup.MoveChildToBottom( rigBodyGroup )
    rootGroup.MoveChildToBottom( rigLegsGroup )  
    
    #==============================================================================================
    # Set the selection groups colors
    #==============================================================================================
    topLevelColor = vs.Color( 0, 128, 255, 255 )
    RightColor = vs.Color( 255, 180, 180, 255 )
    LeftColor = vs.Color( 180, 255, 180, 255 )
    BackColor = vs.Color( 180, 180, 255, 255 )
    
    rigBodyGroup.SetGroupColor( topLevelColor, False )
    rigLegsGroup.SetGroupColor( topLevelColor, False )
    rigMiscGroup.SetGroupColor( topLevelColor, False )
    
    RightLegGroup.SetGroupColor( RightColor, False )
    LeftLegGroup.SetGroupColor( LeftColor, False )
    BackLegGroup.SetGroupColor( BackColor, False )
    
    
    # End the rig definition
    sfm.EndRig()

    return
    
#==================================================================================================
# Script entry
#==================================================================================================

# Construct the rig for the selected animation set
BuildRig();

