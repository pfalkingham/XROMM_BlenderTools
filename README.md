# XROMM_BlenderTools
A version of the XROMM Maya Tools (https://bitbucket.org/xromm/xromm_mayatools), but for blender 

Download latest release here: https://github.com/pfalkingham/XROMM_BlenderTools/releases

## A warning ##
The experts of XROMM are still using Maya.  Don't expect much help if you use this. In fact, I _strongly_ recommend you don't use this for anything important just yet! 

## YouTube video ##

You can see it working here: https://youtu.be/zRH4XBChrgA

## --In Progress--

Original Maya tools written by <a href="https://biology.providence.edu/faculty-members/david-baier/">Dave Baier</a> (supported by the US National Science Foundation through an Advances in Biological Informatics grant to PI <a href = "https://vivo.brown.edu/display/ebrainer">Elizabeth Brainerd</a> and CoPIs <a href="https://vivo.brown.edu/display/sgatesy">Stephen Gatesy</a> and David Baier, see link above)

I aim to replicate functionality, rather than code.  Maya isn't for everyone - it takes ages to start up, installs a bunch of cruft that runs in the background (Autodesk app), and is generally not seeing much active development to the UX.  Blender is free and open source, which is far better situation for a set of science tools.  Blender is also much quicker, and more in the community are generally more familiar with it.

Below is a to-do list, in order of priority.  The priority is based on replicating the tools I use most.  Others are welcome to contribute.

# To Do

## High priority:

~~-- Addon UI: Essentially the equivelent of the MayaTools shelf, a way to interact with the scripts.~~

~~-- Xcam import (based on mayacamsv2): import cameras and image planes as exported from XMALab~~  DONE!

----[optional] Xcam import based on mayacamsv1 <- is there really any need?  Lot of work to support out-dated xcam format.

-- import:  ~~can import rigid body transormations~~, xyz coordinates to new objects, ~~objs~~.  

 
~~-- axes: create axes at joints.~~

~~-- oRel: calculates relative motion between two axes.~~

~~-- jAx: Joint axes integral to some peoples workflows~~ - This is now done, as can be accomplished through creating axes, then running relative motion.
 
## Low Priority 

~~-- CT export: Exports xyz coordinates of CT markers~~

~~-- vAvg: Calculates average position of a selection of verticies and puts a locator there (related to the above)~~

~~-- exp: Export data.  Complex, and native albeit cumbersome methods exist in blender, or can be scripted later.~~

## Low Priority because I don't use them, but useful to others.

-- jcs: Joint coordinate system, not sure I've ever used this.

## No plans to implement:

-- PSDR: pan/scan for looking through xcams.  Blender handles this differently and you can do this natively without the need for PSDR.
-- PStrn: Shader related - may leave this out and handle manually in blender.  Not vital, so may be implemented much later.
