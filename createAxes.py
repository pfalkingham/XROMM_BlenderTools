########################################
#Create axes with or without locators.
#Written by Peter Falkingham, July 2023
#Credit for original Maya Mel scripts on which this is based goes to: Dave Baier.
########################################


import bpy

def createNewAxes(axisname, locators, axisSize):


    #create the axes - 3 cylinders topped by three cones, merged into a single object.
    #These values come from the maya scripts:
    cylLen = axisSize*0.9
    coneLen = axisSize*0.1
    cylRad = axisSize*0.01
    coneRad = axisSize*0.02


    bpy.ops.mesh.primitive_cylinder_add(radius=cylRad, depth=cylLen)
    cylinderz = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(radius=cylRad, depth=cylLen, rotation=(1.5708,0,0))
    cylindery = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(radius=cylRad, depth=cylLen, rotation=(0,1.5708,0))
    cylinderx = bpy.context.active_object


    bpy.ops.mesh.primitive_cone_add(radius1=coneRad, depth=coneLen, location=(0,0,cylLen/2))
    conz = bpy.context.active_object
    bpy.ops.mesh.primitive_cone_add(radius1=coneRad, depth=coneLen, location=(0,cylLen/2,0),rotation=(-1.5708,0,0))
    cony = bpy.context.active_object
    bpy.ops.mesh.primitive_cone_add(radius1=coneRad, depth=coneLen, location=(cylLen/2, 0,0),rotation=(0,1.5708,0))
    conx = bpy.context.active_object

    #Create materials if they don't exist.
    mat_red = bpy.data.materials.get("Red")
    if mat_red is None:
        mat_red = bpy.data.materials.new(name="Red")
        mat_red.diffuse_color = (1, 0, 0, 1)
    mat_green = bpy.data.materials.get("Green")
    if mat_green is None:
        mat_green = bpy.data.materials.new(name="Green")
        mat_green.diffuse_color = (0, 1, 0, 1)
    mat_blue = bpy.data.materials.get("Blue")
    if mat_blue is None:
        mat_blue = bpy.data.materials.new(name="Blue")
        mat_blue.diffuse_color = (0, 0, 1, 1)

    # Set the material indices for the cylinders and cones
    cylinderx.data.materials.append(mat_red)
    conx.data.materials.append(mat_red)
    cylindery.data.materials.append(mat_green)
    cony.data.materials.append(mat_green)
    cylinderz.data.materials.append(mat_blue)
    conz.data.materials.append(mat_blue)


    # Select all the objects to be joined
    bpy.context.view_layer.objects.active = cylinderx
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.select_all(action='DESELECT')
    cylinderx.select_set(True)
    cylindery.select_set(True)
    cylinderz.select_set(True)
    conx.select_set(True)
    cony.select_set(True)
    conz.select_set(True)

    # Join the selected objects into a single object
    bpy.context.view_layer.objects.active = cylinderz
    bpy.ops.object.join()

    # Rename the joined object to axisname
    bpy.context.active_object.name = axisname

    if(locators==1):
        # Create two locators at +10 and -10 on the Z axis
        loc1 = bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(10, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.name = axisname+"_posZ"
        loc2 = bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(-10, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.name = axisname+"_negZ"

        # Point-constrain the axis object to both empties
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.data.objects[axisname]
        bpy.data.objects[axisname].select_set(True)

        bpy.ops.object.constraint_add(type='COPY_LOCATION')
        constraint1 = bpy.data.objects[axisname].constraints[-1]
        constraint1.target = bpy.data.objects[axisname+"_posZ"]

        bpy.ops.object.constraint_add(type='COPY_LOCATION')
        constraint2 = bpy.data.objects[axisname].constraints[-1]
        constraint2.target = bpy.data.objects[axisname+"_negZ"]
        constraint2.influence=0.5

        bpy.ops.object.constraint_add(type='DAMPED_TRACK')
        constraint3 = bpy.data.objects[axisname].constraints[-1]
        constraint3.target = bpy.data.objects[axisname+"_posZ"]
        constraint3.track_axis='TRACK_Z'
        
        
            