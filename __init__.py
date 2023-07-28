bl_info = {
    "name": "XROMM toolkit for Blender",
    "description": "XROMM toolkit modified for Blender",
    "author": "falkingham",
    "version": (0, 1),
    "blender": (3, 6, 0),
    "location": "",
}



import bpy
from . import xrommUI
from . import createAxes
from . import oRel
from . import xCamBlender
from . import xrommimport

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
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()