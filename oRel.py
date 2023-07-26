#oRel   

import bpy
from mathutils import Matrix


#######
#hardcded values
#######
axis_object = bpy.data.objects["myaxis"]
proximal_object = bpy.data.objects["Cranium"]
distal_object = bpy.data.objects["LowerJaw"]

bpy.ops.object.select_all(action='DESELECT')
axis_object.select_set(True)
#apply any constraints on axis_object
bpy.ops.object.visual_transform_apply()
#Clear all constraints on axis_object
bpy.context.view_layer.objects.active = axis_object
bpy.ops.object.constraints_clear() 

#delete the two locators that share the same name as axis_object plus either _posz or _negz
for obj in bpy.data.objects:
    if obj.name == axis_object.name + "_posZ" or obj.name == axis_object.name + "_negZ":
        bpy.data.objects.remove(obj, do_unlink=True)

#duplicate axis_object and rename it to axis_object.name + "Prox"
bpy.ops.object.select_all(action='DESELECT')
axis_object.select_set(True)
bpy.ops.object.duplicate_move()
bpy.context.object.name = axis_object.name + "Prox"
axis_object_prox = bpy.data.objects[axis_object.name + "Prox"]

#parent axis_object_prox to proximal object
bpy.ops.object.select_all(action='DESELECT')
axis_object_prox.select_set(True)
proximal_object.select_set(True)
bpy.context.view_layer.objects.active = proximal_object
bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

#parent axis_object to distal_object
bpy.ops.object.select_all(action='DESELECT')
axis_object.select_set(True)
distal_object.select_set(True)
bpy.context.view_layer.objects.active = distal_object
bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)


#Now create an empty we can store relative position and rotation values in
# Create a new empty object
arrows_object = bpy.data.objects.new("Arrows", None)

# Add the empty object to the scene
bpy.context.collection.objects.link(arrows_object)

#calculate relative translation and rotation over the timeline, and store it in the empty
# Iterate over the frames in the timeline
for frame in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
    # Set the current frame
    bpy.context.scene.frame_set(frame)

    # Get the relative transform between the two axes
    rel_transform = axis_object_prox.matrix_world.inverted() @ axis_object.matrix_world

    # Extract the relative rotation and translation from the relative transform
    rel_rotation = rel_transform.to_euler()
    rel_translation = rel_transform.to_translation()

    # Set the rotation and translation of the arrows object
    arrows_object.rotation_mode = 'XYZ'
    arrows_object.rotation_euler = rel_rotation
    arrows_object.location = rel_translation

    # Insert a keyframe for the arrows object
    arrows_object.keyframe_insert(data_path='location', frame=frame)
    arrows_object.keyframe_insert(data_path='rotation_euler', frame=frame)
