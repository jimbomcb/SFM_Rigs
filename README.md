SFM_Rigs
========

Rigging scripts for Source Filmmaker!

*Installation*
-
Drop the *.py file into SourceFilmmaker\game\platform\scripts\sfm\animset, the rig scripts are now accessible from the rightclick->rig menu on animation sets.

*rig_headcrabs*
-
Rigging for the 3 headcrabs, requires custom model, can be found [here](http://steamcommunity.com/groups/OpenSourceFilmmaker/discussions/2/864945865074664734/)

*rig_turret_babby*
-
Rigging for baby turret, requires custom model, can be found [here](http://steamcommunity.com/groups/OpenSourceFilmmaker/discussions/2/864945179793303189/)

*rig_blackmesa*
-
Rigging for Black Mesa models! Requires an installed and mounted version of the [Black Mesa mod](http://blackmesasource.com).

This is an all-in-one script that works with multiple models. This is my attempt at rigging all current models which aren't functional with the standard biped rig.

Currently supports:

Aliens:

* Alient Grunt
  * Known Issues:
    * IK rigging on the legs have some issues, their legs have 3 bones whereas our IK rigs only support 2 bones.
* Bullsquid
* Gargantua
* Houndeye

Humans:

* Assassin 
  * Features:
    * Support for cloaking. When the rig is added to the assassin, there will be a new AssassinCloak controller, allowing you to control the levels of the cloaking through the graph editor.  

Robots:

* Loader Robot - REQUIRES: https://dl.jimbomcb.net/sfm/sfm_loader/sfm_loader.zip
  * Known Issues:
    * Piston joints are currently broken due to issues with locking to IK constrained bones. Either animate manually or remove from the shot.  


*By*
--

John 'jimbomcb' McBroom