#######################
# UI code for XROMM toolkit for blender
# Written by Peter Falkingham July/August 2023
#######################

import bpy
import sys
import os
from bpy.props import StringProperty, PointerProperty, CollectionProperty
from bpy.types import PropertyGroup


###########################################################
#XCAM UI CODE
###########################################################
# Define a file picker property
bpy.types.Scene.maya_cam_file = bpy.props.StringProperty(
    name="",
    description="Select a MayaCam file",
    default="",
    maxlen=1024,
    subtype='FILE_PATH'
)

# Define a directory picker property
bpy.types.Scene.images_file = bpy.props.StringProperty(
    name="",
    description="Select an image or movie (or leave blank)",
    default="",
    maxlen=1024,
    subtype='FILE_PATH'   ###Actually, I may want to make this a single file.
)

# Define a boolean property for the checkbox
bpy.types.Scene.image_sequence = bpy.props.BoolProperty(
    name="Image Sequence?",
    description="Check if using an image sequence",
    default=False
)

# Define a string property for the cameraname input box
bpy.types.Scene.text_input = bpy.props.StringProperty(
    name="Camera name",
    description="xCam name",
    default="xCam",
    maxlen=1024
)

# Define an operator for creating an xCam
class CreateXCamOperator(bpy.types.Operator):
    bl_idname = "scene.create_xcam"
    bl_label = "Create XCam"
    bl_description = "Create xCam from file+images"
    bl_options = {'UNDO'}

    def execute(self, context):
        scene = context.scene
        if not scene.maya_cam_file or not os.path.isfile(scene.maya_cam_file):
            self.report({'ERROR'}, "Please select a valid MayaCam file.")
            return {'CANCELLED'}

        if scene.images_file.strip() and not os.path.isfile(scene.images_file):
            self.report({'ERROR'}, "Image/movie path is invalid. Leave blank if you do not want an image plane texture.")
            return {'CANCELLED'}

        from . import xCamBlender
        xCamBlender.importXCam(scene.maya_cam_file, scene.text_input, scene.images_file, scene.image_sequence)
        self.report({'INFO'}, "Creating xCam2")
        return {'FINISHED'}

# Define a panel class
class XCamPanel(bpy.types.Panel):
    bl_label = "XCam"
    bl_idname = "VIEW3D_PT_xcam"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XROMM"    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Select MayaCam (v2) File:")
        layout.prop(scene, "maya_cam_file")

        layout.label(text="Select an image or movie (or leave blank):")
        layout.prop(scene, "images_file")
        
        # Add the checkbox to the layout
        layout.prop(scene, "image_sequence")
        
        # Add the text input box to the layout
        row = layout.row()
        row.label(text="Camera name:")
        col = row.column()
        col.prop(scene, "text_input", text="")

        
        layout.operator("scene.create_xcam")


###########################################################
#IMPORT TRANSFORMATION UI CODE
###########################################################

# Define a file picker property
bpy.types.Scene.importfile = bpy.props.StringProperty(
    name="",
    description="Select a CSV file",
    default="",
    maxlen=1024,
    subtype='FILE_PATH'
)

# Define a boolean property for the checkboxes
bpy.types.Scene.isTranslationImp = bpy.props.BoolProperty(
    name="import Translations",
    description="include translations in exported data",
    default=True
)
bpy.types.Scene.isRotationImp = bpy.props.BoolProperty(
    name="import Rotations",
    description="include rotations in exported data",
    default=False
)

#new object or selected
bpy.types.Scene.new_or_selected = bpy.props.EnumProperty (
    items=[
        ('NEW', 'New Sphere(s)', ''),
        ('SELECTED', 'Selected object', '')
    ],
    default='NEW'
)

