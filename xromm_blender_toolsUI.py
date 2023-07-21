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
        
        layout.operator("scene.create_xcam")


###########################################################
#IMPORT TRANSFORMATION UI CODE
###########################################################

# Define a panel class
class ImportPanel(bpy.types.Panel):
    bl_label = "Import"
    bl_idname = "VIEW3D_PT_import"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XROMM"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text = "not yet implemented")



###########################################################
#Register/Unregister Classes (may need changing for addon)
###########################################################

# Register the classes
classes = (CreateXCamOperator, XCamPanel, ImportPanel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
