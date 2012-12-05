# Particle system rigger, adding various controls for timescale etc.

import vs

# butchered from sfmutils, tweaked so they actually work for what we want
def BuildControllerAndChannel( name, value, animSet, shot ):

    
    return controller
    
def CreateControllerForElementFloat( name, lo, hi, default, target, targetproperty, group, animSet, shot ):

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
    
    ## Output our final channel result to the target value/property.
    scaledChannel.SetOutput( target, targetproperty )
    
    return
    
def BuildRig():
    
    shot = sfm.GetCurrentShot()
    animSet = sfm.GetCurrentAnimationSet()
    rootGroup = animSet.GetRootControlGroup()
    particleSystem = animSet.GetValue("particle system")
    
    ## Create our main controller
        
    CreateControllerForElementFloat( "SimulationTimescale", 0.0, 2.0, 1.0, particleSystem, "simulationTimeScale", rootGroup, animSet, shot )
    
    
    return
    
BuildRig();