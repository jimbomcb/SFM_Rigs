# Adds dilation controllers for pupils.
# - John McBroom

import vs
import asset

def SetupDilation( animSet, shot, group, name, material ):
	print "Creating dilation controllers for "+material
	dilationMaster, dilationMasterValue = sfmUtils.CreateControlledValue("dilation_"+name, "value", vs.AT_FLOAT, 0.0, animSet, shot)	
	group.AddControl(dilationMaster)	
	dilationConnection = sfmUtils.CreateConnection( "dilationConnection"+name, dilationMasterValue, "value", animSet )	

	# Create our material vars
	dilationElement = vs.CreateElement('DmeMaterial', 'dilation_'+name, shot.GetFileId() )
	dilationElement.SetValue('mtlName', material )
	dilationElement.SetValue( '$dilation', 0.0 )
	animSet.gameModel.materials.AddToTail(dilationElement)

	control = sfmUtils.CreateControlAndChannel('dilationControl', vs.AT_FLOAT, 0.0, animSet, shot)
	control.channel.SetOutput(dilationElement, '$dilation')
	dilationConnection.AddOutput(dilationElement, '$dilation')
	
def BuildRig():

	shot = sfm.GetCurrentShot()
	animSet = sfm.GetCurrentAnimationSet()
	rootGroup = animSet.GetRootControlGroup()
	gameModel = animSet.gameModel
	shdr = gameModel.GetStudioHdr()
	topLevelColor = vs.Color( 0, 128, 255, 255 )
	RightColor = vs.Color( 255, 100, 100, 255 )
	LeftColor = vs.Color( 100, 255, 100, 255 )
	gameModel.AddAttribute( 'materials', vs.AT_ELEMENT_ARRAY )

	print 'Adding pupil dilation control...'

	# Create our control group
	dilationGroup = animSet.FindOrAddControlGroup( animSet.GetRootControlGroup(), 'Dilation' )
	dilationGroup.SetGroupColor( topLevelColor, False )	

	# Check if we have a special model
	if ( gameModel.GetModelName() == "models/player/director.mdl" ):
		SetupDilation( animSet, shot, dilationGroup, "eyeball_l", "models/player/director/eyeball_l" )
		SetupDilation( animSet, shot, dilationGroup, "eyeball_r", "models/player/director/eyeball_r" )
	else: # Otherwise, just fall back to a generic way, will work for TF2 models, MAYBE l4d...		
		for i in range(shdr.numtextures):
			matpath = shdr.pTexture(i).pszName()
			if ( matpath.find( "eyeball" ) != -1 ):
				materialName = matpath.rsplit('/',1)[-1]
				SetupDilation( animSet, shot, dilationGroup, materialName, matpath )
				
	return

BuildRig();