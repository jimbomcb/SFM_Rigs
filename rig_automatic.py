## JSON rigging script
## - jimbomcb@gmail.com

# constraint_type
# 0 = sfmUtils.CreatePointOrientConstraint
# 1 = CreatePointConstraint
# 2 = CreateOrientConstraint

# SAMPLE!

# {
	# "settings": {
		# "colours":{
			# "topLevel":		[40, 160, 255],
		# }
	# },
	
    # "drone": {
        # "models": ["models/aliens/drone/drone.mdl"],
        # "categories": {
            # "RigBody": {
				# "colour": "topLevel",
                # "children": {}
            # }
        # },
        # "rig": {
            # "rigBase": {
                # "category": "RigBody",
                # "bone": "root",
                # "parent": "root" # The root bone is automatically generated for all models.
            # },
        # }
    # }
# }

import vs
import sfm
import os
import json
import urllib2

from vs import dmeutils
animUtils = dmeutils.CDmAnimUtils
    
json_url = "https://dl.jimbomcb.net.s3.amazonaws.com/rigger/rig_feed.json"
isLocal = False

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
    
def SetupCategory( list, rootGroup, colours, level = 1, parent = None ):
    for i in list:
    
        indents = ""
        for _ in range(level):
            indents += "-"
        DebugMsg( indents+" Created "+i )
        
        list[i]["_category"] = rootGroup.CreateControlGroup( i )
        
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
        json_data=open('platform/scripts/sfm/animset/jimbomcb/rig_feed.json')
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
    rig = sfm.BeginRig( "rig_" + animSet.GetName() );
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
        	
    # Grab our Dags
    DebugMsg( "Finding dags..." )
    boneRoot = sfmUtils.FindFirstDag( [ "RootTransform" ], True )
    for i in ourModel["rig"]:
        if ( i == "rig_root" ):
            raise Exception("UH OH! Someone is trying to use \"rig_root\", this is already automatically generated on rootTransform")
        DebugMsg( "- Finding "+ourModel["rig"][i]["bone"] )
        ourModel["rig"][i]["_dag"] = sfmUtils.FindFirstDag( [ ourModel["rig"][i]["bone"] ], True )
    
    # Generate handles
    DebugMsg( "Generating handles..." )
    rigRoot = sfmUtils.CreateConstrainedHandle( "rig_root",  boneRoot,  bCreateControls=False )
    allRigHandles = [ rigRoot ];
    for i in ourModel["rig"]:   
        DebugMsg( "- Created handle: "+i+" for "+ourModel["rig"][i]["bone"] )
        ourModel["rig"][i]["_rig"] = sfmUtils.CreateConstrainedHandle( i, ourModel["rig"][i]["_dag"], bCreateControls=False )
        allRigHandles += [ ourModel["rig"][i]["_rig"] ]
    
    sfm.ClearSelection()
    sfmUtils.SelectDagList( allRigHandles )
    sfm.GenerateSamples()
    sfm.RemoveConstraints()  
     
    # Setting up parents
    DebugMsg( "Setting up parents..." )
    for i in ourModel["rig"]:
        thisBone = ourModel["rig"][i]
        if ( thisBone["parent"] == "root" ):
            DebugMsg( "- Parenting "+i+" to root!" )
            sfmUtils.ParentMaintainWorld( thisBone["_rig"], rigRoot )
        elif ( thisBone["parent"] != False ):
            parentBone = ourModel["rig"][thisBone["parent"]]
            DebugMsg( "- Parenting "+i+" to "+thisBone["parent"]+"!" )
            sfmUtils.ParentMaintainWorld( thisBone["_rig"], parentBone["_rig"] )
        
    sfm.SetDefault()
    
    # Set up handle constraints
    DebugMsg( "Setting up handle constraints..." )
    for i in ourModel["rig"]:
        thisName = i
        thisRig = ourModel["rig"][i]["_rig"]
        thisDag = ourModel["rig"][i]["_dag"]
        
        if "constraint_type" in ourModel["rig"][i]:
            if ( ourModel["rig"][i]["constraint_type"] == 1 ):
                DebugMsg( "- Constraining "+thisName+" with CreatePointConstraint." )
                CreatePointConstraint( thisRig, thisDag )
                continue                
            if ( ourModel["rig"][i]["constraint_type"] == 2 ):
                DebugMsg( "- Constraining "+thisName+" with CreateOrientConstraint." )
                CreateOrientConstraint( thisRig, thisDag )
                continue
                
        DebugMsg( "- Constraining "+thisName+" with CreatePointOrientConstraint." )
        sfmUtils.CreatePointOrientConstraint( thisRig, thisDag )
        
    # ARMS AND LEGS - TODO
    
    # Set up categories
    DebugMsg( "Setting up categories..." )
    HideControlGroups( rig, rootGroup, "Body", "Arms", "Legs", "Unknown", "Other", "Root" )
    ourModel["categories"] = SetupCategory( ourModel["categories"], rootGroup,  json_rig["settings"]["colours"] )
        
    DebugMsg( "Applying categories..." )
    for i in ourModel["rig"]:
        thisRig = ourModel["rig"][i]
        thisCategory = FindCategory( ourModel["categories"], thisRig["category"] )
        DebugMsg( "- Adding "+i+" to "+thisRig["category"] )
        sfmUtils.AddDagControlsToGroup( thisCategory, thisRig["_rig"] )	
    
    sfm.EndRig()
    print "Done."
			
    return
    
BuildRig();
