###############################
# Script to export XYZ translations of markers in Blender XROMM toolkit
# Written By Peter FAlkingham July 2023
###############################



import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
import os

def write_marker_data(context, filepath):
    f = open(filepath, 'w', encoding='utf-8')
    # write the header row
    #for obj in selected objects,
    for obj in bpy.context.selected_objects[:-1]:
        f.write(obj.name+"_x, ")
        f.write(obj.name+"_y, ")
        f.write(obj.name+"_z, ")
    #write the last object without a comma
    f.write(bpy.context.selected_objects[-1].name+"_x, ")
    f.write(bpy.context.selected_objects[-1].name+"_y, ")
    f.write(bpy.context.selected_objects[-1].name+"_z")
    f.write("\n")
    for obj in bpy.context.selected_objects[:-1]:
        f.write(str(obj.location.x)+", ")
        f.write(str(obj.location.y)+", ")
        f.write(str(obj.location.z)+", ")
    #write the last object without a comma
    f.write(str(bpy.context.selected_objects[-1].location.x)+", ")
    f.write(str(bpy.context.selected_objects[-1].location.y)+", ")
    f.write(str(bpy.context.selected_objects[-1].location.z))
    f.write("\n")

    return {'FINISHED'}

###########################
# The below invokes the file picker and passes the file name to the function.
# I reused this from my ArchBooMaker scripts: https://github.com/pfalkingham/ArchBooBlender/blob/main/exportValues.py
###########################

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
class ExportMarkerData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_data.marker_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Marker Location Data"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return write_marker_data(context, self.filepath)
    
# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(ExportMarkerData)



def unregister():
    bpy.utils.unregister_class(ExportMarkerData)
  

if __name__ == "__main__":
    register()
    
        # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
