#########################################
# XROMM Toolkit for Blender, initialization file
# Written by Peter Falkingham, July 2023.
#########################################

import os
import tomllib


def get_extension_manifest():
    """Reads extension metadata from blender_manifest.toml"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(dir_path, "blender_manifest.toml")
    try:
        with open(manifest_path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        print(f"XROMM Toolkit: Failed to read manifest: {e}")
        return {}


_manifest = get_extension_manifest()
__version__ = _manifest.get("version", "0.0.0")
__extension_name__ = _manifest.get("name", "XROMM Toolkit")
__author__ = _manifest.get("maintainer", "")



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
from . import jcsRel
from .xrommUI import XROMMBoneMapItem, XROMMMultiBoneImportOperator

classes = (
    xrommUI.CreateXCamOperator,
    xrommUI.XCamPanel,
    xrommUI.ImportPanel,
    xrommUI.markersPanel,
    xrommUI.axesPanel,
    xrommUI.exportPanel,
    xrommUI.AboutPanel,
    xrommUI.CreateAxesWOOperator,
    xrommUI.CreateAxesWOperator,
    xrommUI.CalculateRelativeMotionOperator,
    xrommUI.CalculateJCSRelativeMotionOperator,
    xrommUI.ImportOperator,
    xrommUI.ImportTransRotOperator,
    xrommUI.vAVGOperator,
    xrommUI.ctExOperator,
    xrommUI.xrommExportOperator,
    ctExp.ExportMarkerData,
    ExportXROMMData.ExpXROMMData,
    XROMMBoneMapItem,
    XROMMMultiBoneImportOperator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Dynamic props for multi-bone import
    from bpy.props import CollectionProperty, StringProperty
    if not hasattr(bpy.types.WindowManager, 'xromm_bone_map'):
        bpy.types.WindowManager.xromm_bone_map = CollectionProperty(type=classes[-2])  # XROMMBoneMapItem
    if not hasattr(bpy.types.WindowManager, 'xromm_multi_import_file'):
        bpy.types.WindowManager.xromm_multi_import_file = StringProperty()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    if hasattr(bpy.types.WindowManager, 'xromm_bone_map'):
        del bpy.types.WindowManager.xromm_bone_map
    if hasattr(bpy.types.WindowManager, 'xromm_multi_import_file'):
        del bpy.types.WindowManager.xromm_multi_import_file

if __name__ == "__main__":
    register()