# Define an operator for creating an xCam
class ImportOperator(bpy.types.Operator):
    bl_idname = "scene.importfile"
    bl_label = "Import Rigid Body Data to selected object"
    bl_description = "Import data"
    bl_options = {'UNDO'}

    def execute(self, context):
        import csv
        from . import xrommimport

        filepath = context.scene.importfile
        if not filepath:
            self.report({'ERROR'}, "No file selected.")
            return {'CANCELLED'}

    # --- Analyze the CSV to decide on the import path ---
        try:
            with open(filepath, newline='') as csvfile:
                first_row_str = csvfile.readline()
                if not first_row_str:
                    self.report({'ERROR'}, "CSV file is empty.")
                    return {'CANCELLED'}

                try:
                    float(first_row_str.split(',')[0])
                    has_header = False
                except ValueError:
                    has_header = True

                csvfile.seek(0)
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                header = next(reader) if has_header else [f'col_{i}' for i in range(len(first_row_str.split(',')))]

                # Check if there's a frame column based on total column count
                total_cols = len(header)
                if total_cols % 16 == 1:
                    has_frame_col = True
                    data_cols = total_cols - 1
                elif total_cols % 16 == 0:
                    has_frame_col = False
                    data_cols = total_cols
                else:
                    self.report({'ERROR'}, f"Incorrect number of data columns. Expected multiple of 16 or 16n+1, got {total_cols}.")
                    return {'CANCELLED'}
                    
                num_objects = data_cols // 16

                # Build object (bone) names
                file_object_names = []
                if has_header:
                    # reset reader to get full header again
                    csvfile.seek(0)
                    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    header_row = next(reader)
                    for i in range(num_objects):
                        idx = (i * 16) + (1 if has_frame_col else 0)
                        base_name = header_row[idx].split('_')[0]
                        file_object_names.append(base_name)
                else:
                    file_object_names = [f"bone{i+1}" for i in range(num_objects)]

        except Exception as e:
            self.report({'ERROR'}, f"File analysis failed: {e}")
            return {'CANCELLED'}

        # --- Decide on single vs. multi-object import ---
        if num_objects > 1:
            # Store temporary data on the window manager to be used by the popup operator
            wm = context.window_manager
            wm.xromm_multi_import_file = filepath
            collection = wm.xromm_bone_map
            collection.clear()
            for name in file_object_names:
                item = collection.add()
                item.bone_name = name
                item.object_ref = None
            # invoke popup
            bpy.ops.scene.xromm_multi_bone_map('INVOKE_DEFAULT')
        else:
            xrommimport.importRBT(filepath)

        return {'FINISHED'}

#############################
# Multi-bone mapping support
#############################

class XROMMBoneMapItem(PropertyGroup):
    bone_name: StringProperty(name="Bone")
    object_ref: PointerProperty(type=bpy.types.Object, name="Object")

class XROMMMultiBoneImportOperator(bpy.types.Operator):
    bl_idname = "scene.xromm_multi_bone_map"
    bl_label = "Map Bones to Objects"
    bl_description = "Assign scene objects to imported bones"
    bl_options = {'UNDO'}

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        layout.label(text="Assign each bone to a Blender object:")
        col = layout.column()
        for item in wm.xromm_bone_map:
            row = col.row(align=True)
            row.label(text=item.bone_name)
            row.prop(item, "object_ref", text="")

    def execute(self, context):
        from . import xrommimport
        wm = context.window_manager
        mapping = {}
        missing = []
        for item in wm.xromm_bone_map:
            if item.object_ref:
                mapping[item.bone_name] = item.object_ref.name
            else:
                missing.append(item.bone_name)
        if missing:
            self.report({'ERROR'}, f"Unassigned bones: {', '.join(missing)}")
            return {'CANCELLED'}
        xrommimport.importRBT(wm.xromm_multi_import_file, mapping)
        self.report({'INFO'}, "Imported multi-bone rigid body data")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
    
# Define an operator for creating an xCam
class ImportTransRotOperator(bpy.types.Operator):
    bl_idname = "scene.importtrfile"
    bl_label = "Import translation/rotation data"
    bl_description = "Import translation and/or rotation data to selected object or new sphere(s)"
    bl_options = {'UNDO'}

    def execute(self, context):
        ###########################################################
        from . import transrotimport
        transrotimport.importTR(context.scene.importfile, context.scene.isTranslationImp, context.scene.isRotationImp, context.scene.new_or_selected)
        ###########################################################
        self.report({'INFO'}, "importing csv")
        return {'FINISHED'}

# Define a panel class
class ImportPanel(bpy.types.Panel):
    bl_label = "Import XYZ or motion data"
    bl_idname = "VIEW3D_PT_import"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XROMM"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "importfile", text="CSV")
        layout.separator()
        layout.label(text="Import Rigid Body transformations:")
        layout.operator("scene.importfile")
        layout.separator()
        layout.label(text = "Import Translations/Rotations:")
        #add checkboxes for translations and rotations
        row = layout.row()
        row.prop(scene, "isTranslationImp", text="Translation")
        row.prop(scene, "isRotationImp", text="Rotation")
        layout.prop (scene, "new_or_selected", expand=True)
        layout.operator("scene.importtrfile")


