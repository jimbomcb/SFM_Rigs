# Adds scaling control to selfillum
# - John McBroom

import vs

def CreateIllumController( name, lo, hi, default, group, animSet, shot ):

    find_controller = animSet.FindControl( name ) 
    
    if ( find_controller != None ) :
        print "CreateIllumController - Already found illum controller, exiting to prevent any crashes"
        return
        
    default_normalized = (default-lo)/(hi-lo)
    
    ## Create main controller
    controller = animSet.FindOrAddControl( name, False )
    if ( controller != None ) :
        sfmUtils.AddElementToRig( controller, animSet )
        sfmUtils.AddAttributeToElement( controller, "value", vs.AT_FLOAT, default_normalized )
        sfmUtils.AddAttributeToElement( controller, "defaultValue", vs.AT_FLOAT, default_normalized )	
        channel = sfmUtils.CreateChannel( name, vs.AT_FLOAT, default_normalized, animSet, shot )
        if ( channel != None ) :
            controller.SetValue( "channel", channel )
            channel.SetInput( controller, "value" )
            
    group.AddControl(controller)    
    
    ## Create interpolating expression
    expression = sfmUtils.CreateExpression( name+"_rescale", "lerp(value,lo,hi)", animSet )
    sfmUtils.AddAttributeToElement( expression, "lo", vs.AT_FLOAT, lo )
    sfmUtils.AddAttributeToElement( expression, "hi", vs.AT_FLOAT, hi )
    sfmUtils.AddAttributeToElement( expression, "value", vs.AT_FLOAT, default )
    
    ## Output main controler channel into interpolation value
    controller.channel.SetOutput( expression, "value" )
        
    ## Create our channel, passes value from expression to target value.
    scaledChannel = vs.CreateElement( "DmeChannel", "scaled_"+name, shot.GetFileId() )	
    sfmUtils.AddElementToRig( scaledChannel, animSet )    
    log = vs.CreateElement( "DmeFloatLog", "float log", shot.GetFileId() )
    scaledChannel.SetLog( log )    
    channelsClip = sfmUtils.GetChannelsClipForAnimSet( animSet, shot )
    if ( channelsClip != None ) :
        channelsClip.channels.AddToTail( scaledChannel )
        
    ## Output interpolation result into our final channel
    scaledChannel.SetInput( expression, "result" )
   
    ## Loop throuhg our materials, hooking up expression output to it.
    shdr = animSet.gameModel.GetStudioHdr()
    
    for i in range(shdr.numtextures):
    
        cloak_1 = vs.CreateElement('DmeMaterial', shdr.pTexture(i).pszName(), shot.GetFileId() )
        cloak_1.SetValue('mtlName', shdr.pTexture(i).pszName() )
        cloak_1.SetValue( '$selfillumtint', 0.0 )
        animSet.gameModel.materials.AddToTail(cloak_1)
        
        scaledChannel.SetOutput(cloak_1, '$selfillumtint')
        
    return
       
    return
    
def BuildRig():
    
    shot = sfm.GetCurrentShot()
    animSet = sfm.GetCurrentAnimationSet()
    rootGroup = animSet.GetRootControlGroup()
    gameModel = animSet.gameModel
    shdr = gameModel.GetStudioHdr()
    
    if ( gameModel != None ) :
        gameModel.AddAttribute( 'materials', vs.AT_ELEMENT_ARRAY )
        
        ## Create our main controller        
        CreateIllumController( "Self Illumination Scale", 0.0, 10.0, 1.0, rootGroup, animSet, shot )
        
    return
    
BuildRig();