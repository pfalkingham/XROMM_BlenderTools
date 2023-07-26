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
        ###########################################################
        # TODO: Add logic here
        ###########################################################
        self.report({'INFO'}, "Creating xCam")
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
    bl_label = "Import Data"
    bl_description = "Import data"

    def execute(self, context):
        ###########################################################
        # TODO: Add logic here
        ###########################################################
        self.report({'INFO'}, "importing csv")
        return {'FINISHED'}

# Define a panel class
class ImportPanel(bpy.types.Panel):
    bl_label = "import_file"
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
        layout.label(text = "To selected object or new sphere(s)")
        layout.operator("scene.importfile")


###########################################################
#MARKERS UI CODE
###########################################################

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

        layout.label(text = "not yet implemented:")
        layout.label(text = "vAvg")
        layout.label(text = "CTex")




###########################################################
#AXES AND ROTATIONS UI CODE
###########################################################


# Define a string property for the axisname input box
bpy.types.Scene.axis_input = bpy.props.StringProperty(
    name="Axis name",
    description="axis name",
    default="",
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
        axis_object = context.scene.axis_object
        proximal_object = context.scene.proximal_object
        distal_object = context.scene.distal_object
        
        # Call the oRel script with the selected objects as arguments
        # TODO: Add logic here
        self.report({'INFO'}, "Calculating relative motion")
        return {'FINISHED'}



###########################################################
#Export UI CODE
###########################################################

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
        layout.label(text = "not yet implemented:")
        layout.label(text = "Export selected object(s):")
        layout.label(text = "Translation | Rotation | Trans/Rot")





###########################################################
#Register/Unregister Classes (may need changing for addon)
###########################################################

# Register the classes
classes = (CreateXCamOperator, XCamPanel, ImportPanel, markersPanel, axesPanel, exportPanel,CreateAxesWOOperator,CreateAxesWOperator,CalculateRelativeMotionOperator,ImportOperator)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
