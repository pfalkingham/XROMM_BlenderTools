########################################
#Import Xcam data, setup  a camera and an image plane, assign image/image sequence/movie to that plane
#Written by Peter Falkingham, July 2023
#Credit for original Maya Mel scripts on which this is based goes to: Dave Baier.
########################################

import bpy
import math
import numpy as np
import mathutils
import os
import glob
import re

def importXCam(mayacamfile, camName, image_path, is_image_sequence):
    
    file = open(mayacamfile, "r") 
    content = file.read() 
    file.close()

    #set cursor to origin to avoid wierdness:
    bpy.context.scene.cursor.location = (0,0,0)

    #split the file by lines and commas
    lines = content.split("\n") 
    image_size = np.array(lines[1].split(","))
    camera_matrix = np.array([lines[4].split(","), lines[5].split(","), lines[6].split(",")])
    rotation_matrix = np.array([lines[9].split(","), lines[10].split(","), lines[11].split(",")])
    translation_matrix = np.array([lines[14], lines[15], lines[16]])

    image_size=image_size.astype(int)
    camera_matrix = camera_matrix.astype(float)
    rotation_matrix = rotation_matrix.astype(float)
    translation_matrix = translation_matrix.astype(float)

    #create a new camera object and name it "Camera"
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = camName   

    #A lot of stuff here carried over from the original maya scripts

    ###########################################
    #get +set rotations and translations for camera
    ###########################################

    inverse_rotation_matrix4 = mathutils.Matrix.Identity(4)

    for i in range(3):
        for j in range(3):
            inverse_rotation_matrix4[i][j] = -1* rotation_matrix[j][i]

    inverse_translation_vector = np.array(-translation_matrix)

    # Multiply the inverse translation vector by the rotation matrix.
    inverse_translation_rotation_vector = inverse_translation_vector @ rotation_matrix

    for i in range(3):
        inverse_rotation_matrix4[i][3] = inverse_translation_rotation_vector[i]
    inverse_rotation_matrix4[3][3] = 1

    m = np.transpose(inverse_rotation_matrix4)

    m[0] = -m[0]

    camera.matrix_world = m

    ###############################
    #Lock Camera location/rotation
    ###############################

    camera.lock_location = (True, True, True)
    camera.lock_rotation = (True, True, True)
    camera.lock_scale = (True, True, True)


    ###################################
    #Now set focal length + resolution?
    ###################################

    #Not vital


    ####################################
    #set some parameters for image plane
    ####################################

    u0 = camera_matrix[0][2]
    v0 = camera_matrix[1][2]
    flx = camera_matrix[0][0]
    fly = camera_matrix[1][1]
    imx = image_size[0]
    imy = image_size[1]

    ########################
    #Add image plane
    ########################

    bpy.ops.mesh.primitive_plane_add(size=imx)
    xplane = bpy.context.object
    xplane.name = camName+"_plane"   
    xplane.scale[1] = imx/imy
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)



    # Move the plane to the camera's location
    xplane.location = camera.location


    #move the plane relative to it's pivot
    #I DON'T KNOW WHY, BUT THE MAYA SCRIPTS DO THIS, AND IT'S NECESSARY FOR PROPER ALIGNMENT
    # Enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')
    # Move the selected vertices
    bpy.ops.transform.translate(value=(-((u0+0.5)-(imx/2)), -(((imy/2)-(v0+0.5))), 0))
    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')


    # Add a Copy Rotation constraint to the plane object
    bpy.ops.object.constraint_add(type='COPY_ROTATION')
    bpy.context.object.constraints["Copy Rotation"].target = camera
    bpy.ops.constraint.apply(constraint="Copy Rotation")

    # Add a Limit Location constraint to the plane object
    constraint = xplane.constraints.new(type='LIMIT_LOCATION')
    constraint.use_min_x = True
    constraint.use_max_x = True
    constraint.use_min_y = True
    constraint.use_max_y = True
    constraint.owner_space = 'CUSTOM'
    constraint.space_object = bpy.data.objects[camera.name]


    # Set the constraint limits to zero
    constraint.min_x = 0.0
    constraint.max_x = 0.0
    constraint.min_y = 0.0
    constraint.max_y = 0.0

    # Move the plane back along its local Z axis
    initDist = np.linalg.norm(translation_matrix)
    print(initDist)
    bpy.ops.transform.translate(value=(0, 0, -initDist*1.3), orient_type='LOCAL')


    #Scale the plane with expressions
    # Add a driver to the plane's X Scale property
    driver = xplane.driver_add('scale',0).driver
    driver.type = 'SCRIPTED'

    # Add a variable to the driver to reference the camera object
    var = driver.variables.new()
    var.name = 'plane_cam_dist'
    var.type = 'LOC_DIFF'
    var.targets[0].id = xplane
    var.targets[1].id = camera

    # Set the driver expression
    driver.expression = f"(plane_cam_dist/{flx})"

    # Add a driver to the plane's Y Scale property
    driver = xplane.driver_add('scale',1).driver
    driver.type = 'SCRIPTED'

    # Add a variable to the driver to reference the camera object
    var = driver.variables.new()
    var.name = 'plane_cam_dist'
    var.type = 'LOC_DIFF'
    var.targets[0].id = xplane
    var.targets[1].id = camera

    # Set the driver expression
    driver.expression = f"(plane_cam_dist/{fly})"


    #Add custom property so you can see the SID
    xplane['SID'] = 0.0

    # Add a driver to the plane's X Scale property
    driver = xplane.driver_add('["SID"]').driver
    driver.type = 'SCRIPTED'

    # Add a variable to the driver to reference the camera object
    var = driver.variables.new()
    var.name = 'plane_cam_dist'
    var.type = 'LOC_DIFF'
    var.targets[0].id = xplane
    var.targets[1].id = camera

    # Set the driver expression
    driver.expression = "plane_cam_dist"




    ########################
    #add image or sequence to plane
    ########################

    # Create a new material
    material = bpy.data.materials.new(name=camName+"material")

    # Enable 'Use Nodes'
    material.use_nodes = True

    # Get the material's node tree
    node_tree = material.node_tree

    # Clear all nodes
    node_tree.nodes.clear()

    # Create an Image Texture node
    image_node = node_tree.nodes.new(type='ShaderNodeTexImage')

    # Check if the file is an image sequence or movie file
    if is_image_sequence:
        # Check if the file is a movie file
        if os.path.splitext(image_path)[1].lower() in {'.mp4', '.avi', '.mov'}:
            # Set the node type to 'ShaderNodeTexMovie'
            image_node = node_tree.nodes.new(type='ShaderNodeTexMovie')
            
            # Load the movie file
            image_node.movie = bpy.data.movieclips.load(image_path)
            
            # Set the frame duration
            image_node.frame_duration = image_node.movie.frame_duration
            
        else:
            # Load the image sequence
            image_node.image = bpy.data.images.load(image_path)
            
            # Set the source to 'SEQUENCE'
            image_node.image.source = 'SEQUENCE'
            
            # Set the frame duration
            file_name = os.path.basename(image_path)
            file_name = re.sub(r'\d+', '*', file_name)
            image_path = os.path.join(os.path.dirname(image_path), file_name)
            files = glob.glob(image_path)
            num_frames = len(files)
            image_node.image_user.frame_duration = num_frames
        
        # Enable auto-refresh for the image sequence or movie file
        image_node.image_user.use_auto_refresh = True
            
    else:
        # Load the single image
        image_node.image = bpy.data.images.load(image_path)

    # Create a Diffuse BSDF node
    diffuse_node = node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')

    # Create an Output node
    output_node = node_tree.nodes.new(type='ShaderNodeOutputMaterial')

    # Link the nodes together
    node_tree.links.new(image_node.outputs['Color'], diffuse_node.inputs['Color'])
    node_tree.links.new(diffuse_node.outputs['BSDF'], output_node.inputs['Surface'])

    # Assign the material to xplane
    xplane.active_material = material