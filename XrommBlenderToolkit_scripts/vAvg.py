#############################
#vAvg adapted from the Maya Mel scripts
#Takes selected object, and optionally separates it into multiple objects
#the creates an empty locator at the centre of each object
#Options for vertex average (as in Maya scripts, slow) or new bounding box average (faster)
#Written by Peter Falkingham, July 2023.
#Original Maya Mel scripts by Dave Baier
#############################

import bpy
from mathutils import Vector

def vertAvg(isSlow, isSeparate):

    #uses currently selected object

    if(isSeparate):
        bpy.ops.mesh.separate(type='LOOSE')

    #for loop through selected objects
    for obj in bpy.context.selected_objects:
        
        #set next obj as active object
        bpy.context.view_layer.objects.active = obj
        
        ################################
        #Slower, vertex based version, as in Maya - averages location of all verticies
        ################################
        if isSlow:
            # Get the object's vertices:
            verts = obj.data.vertices
            # Transform the vertex coordinates into world space:
            world_verts = [obj.matrix_world @ Vector(v.co) for v in verts]
            # Calculate the object's centre by averaging the vertex locations:
            obj_center = sum(world_verts, Vector()) / len(verts)
        
        ################################
        #Faster version, uses object bounding box
        ################################
        else:
            # Get the object's bounding box in world space:
            bbox = [obj.matrix_world @ Vector(b) for b in obj.bound_box]
            # Calculate the object's centre:
            obj_center = sum((Vector(b) for b in bbox), Vector()) / 8
        
        # Create an empty axes at the object's centre:
        empty = bpy.ops.object.empty_add(type='PLAIN_AXES', location=obj_center)
        # Get the newly created object from the selected objects collection:
        empty = bpy.context.selected_objects[-1]
        empty.name = "m_"+obj.name
