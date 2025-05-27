#########################################
# XROMM Toolkit for Blender, initialization file
# Written by Peter Falkingham, July 2023.
#########################################


bl_info = {
    "name": "XROMM toolkit for Blender",
    "description": "XROMM toolkit modified for Blender",
    "author": "Peter Falkingham",
    "version": (0, 9, 3),
    "blender": (3, 6, 0),
    "location": "",
}



import bpy
from . import xrommUI
from . import createAxes
from . import oRel
from . import xCamBlender
from . import xrommimport
from . import vAvg
from . import ctExp
from . import ExportXROMMData
from . import transrotimport

classes = (
    xrommUI.CreateXCamOperator,
    xrommUI.XCamPanel,
    xrommUI.ImportPanel,
    xrommUI.markersPanel,
    xrommUI.axesPanel,
    xrommUI.exportPanel,
    xrommUI.CreateAxesWOOperator,
    xrommUI.CreateAxesWOperator,
    xrommUI.CalculateRelativeMotionOperator,
    xrommUI.ImportOperator,
    xrommUI.ImportTransRotOperator,
    xrommUI.vAVGOperator,
    xrommUI.ctExOperator,
    xrommUI.xrommExportOperator,
    ctExp.ExportMarkerData,
    ExportXROMMData.ExpXROMMData,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()