###########################################################
#MARKERS UI CODE
###########################################################

# Define a boolean property for the checkbox
bpy.types.Scene.isSeparate = bpy.props.BoolProperty(
    name="Separate object?",
    description="Do you wish to separate the object into peices, and make a locator for each?",
    default=False
)
bpy.types.Scene.isSlow = bpy.props.EnumProperty(
    items=[
        ('TRUE', 'Accurate', ''),
        ('FALSE', 'Fast', '')
    ],
    default='TRUE'
)

# Define an operator for calling vavg
class vAVGOperator(bpy.types.Operator):
    bl_idname = "scene.vavg"
    bl_label = "Calculate marker positions"
    bl_description = "Calculate marker positions"
    bl_options = {'UNDO'}

    def execute(self, context):
        ###########################################################
        from . import vAvg
        vAvg.vertAvg(context.scene.isSlow, context.scene.isSeparate)
        ###########################################################
        self.report({'INFO'}, "calculating markers")
        return {'FINISHED'}
    
# Define an operator for ctex
class ctExOperator(bpy.types.Operator):
    bl_idname = "scene.ctex"
    bl_label = "export marker positions"
    bl_description = "Export selected marker positions"

    def execute(self, context):
        ###########################################################
        from . import ctExp
        bpy.ops.export_data.marker_data('INVOKE_DEFAULT')
        ###########################################################
        self.report({'INFO'}, "exporting markers")
        return {'FINISHED'}

# Define a panel class
class markersPanel(bpy.types.Panel):
    bl_label = "Markers"
    bl_idname = "VIEW3D_PT_markers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XROMM"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text = "vAvg - Marker locations")
        # Add a segmented control for "Fast" or "Accurate"
        layout.prop (scene, "isSlow", expand=True)
        #need a button:
        layout.operator("scene.vavg", text="Calculate marker positions")
        layout.separator()
        layout.label(text = "CTexport")
        #just a button
        layout.operator("scene.ctex", text="Export marker positions")




###########################################################
#AXES AND ROTATIONS UI CODE
###########################################################


# Define a string property for the axisname input box
bpy.types.Scene.axis_input = bpy.props.StringProperty(
    name="Axis name",
    description="axis name",
    default="axis",
    maxlen=1024
)

#define pointers for the objects I'll pass to oRel
bpy.types.Scene.oRel_axes = bpy.props.PointerProperty(type=bpy.types.Object)
bpy.types.Scene.prox_obj = bpy.props.PointerProperty(type=bpy.types.Object)
bpy.types.Scene.dist_obj = bpy.props.PointerProperty(type=bpy.types.Object)

# Define an operator for creating a axes without locator
class CreateAxesWOOperator(bpy.types.Operator):
    bl_idname = "scene.create_axes_wo"
    bl_label = "Create Axes"
    bl_description = "Create Axes WITHOUT locators"
    bl_options = {'UNDO'}

    def execute(self, context):
        ###########################################################
        scene = context.scene
        from . import createAxes
        createAxes.createNewAxes(scene.axis_input, 0, 5) 
        ###########################################################
        self.report({'INFO'}, "Creating axes WITHOUT locators")
        return {'FINISHED'}

# Define an operator for creating a axes WITH locators
class CreateAxesWOperator(bpy.types.Operator):
    bl_idname = "scene.create_axes_with"
    bl_label = "Create Axes with locators"
    bl_description = "Create Axes with locators"
    bl_options = {'UNDO'}

    def execute(self, context):
        ###########################################################
        scene = context.scene
        from . import createAxes
        createAxes.createNewAxes(scene.axis_input, 1, 5)  #hard coding a size of 5cm for now
        ###########################################################
        self.report({'INFO'}, "Creating axes with locators")
        return {'FINISHED'}



# Define a panel class
class axesPanel(bpy.types.Panel):
    bl_label = "Axes and Rel Motion"
    bl_idname = "VIEW3D_PT_axes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XROMM"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text = "Create Axes:")
        row = layout.row()
        row.label(text="Axis name:")
        col = row.column()
        col.prop(scene, "axis_input", text="")
        row = layout.row()
        row.operator("scene.create_axes_wo", text="Without locators")
        row.operator("scene.create_axes_with", text="With locators")
        
        layout.separator()
        
        layout.label(text = "Output relative Motion:")
        # Add two columns with object selectors
        layout.prop_search(scene, "oRel_axes", scene, "objects", text="Axes")
        layout.prop_search(scene, "prox_obj", scene, "objects", text="Proximal Object")
        layout.prop_search(scene, "dist_obj", scene, "objects", text="Distal Object")
        
        # Add a button to call the oRel script
        layout.separator()
        layout.operator("scene.calculate_relative_motion", text="Calculate relative motion")

