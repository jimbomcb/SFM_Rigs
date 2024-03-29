## JSON rigging script
## - jimbomcb@gmail.com

# constraint_type
# 0 = sfmUtils.CreatePointOrientConstraint
# 1 = CreatePointConstraint
# 2 = CreateOrientConstraint

import vs
import sfm
import os
import json
import urllib2

from vs import dmeutils
animUtils = dmeutils.CDmAnimUtils
    
filesystem_path = "platform/scripts/sfm/animset/json_rigger/rig_feed.json" ## If the filesystem path exists, we use it, otherwise grab the URL.
json_url = "https://json.rigger.s3.amazonaws.com/rig_feed.json"
isLocal = ( os.path.isfile(filesystem_path) )

IK_NONE = 0
IK_THIGH = 1
IK_KNEE = 2
IK_FOOT = 3
IK_KNEE_HELPER = 4

def DebugMsg( msg ):
    if ( isLocal == True ):
        print "JSONRIG: "+msg

def FindCategory( list, name ):
    for i in list:
        if ( i == name ):
            return list[i]["_category"]       
        if "children" in list[i]:
            foundChild = FindCategory( list[i]["children"], name )
            if ( foundChild != None ):
                return foundChild    
    return None
    
def FindCategoryParent( list, name, default ):
    for i in list:    
        if ( name == i ):
            return default
        if "children" in list[i]:
            foundChild = FindCategoryParent( list[i]["children"], name, default )
            if ( foundChild != False ):
                return list[i]["_category"]    
    return False
    
def SetupCategory( list, rootGroup, colours, level = 1, parent = None ):
    for i in list:
    
        indents = ""
        for _ in range(level):
            indents += "-"
        DebugMsg( indents+" Created "+str(i) )
        
        list[i]["_category"] = rootGroup.CreateControlGroup( str(i) )
        
        if ( parent != None ):
            parent.AddChild( list[i]["_category"] )	
        
        if "colour" in list[i]:
            if list[i]["colour"] in colours:
                thisCol = colours[list[i]["colour"]]
                DebugMsg( indents+" Setting colour to "+list[i]["colour"] )
                list[i]["_category"].SetGroupColor( vs.Color(thisCol[0],thisCol[1],thisCol[2],255), False )                
                
        if "children" in list[i]:
            list[i]["children"] = SetupCategory( list[i]["children"], rootGroup, colours, level + 1, list[i]["_category"] )  
                
    return list

