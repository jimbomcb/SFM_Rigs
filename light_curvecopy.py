# When ran, copies all values from the light to other lights in this shot that aren't unselectable.
# - John McBroom

import vs
from pprint import pprint
from vsUtils import iterAttrs
from vs.mathlib import *

animSet = sfm.GetCurrentAnimationSet()
rootGroup = animSet.GetRootControlGroup()
shot = sfm.GetCurrentShot()

controls_to_copy = ["intensity","ambientIntensity","horizontalFOV","verticalFOV","radius",
                    "shadowFilterSize","shadowAtten","minDistance","maxDistance",
                    "constantAttenuation","linearAttenuation","quadraticAttenuation",
                    "shadowDepthBias","shadowSlopeScaleDepthBias","farZAtten",
                    "nearEdge","farEdge","cutOn","cutOff","volumetricIntensity",
                    "noiseStrength","width","height","edgeWidth","edgeHeight",
                    "color_red","color_blue","color_green","color_alpha"]
controls_master = {}
controls_master_transform = {} # Our vector3 transforms are a different beast than the other float logs, let's handle it differently
controls_master_name = animSet.GetName()

## Get the keys we want from our controls.
for control in controls_to_copy:
    elem_control = rootGroup.FindControlByName( control, True ) # Do a recursive search for our control
    times = vs.tier1.CUtlVectorTime()
    values = vs.tier1.CUtlVectorFloat()
    elem_control.channel.log.layers[0].GetAllKeys(times,values) # And get all the keys.
    controls_master[control] = []
    for key in range(times.Count()): controls_master[control].append((times[key].GetTenthsOfMS(),values[key]))

# Also get transform, we handle it slightly differently.
master_transform = rootGroup.FindControlByName( "transform", True ) # Do a recursive search for our control

# Position
times = vs.tier1.CUtlVectorTime()
values = vs.tier1.CUtlVectorVector()
master_transform.GetPositionChannel().log.layers[0].GetAllKeys(times,values) # And get all the keys.
controls_master_init_position = values[0]
controls_master_transform["position"] = []
for key in range(times.Count()): controls_master_transform["position"].append((times[key].GetTenthsOfMS(),values[key]-controls_master_init_position))

# Rotation
times = vs.tier1.CUtlVectorTime()
values = vs.tier1.CUtlVectorQuaternion()
master_transform.GetOrientationChannel().log.layers[0].GetAllKeys(times,values) # And get all the keys.
controls_master_init_orientation = values[0].AsRadianEuler().ToQAngle()
controls_master_transform["orientation"] = []
for key in range(times.Count()): controls_master_transform["orientation"].append((times[key].GetTenthsOfMS(),values[key].AsRadianEuler().ToQAngle() - controls_master_init_orientation))

## This little snippet from http://facepunch.com/showthread.php?t=1239038&p=39291934&viewfull=1#post39291934
allAnimSets = []
for i in shot.iterAttrs():
    if i.GetName() == "animationSets": 
        for j in i: allAnimSets.append(j)
        break

for sibling_anim in allAnimSets:
    
    sibling_rootGroup = sibling_anim.GetRootControlGroup()
    
    if not sibling_anim.HasAttribute("light"): continue # Skip anything that isn't a light.
    if not sibling_rootGroup.IsSelectable(): continue # Skip non-selectable lights
    if controls_master_name == sibling_anim.GetName(): continue # Skip our master

    for control_name,curve_data in controls_master.iteritems():        
        elem_control = sibling_rootGroup.FindControlByName( str(control_name), True ) # Do a recursive search for our control
        
        ## First, we want to clear out any old keys.    
        times = vs.tier1.CUtlVectorTime()
        values = vs.tier1.CUtlVectorFloat()    
        elem_control.channel.log.layers[0].GetAllKeys(times,values)
        for key in range(times.Count()): elem_control.channel.log.layers[0].RemoveKeys( times[key] )
        
        ## Now, insert our new data
        for time,value in curve_data:
            elem_control.channel.log.layers[0].InsertKey( vs.DmeTime_t(time), value )
    
    # Now, our transforms.
    sibling_transform = sibling_rootGroup.FindControlByName( "transform", True )
    
    #Scrap our old keys
    # Position
    times = vs.tier1.CUtlVectorTime()
    values = vs.tier1.CUtlVectorVector()
    sibling_transform.GetPositionChannel().log.layers[0].GetAllKeys(times,values) # And get all the keys.
    our_position = values[0]
    for key in range(times.Count()): sibling_transform.GetPositionChannel().log.layers[0].RemoveKeys( times[key] )
    
    for time,pos in controls_master_transform["position"]:
        sibling_transform.GetPositionChannel().log.layers[0].InsertKey( vs.DmeTime_t(time), our_position + pos )
        
    # Orientation
    times = vs.tier1.CUtlVectorTime()
    values = vs.tier1.CUtlVectorQuaternion()
    sibling_transform.GetOrientationChannel().log.layers[0].GetAllKeys(times,values) # And get all the keys.
    our_orientation = values[0].AsRadianEuler().ToQAngle()
    for key in range(times.Count()): sibling_transform.GetOrientationChannel().log.layers[0].RemoveKeys( times[key] )
    
    for time,orientation in controls_master_transform["orientation"]:
        new_orientation = Quaternion(RadianEuler(our_orientation + orientation))
        sibling_transform.GetOrientationChannel().log.layers[0].InsertKey( vs.DmeTime_t(time), new_orientation )
    



