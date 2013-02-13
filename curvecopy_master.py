# Master script, writes out light curves to a file, read by curvecopy_slave.
# - John McBroom

import vs, vs.datamodel
from pprint import pprint
import json

controls_to_copy = ["intensity","ambientIntensity","horizontalFOV","verticalFOV","radius",
                    "shadowFilterSize","shadowAtten","minDistance","maxDistance",
                    "constantAttenuation","linearAttenuation","quadraticAttenuation",
                    "shadowDepthBias","shadowSlopeScaleDepthBias","farZAtten",
                    "nearEdge","farEdge","cutOn","cutOff","volumetricIntensity",
                    "noiseStrength","width","height","edgeWidth","edgeHeight",
                    "color_red","color_blue","color_green","color_alpha"]
controls_master = {}

animSet = sfm.GetCurrentAnimationSet()
rootGroup = animSet.GetRootControlGroup()

## Get the keys we want from our controls.
for control in controls_to_copy:
    print "Copying curve "+control
    elem_control = rootGroup.FindControlByName( control, True ) # Do a recursive search for our control
    times = vs.tier1.CUtlVectorTime()
    values = vs.tier1.CUtlVectorFloat()
    elem_control.channel.log.layers[0].GetAllKeys(times,values) # And get all the keys.
    controls_master[control] = []
    for key in range(times.Count()):
        controls_master[control].append([times[key].GetTenthsOfMS(),values[key]])
        
## Dump our data out into a file for copying to other animsets.
f = open('sibling_copier_data', 'w')
f.write(json.dumps( controls_master ))
f.close()

print "Dumped curve data to 'sibling_copier_data'"