# Define an operator for calculating relative motion
class CalculateRelativeMotionOperator(bpy.types.Operator):
    bl_idname = "scene.calculate_relative_motion"
    bl_label = "Calculate relative motion"
    bl_description = "Calculate relative motion"
    bl_options = {'UNDO'}

    def execute(self, context):
        # Get the selected objects from the object selectors
        axis_object = context.scene.oRel_axes
        proximal_object = context.scene.prox_obj
        distal_object = context.scene.dist_obj
        
        # Show a pop-up message with OK and Cancel buttons
        # saying that this will use the current frame as zero or 'neutral'

        from . import oRel
        oRel.calcRelMotion(axis_object, proximal_object, distal_object)

        return {'FINISHED'}



###########################################################
#Export UI CODE
###########################################################

# Define a boolean property for the checkbox
bpy.types.Scene.isAnimation = bpy.props.BoolProperty(
    name="Export Animated data ?",
    description="Do you wish to export animated data (full timeline)?",
    default=True
)
bpy.types.Scene.isTranslation = bpy.props.BoolProperty(
    name="Export Translations",
    description="include translations in exported data",
    default=True
)
bpy.types.Scene.isRotation = bpy.props.BoolProperty(
    name="Export Rotations",
    description="include rotations in exported data",
    default=True
)


# Define a panel class
class exportPanel(bpy.types.Panel):
    bl_label = "Export data"
    bl_idname = "VIEW3D_PT_exp"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XROMM"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text = "Export selected object(s):")
        layout.label(text = "Translation | Rotation | Trans/Rot")
        #three checkboxes for isnamation, istranslation, and isrotation
        row = layout.row()
        row.prop(scene, "isAnimation", text="Animation")
        row.prop(scene, "isTranslation", text="Translation")
        row.prop(scene, "isRotation", text="Rotation")
        #button to call the export script
        layout.operator("export.xromm_data", text="Export XROMM data")


# Define an operator for exporting XROMM data
class xrommExportOperator(bpy.types.Operator):
    bl_idname = "export.xromm_data"
    bl_label = "export XROMM data"
    bl_description = "Export trans/rot of selected objects"

    def execute(self, context):
        ###########################################################
        from . import ExportXROMMData
        scene = context.scene
        bpy.ops.export_data.xromm_data('INVOKE_DEFAULT')
        ###########################################################
        self.report({'INFO'}, "exporting XROMM data")
        return {'FINISHED'}

###########################################################
#ABOUT UI CODE
###########################################################

# Define a panel class
class AboutPanel(bpy.types.Panel):
    bl_label = "About"
    bl_idname = "VIEW3D_PT_about"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XROMM"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        
        # Get addon's bl_info
        # The __package__ is XrommBlenderToolkit_scripts, but the addon name is XROMM_BlenderTools
        # So we need to get the parent module's info.
        addon_name = __name__.split('.')[0]
        addon_module = sys.modules.get(addon_name)
        if addon_module:
            bl_info = getattr(addon_module, 'bl_info', {})
            
            name = bl_info.get("name", "")
            version = bl_info.get("version", (0,0,0))
            author = bl_info.get("author", "")

            if name:
                layout.label(text=name)
            if version:
                layout.label(text=f"Version: {'.'.join(map(str, version))}")
            if author:
                layout.label(text=f"Author: {author}")
        else:
            layout.label(text="Could not find addon information.")


###########################################################
#Register/Unregister Classes (may need changing for addon)
###########################################################

# Register the classes
classes = (CreateXCamOperator, 
           XCamPanel, 
           ImportPanel, 
           markersPanel, 
           axesPanel, 
           exportPanel,
           AboutPanel,
           CreateAxesWOOperator,
           CreateAxesWOperator,
           CalculateRelativeMotionOperator,
           ImportOperator,
           ImportTransRotOperator,
           vAVGOperator,
           ctExOperator,
           xrommExportOperator,
           )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