def IsInIKJoint( list, name ):

    for i in list:   
        if ( i["start"] == name ):
            return IK_THIGH 
        if ( i["middle"] == name ):
            return IK_KNEE
        if ( i["end"] == name ):
            return IK_FOOT  
        if ( i["knee"] == name ):
            return IK_KNEE_HELPER
        
    return IK_NONE
 
    
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

    if ( isLocal == False ) :
        print "Reading JSON Rigging script from "+json_url
        try:
            resp = urllib2.urlopen(json_url)
        except urllib2.URLError, e:
            raise Exception("Grabbing json failed! - "+str(e.getcode()))
            
        json_rig = json.load(resp)
    else:
        print "Reading JSON Rigging script from "+filesystem_path
        json_data=open(filesystem_path)
        json_rig = json.load(json_data)
        json_data.close()
        
    if ( "settings" not in json_rig ):
        raise Exception("JSON ERROR: No settings defined!");
        
    if ( "colours" not in json_rig["settings"] ):
        raise Exception("JSON ERROR: No colours defined!");
        
    # Get the currently selected animation set and shot
    shot = sfm.GetCurrentShot()
    animSet = sfm.GetCurrentAnimationSet()
    gameModel = animSet.gameModel
    rootGroup = animSet.GetRootControlGroup()
	    
    # Start the biped rig to which all of the controls and constraints will be added
    rig = sfm.BeginRig( "autorig__" + animSet.GetName() );
    if ( rig == None ):
        return
    
    # Change the operation mode to passthrough so changes chan be made temporarily
    sfm.SetOperationMode( "Pass" )
    
    # Move everything into the reference pose
    sfm.SelectAll()
    sfm.SetReferencePose()
	
    if ( gameModel == None ) :
		raise Exception("Unable to find gameModel...??")
		
    ourModel = False
    
    for index in json_rig:               
        if ( "models" not in json_rig[index] ):
            continue
            
        for mdl in json_rig[index]["models"]:
            if ( mdl == gameModel.GetModelName() ) :
                ourModel = json_rig[index]
                DebugMsg( "Found a match, we're using "+index+" ("+mdl+")!" )
                break # Break out of this search                
        if ( ourModel != False ):
            break # And then this.
           
    if ( ourModel == False ) :
		raise Exception("Sorry! Unable to find any rig for this model. (" + gameModel.GetModelName() + ")")
        
    # Dump the json rig list into a dict
    # PS: i'm bad at python - this is so we can do ourModel["rig"][rigname] instead of having to find the right 
    # element in the list. We use the list later on because it maintains the correct order which is needed
    # for the category setup! Please show me a better way of doing this.
    ourModel["rig_dict"] = {} 
    for i in ourModel["rigs"]:
        ourModel["rig_dict"][i["name"]] = i
        	
    # Grab our Dags
    DebugMsg( "Finding dags..." )
    boneRoot = sfmUtils.FindFirstDag( [ "RootTransform" ], True )
    for i in ourModel["rig_dict"]:
        if ( i == "rig_root" ):
            raise Exception("UH OH! Someone is trying to use \"rig_root\", this is already automatically generated on rootTransform")
        DebugMsg( "- Finding "+ourModel["rig_dict"][i]["bone"] )
        ourModel["rig_dict"][i]["_dag"] = sfmUtils.FindFirstDag( [ ourModel["rig_dict"][i]["bone"] ], True )
    
    # Generate handles
    DebugMsg( "Generating handles..." )
    rigRoot = sfmUtils.CreateConstrainedHandle( "rig_root",  boneRoot,  bCreateControls=False )
    allRigHandles = [ rigRoot ];
    for i in ourModel["rig_dict"]:  
    
        iIsInIK = IsInIKJoint( ourModel["ikjoint"], i )
        if ( iIsInIK == IK_THIGH or iIsInIK == IK_KNEE ):
            ourModel["rig_dict"][i]["_rig"] = False
            continue
            
        DebugMsg( "- Created handle: "+i+" for "+ourModel["rig_dict"][i]["bone"] )
        ourModel["rig_dict"][i]["_rig"] = sfmUtils.CreateConstrainedHandle( i, ourModel["rig_dict"][i]["_dag"], bCreateControls=False )
        allRigHandles += [ ourModel["rig_dict"][i]["_rig"] ]
        
        if ( iIsInIK == IK_FOOT ): # Generate our foot helper, used for parenting stuff to it.
            DebugMsg( "- Created handle: rig_helper_"+i+" for "+ourModel["rig_dict"][i]["bone"] )
            ourModel["rig_dict"][i]["_helper"] = sfmUtils.CreateConstrainedHandle( "rig_helper_"+i, ourModel["rig_dict"][i]["_dag"], bCreateControls=False )
                    
    # Generate knee helper handles - TODO: offsets defined in json
    DebugMsg( "Generating IK PVTarget..." )
    for i in ourModel["ikjoint"]:   
        DebugMsg( "- Created IK PVtarget for "+i["knee"] )
        ikOffset = vs.Vector(0,0,0)
        
        if "offset" in i: # Check for offset, otherwise we stick to 0
            if "start" in i["offset"]: # It's not a vector, calculate vector to another bone and scale by dist.
                DebugMsg("-- Setting joint offset based on ComputeVectorBetweenBones( "+i["offset"]["start"]+","+i["offset"]["end"]+","+str(i["offset"]["dist"])+")")
                dagStart = ourModel["rig_dict"][i["offset"]["start"]]["_dag"]
                dagEnd = ourModel["rig_dict"][i["offset"]["end"]]["_dag"]
                ikOffset = ComputeVectorBetweenBones( dagStart, dagEnd, i["offset"]["dist"] )
            else:
                DebugMsg("-- Setting joint offset - vs.Vector("+str(i["offset"][0])+","+str(i["offset"][1])+","+str(i["offset"][2])+")")
                ikOffset = vs.Vector(i["offset"][0],i["offset"][1],i["offset"][2])
        
        knee_name = "rig_knee_"+i["knee"]
        if "knee_name" in i:
            knee_name = i["knee_name"]
            
        i["_knee"] = sfmUtils.CreateOffsetHandle( knee_name, ourModel["rig_dict"][i["knee"]]["_dag"], ikOffset, bCreateControls=False ) 
        allRigHandles += [ i["_knee"] ]
                
    sfm.ClearSelection()
    sfmUtils.SelectDagList( allRigHandles )
    sfm.GenerateSamples()
    sfm.RemoveConstraints()  
     
    # Setting up parents
    DebugMsg( "Setting up parents..." )
    for i in ourModel["rig_dict"]:
        thisBone = ourModel["rig_dict"][i]
        
        if ( not thisBone["_rig"] ):
            continue
        
        iIsInIK = IsInIKJoint( ourModel["ikjoint"], i )
                
        if ( iIsInIK == IK_FOOT ):
            DebugMsg( "- Parenting IK FOOT "+i+" to root!" )
            sfmUtils.ParentMaintainWorld( thisBone["_rig"], rigRoot )            
            sfmUtils.ParentMaintainWorld( thisBone["_helper"], rigRoot ) 
        elif ( iIsInIK != IK_NONE ):
            continue
        elif ( thisBone["parent"] == "root" ):
            DebugMsg( "- Parenting "+i+" to root!" )
            sfmUtils.ParentMaintainWorld( thisBone["_rig"], rigRoot )
        elif ( thisBone["parent"] != False ):
            parentBone = ourModel["rig_dict"][thisBone["parent"]]
            
            if ( not parentBone["_rig"] ):
                continue                
                
            parentRig = parentBone["_rig"]
            
            iIsParentInIK = IsInIKJoint( ourModel["ikjoint"], thisBone["parent"] )
            if ( iIsParentInIK == IK_FOOT and iIsInIK != IK_KNEE_HELPER ):
                DebugMsg( "- Parenting "+i+" to "+thisBone["parent"]+" HELPER!" )
                parentRig = parentBone["_helper"]
            else:            
                DebugMsg( "- Parenting "+i+" to "+thisBone["parent"]+"!" )
                
            sfmUtils.ParentMaintainWorld( thisBone["_rig"], parentRig )
            
    # Knee parents
    for i in ourModel["ikjoint"]:   
    
        knee_name = "rig_knee_"+i["knee"]
        if "knee_name" in i:
            knee_name = i["knee_name"]
            
        if "kneeparent" in i:
            if ( i["kneeparent"] == False ):
                DebugMsg( "- Parenting "+knee_name+" to root." )
                sfmUtils.ParentMaintainWorld( i["_knee"], rigRoot )
            else:
                DebugMsg( "- Parenting "+knee_name+" to "+i["kneeparent"]+"." )
                sfmUtils.ParentMaintainWorld( i["_knee"], ourModel["rig_dict"][i["kneeparent"]]["_rig"] )
        else:
            DebugMsg( "- Parenting "+knee_name+" to "+i["end"]+"." )
            sfmUtils.ParentMaintainWorld( i["_knee"], ourModel["rig_dict"][i["end"]]["_rig"] )
        
    sfm.SetDefault()
    
    # Set up handle constraints
    DebugMsg( "Setting up handle constraints..." )
    for i in ourModel["rig_dict"]:
        thisName = i
        thisRig = ourModel["rig_dict"][i]["_rig"]
        thisDag = ourModel["rig_dict"][i]["_dag"]
        
        if ( not thisRig ):
            continue
        
        if ( IsInIKJoint( ourModel["ikjoint"], i ) != IK_NONE ):
            continue
        
        if "constraint_type" in ourModel["rig_dict"][i]:
            if ( ourModel["rig_dict"][i]["constraint_type"] == 1 ):
                DebugMsg( "- Constraining "+thisName+" with CreatePointConstraint." )
                CreatePointConstraint( thisRig, thisDag )
                continue                
            if ( ourModel["rig_dict"][i]["constraint_type"] == 2 ):
                DebugMsg( "- Constraining "+thisName+" with CreateOrientConstraint." )
                CreateOrientConstraint( thisRig, thisDag )
                continue
                
        DebugMsg( "- Constraining "+thisName+" with CreatePointOrientConstraint." )
        sfmUtils.CreatePointOrientConstraint( thisRig, thisDag )
        
    for i in ourModel["ikjoint"]:   
        DebugMsg( "- Creating an IK joint, "+i["start"]+" - "+i["middle"]+" - "+i["end"]+" (Knee: "+i["knee"]+")" )
        ikStart = ourModel["rig_dict"][i["start"]]
        ikMiddle = ourModel["rig_dict"][i["middle"]]
        ikEnd = ourModel["rig_dict"][i["end"]]
        sfmUtils.BuildArmLeg( i["_knee"], ikEnd["_rig"], ikStart["_dag"], ikEnd["_dag"], i["constrainfoot"] )
        
    # Set up categories
    DebugMsg( "Setting up categories..." )
    HideControlGroups( rig, rootGroup, "Body", "Arms", "Legs", "Unknown", "Other", "Root" )
    ourModel["categories"] = SetupCategory( ourModel["categories"], rootGroup,  json_rig["settings"]["colours"] )
    
    rigHelpersGroup = rootGroup.CreateControlGroup( "RigHelpers" )
    rigHelpersGroup.SetVisible( False )
    rigHelpersGroup.SetSnappable( False )
        
    DebugMsg( "Applying categories..." )
    for i in ourModel["rigs"]:
        thisRig = ourModel["rig_dict"][i["name"]]        
        if ( not thisRig["_rig"] ):
            continue        
        thisCategory = FindCategory( ourModel["categories"], thisRig["category"] )
        DebugMsg( "- Adding "+i["name"]+" to "+thisRig["category"] )
        sfmUtils.AddDagControlsToGroup( thisCategory, thisRig["_rig"] )	
        
        # If we're an IK foot, we have a helper! Stick it in the helper group.        
        iIsInIK = IsInIKJoint( ourModel["ikjoint"], i["name"] )
        if ( iIsInIK == IK_FOOT ):
            sfmUtils.AddDagControlsToGroup( rigHelpersGroup, thisRig["_helper"] )
        
    for i in ourModel["ikjoint"]:
        thisRig = ourModel["rig_dict"][i["knee"]]
        thisCategory = FindCategory( ourModel["categories"], thisRig["category"] )
        DebugMsg( "- Adding "+i["knee"]+" to "+thisRig["category"] )
        sfmUtils.AddDagControlsToGroup( thisCategory, i["_knee"] )	
    
    for i in ourModel["categories_order"]:
        DebugMsg("Moving "+i+" to the bottom.")
        FindCategoryParent( ourModel["categories"], i, rootGroup ).MoveChildToBottom( FindCategory( ourModel["categories"], i ) )
    
    sfm.EndRig()
    print "Done."
    
    if ( json_rig["settings"]["outofdate"] ):
        print "!!!!!!!!!!!!!!!!!!!!!!!!"
        print "!!!!!!!!!!!!!!!!!!!!!!!!"
        print "NOTICE: Your rigging script is out of date, please download an updated version from https://raw.github.com/jimbomcb/SFM_Rigs/master/rig_automatic.py (copy from the console)"
        print "!!!!!!!!!!!!!!!!!!!!!!!!"
        print "!!!!!!!!!!!!!!!!!!!!!!!!"
			
    return
    
BuildRig();
