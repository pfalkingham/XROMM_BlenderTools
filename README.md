# XROMM_BlenderTools
A version of the XROMM Maya Tools (https://bitbucket.org/xromm/xromm_mayatools), but for blender 

Download latest release here: https://github.com/pfalkingham/XROMM_BlenderTools/releases

*Availble directly from within blender using [Blender Extensions](https://extensions.blender.org/add-ons/xromm-tools/). Go to Edit->Preferences->Get Extensions and search for 'XROMM':
![image](https://github.com/user-attachments/assets/dad68283-86d4-482b-9276-45bd03ba8388)


## A warning ##
The experts of XROMM are still using Maya.  Don't expect much help if you use this. In fact, I _strongly_ recommend you don't use this for anything important just yet! 

## YouTube video ##

You can see it working here: https://youtu.be/zRH4XBChrgA

## Development

Original Maya tools written by <a href="https://biology.providence.edu/faculty-members/david-baier/">Dave Baier</a> (supported by the US National Science Foundation through an Advances in Biological Informatics grant to PI <a href = "https://vivo.brown.edu/display/ebrainer">Elizabeth Brainerd</a> and CoPIs <a href="https://vivo.brown.edu/display/sgatesy">Stephen Gatesy</a> and David Baier, see link above)

I aim to replicate functionality, rather than code.  Maya isn't for everyone - it takes ages to start up, installs a bunch of cruft that runs in the background (Autodesk app on PC), and is generally not seeing much active development to the UX.  Blender is free and open source, which is far better situation for a set of science tools.  Blender is also much quicker, and more in the community are generally more familiar with it.

The decision on what to implement is based on replicating the tools I use most.  Others are welcome to contribute, or make requests (email me directly, or use the issues tab)

_Please report all bugs either via email or the issues tab._

# Implemented tools

-- Addon UI: Essentially the equivelent of the MayaTools shelf, a way to interact with the scripts.

-- Xcam import (based on mayacamsv2): import cameras and image planes as exported from XMALab as MayaCamsv2 (v1 not supported)

-- import:  can import rigid body transormations to objects, or xyz locations and/or rotations to new or selected objects.
 
-- axes: create axes at joints, with or without locators.

-- oRel: calculates relative motion between two objects (using axes)

-- jAx: Joint axes integral to some peoples workflows: This can be accomplished through creating axes, then running relative motion.
 
-- CT Marker export: Exports xyz coordinates of CT markers (or any selected object for that matter)

-- vAvg: Calculates average position of a selection of verticies and puts a locator there (related to the above). Two options - fast and accurate (should be more or less the same in most cases)

-- Export data.  Export translation/rotation data from objects, included _data objects created via oRel.


## No plans to implement:

-- PSDR: pan/scan for looking through xcams.  Blender handles cameras differently and you can do this natively without the need for PSDR.

-- PStrn: Shader related - can be easily handled manually in blender.  

-- JCS: Joint coordinate system, not sure I've ever used this, having always used jAx.
