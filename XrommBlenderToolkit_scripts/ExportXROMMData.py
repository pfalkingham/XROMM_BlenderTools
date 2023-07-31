###############################################
# Script to export xyz translation/rotation over single or all frames.
# Written by Peter Falkingham July 2023
###############################################

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
import os
import math

#context is scene context
#filepath is null at this point (hopefully)
#animation is a boolean, TRUE = do all frames, FALSE just the current one.
#translation is a boolean, TRUE = export translations, FALSE = don't
#rotation is a boolean, TRUE = export rotations, FALSE = don't

def write_xromm_data(context, filepath):
    translation = context.scene.isTranslation
    rotation = context.scene.isRotation
    animation = context.scene.isAnimation
    
    f = open(filepath, 'w', encoding='utf-8')
    # write the header row
    #for obj in selected objects
    for obj in bpy.context.selected_objects:
        if(translation):
            f.write(obj.name+"_x, ")
            f.write(obj.name+"_y, ")
            f.write(obj.name+"_z, ")
        if(rotation):
            f.write(obj.name+"_rx, ")
            f.write(obj.name+"_ry, ")
            f.write(obj.name+"_rz, ")
    f.write("\n")    
    #now do the data:
    if(animation==False):
        for obj in bpy.context.selected_objects:
            if(translation):
                f.write(str(obj.location.x)+", ")
                f.write(str(obj.location.y)+", ")
                f.write(str(obj.location.z)+", ")
            if(rotation):
                f.write(str(math.degrees(obj.rotation_euler.x))+", ")
                f.write(str(math.degrees(obj.rotation_euler.y))+", ")
                f.write(str(math.degrees(obj.rotation_euler.z))+", ")
        f.write("\n")
    else:
        #get the current frame and assign to 'curFrame'
        curFrame = bpy.context.scene.frame_current
        #loop through the frames
        for frame in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end+1):
            bpy.context.scene.frame_set(frame)
            for obj in bpy.context.selected_objects:
                if(translation):
                    f.write(str(obj.location.x)+", ")
                    f.write(str(obj.location.y)+", ")
                    f.write(str(obj.location.z)+", ")
                if(rotation):
                    f.write(str(math.degrees(obj.rotation_euler.x))+", ")
                    f.write(str(math.degrees(obj.rotation_euler.y))+", ")
                    f.write(str(math.degrees(obj.rotation_euler.z))+", ")
            f.write("\n")
        #reset the frame to the original
        bpy.context.scene.frame_set(curFrame)
    f.close()

    #hack to clean up file - reopen in read/write and remove the ", " from the end of each line
    f = open(filepath, 'r+', encoding='utf-8')
    content = f.read()
    f.seek(0)
    f.truncate()
    f.write(content.replace(", \n", "\n"))
    f.close()

    return {'FINISHED'}

###########################
# The below invokes the file picker and passes the file name to the function.
# I reused this from my ArchBooMaker scripts: https://github.com/pfalkingham/ArchBooBlender/blob/main/exportValues.py
###########################

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
class ExpXROMMData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_data.xromm_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export XROMM Data"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return write_xromm_data(context, self.filepath)
    
# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(ExportXROMMData)



def unregister():
    bpy.utils.unregister_class(ExportXROMMData)
  

if __name__ == "__main__":
    register()
    
        # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
