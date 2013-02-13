# Master script, writes out light curves to a file, read by curvecopy_slave.
# - John McBroom

import vs, vs.datamodel
import vs.dmeutils
from pprint import pprint
import json
from vsUtils import iterAttrs

animSet = sfm.GetCurrentAnimationSet()
rootGroup = animSet.GetRootControlGroup()
shot = sfm.GetCurrentShot()

## Read our curve data
f = open('sibling_copier_data', 'r')
controls_master = json.loads(f.read())
f.close()

## This little snippet from http://facepunch.com/showthread.php?t=1239038&p=39291934&viewfull=1#post39291934
allAnimSets = []
for i in shot.iterAttrs():
    if i.GetName() == "animationSets": 
        for j in i: allAnimSets.append(j)
        break

## Apply our curve data to target anim set.
for control_name,curve_data in controls_master.iteritems():
    print "Handling control "+control_name
    elem_control = rootGroup.FindControlByName( str(control_name), True ) # Do a recursive search for our control
    
    ## First, we want to clear out any old keys.    
    times = vs.tier1.CUtlVectorTime()
    values = vs.tier1.CUtlVectorFloat()    
    elem_control.channel.log.layers[0].GetAllKeys(times,values)
    for key in range(times.Count()): elem_control.channel.log.layers[0].RemoveKeys( times[key] )
    
    ## Now, insert our new data
    for data in curve_data:
        time = data[0]
        value = data[1]
        elem_control.channel.log.layers[0].InsertKey( vs.DmeTime_t(time), value )
    
    #elem_control.channel.log.layers[0].RemoveKey( 0 )
