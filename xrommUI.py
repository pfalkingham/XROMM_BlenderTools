#######################
# UI code form XROMM toolkit for blender
# Written by Peter Falkingham




import bpy

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

    def execute(self, context):
        scene = context.scene
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

# Define an operator for creating an xCam
class ImportOperator(bpy.types.Operator):
    bl_idname = "scene.importfile"
    bl_label = "Import Data to selected object"
    bl_description = "Import data"

    def execute(self, context):
        ###########################################################
        # TODO: Add logic here
        from . import xrommimport
        xrommimport.importRBT(context.scene.importfile)
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

        layout.label(text="Select CSV File:")
        layout.prop(scene, "importfile", text="CSV")
        layout.operator("scene.importfile")
        layout.label(text = "(ToDo: to selected object or new sphere(s))")  #maybe we'll make this as simple as 'if no object selected, create a sphere


###########################################################
#MARKERS UI CODE
###########################################################

# Define a boolean property for the checkbox
bpy.types.Scene.isSeparate = bpy.props.BoolProperty(
    name="Separate object?",
    description="Do you wish to separate the object into peices, and make a locator for each?",
    default=False
)
bpy.types.Scene.isSlow = bpy.props.BoolProperty(
    name="Slow or Fast",
    description="Slow - vertex based, Fast - bounding box based",
    default=False
)

# Define an operator for calling vavg
class vAVGOperator(bpy.types.Operator):
    bl_idname = "scene.vavg"
    bl_label = "Calculate marker positions"
    bl_description = "Calculate marker positions"

    def execute(self, context):
        ###########################################################
        # TODO: Add logic here
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
        # TODO: Add logic here
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
        # Create a boolean variable called isSeparate
        layout.prop(scene, "isSeparate", text="Separate objects?")
        # Add a segmented control for "Fast" or "Accurate"
        row = layout.row(align=True)
        if scene.isSlow:
            row.prop(scene, "isSlow", toggle=True, text="Accurate", icon="RADIOBUT_ON")
            row.prop(scene, "isSlow", toggle=True, text="Fast", icon="RADIOBUT_OFF")
        else:
            row.prop(scene, "isSlow", toggle=True, text="Accurate", icon="RADIOBUT_OFF")
            row.prop(scene, "isSlow", toggle=True, text="Fast", icon="RADIOBUT_ON")
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

    def execute(self, context):
        ###########################################################
        # TODO: Add logic here
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

    def execute(self, context):
        ###########################################################
        # TODO: Add logic here
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
        # TODO: Add logic here
        from . import ExportXROMMData
        scene = context.scene
        bpy.ops.export_data.xromm_data('INVOKE_DEFAULT')
        ###########################################################
        self.report({'INFO'}, "exporting XROMM data")
        return {'FINISHED'}

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
           CreateAxesWOOperator,
           CreateAxesWOperator,
           CalculateRelativeMotionOperator,
           ImportOperator,
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
