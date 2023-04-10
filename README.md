# XROMM_BlenderTools
A version of the XROMM Maya Tools (https://bitbucket.org/xromm/xromm_mayatools), but for blender 

## --In Progress--

Original Maya tools written by Dave Baier (supported by the US National Science Foundation through an Advances in Biological Informatics grant to PI Elizabeth Brainerd and CoPIs Stephen Gatesy and David Baier, see link above)

I aim to replicate functionality, rather than code.  Maya has become a bloated mess of a software package, takes ages to start up, installs a bunch of cruft (Autodesk app), and is generally not seeing much active development.  Blender is free and open source, which is far better situation for a set of science tools.  Blender is also much quicker, and more in the community are familiar with it.

This repository is so in progress, nothing has been added yet :)

Below is a to-do list, in order of priority.  The priority is based on replicating the tools I use most.  Others are welcome to contribute.

# To Do

## High priority:

-- Addon UI: Essentially the equivelent of the MayaTools shelf, a way to interact with the scripts.

-- Xcam import (based on xcam02): import cameras and image planes as exported from XMALab

-- imp:  can import rigid body transormations, xyz coordinates, objs.  This is integral to animation, but also the most complex tool
 
-- axes: create axes at joints.

-- oRel: calculates relative motion between two axes.
 
## Low Priority 

-- CT export: Exports xyz coordinates of CT markers

-- vAvg: Calculates average position of a selection of verticies and puts a locator there

-- exp: Export data.  Complex, and native albeit cumbersome methods exist natively in blender, or can be scripted later.

## Low Priority because I don't use them, but definately useful.

-- jAx: Joint axes, not something I've used recently, but integral to some peoples workflows

-- jcs: Joint coordinate system, as above.

## No plans to implement:

-- PSDR: pan/scan for looking through xcams.  Blender handles this differently, may be native
-- PStrn: Shader related - may leave this out and handle manually in blender.  Not vital, so may be implemented much later.
