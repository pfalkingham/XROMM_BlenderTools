#######################################
# Script to import translations/rotations to new or selected objects
# Reads header line, then subsequent lines as frames, x,y,z,rx,ry,rz,
# Written by Peter Falkingham August 2023
#######################################

import bpy
import csv

def importTR(importCSV, doTrans, doRot, isNewObject):
    #check if the user actually selected translations and/or rotations
    if not doTrans and not doRot:
        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Neither translation nor rotation selected - nothing imported"), title="Warning", icon='ERROR')
        return {'CANCELLED'}

    # Determine the number of values per object based on doTrans and doRot
    if doTrans and doRot:
        valuesPerObject = 6
    else:
        valuesPerObject = 3

    # Open the CSV file
    with open(importCSV, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        #read header line
        header = next(reader)
        #read in the data
        data = list(reader)

    #need an error catch here - length of header should be greater than, and a multiple of valuesPerObject. e.g. if someone ticked both translation and rotation, but there is only translation data, there will only be three columns
    if len(header) < valuesPerObject or len(header) % valuesPerObject != 0:
        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Number of columns in file not correct"), title="Warning", icon='ERROR')
        return {'CANCELLED'}

    ##########################
    # IMPORTING TO NEW OBJECTS
    ##########################
    objects = {}
    if isNewObject == 'NEW':
        #for each object in the csv, create a new sphere, and import the data. The sphere will be named based on the header, so if the first column is called 'myObject1_x', the object should be 'myObject1'
        #loop through each object in the file
        for i in range(0, len(header), valuesPerObject):
            #create a new object
            bpy.ops.mesh.primitive_uv_sphere_add(radius = 0.5)
            #rename it based on the header
            name = header[i].rsplit('_',1)[0]
            #we need some error checking here, because if an object with that name already exists, it'll get .001 added to it, and we won't be able to find it later
            bpy.context.active_object.name = name
            objects[name] = bpy.context.active_object

        #loop through each frame
        for j in range(len(data)):
            #get the frame number
            frame_number = j+1
            #loop through each object in the file
            for i in range(0, len(header), valuesPerObject):
                #get the object name
                name = header[i].rsplit('_',1)[0]
                #get the object reference from the dictionary
                obj = objects[name]
                #get the x,y,z values
                if doTrans:
                    x = float(data[j][i])
                    y = float(data[j][i+1])
                    z = float(data[j][i+2])
                    #set the location
                    obj.location = (x,y,z)
                    #keyframe it if there are no NANs
                    if not (x == 'NAN' or y == 'NAN' or z == 'NAN'):
                        obj.keyframe_insert(data_path='location', frame=frame_number)
                #get the rotation values
                if doRot:
                    rx = float(data[j][i+3])
                    ry = float(data[j][i+4])
                    rz = float(data[j][i+5])
                    #set the rotation
                    obj.rotation_euler = (rx,ry,rz)
                    #keyframe it if there are no NANs
                    if not (rx == 'NAN' or ry == 'NAN' or rz == 'NAN'):
                        obj.keyframe_insert(data_path='rotation_euler', frame=frame_number)


####################################
# Apply to selected objects
# NOTE: I allow people to select more than 1 object, but as this is an edge case, I leave it to the user to make sure they have selected the objects in the same order as they appear in the file
####################################
    #if isNewObject is false, 
    if isNewObject == 'SELECTED':
        # Get the selected objects
        selected_objects = bpy.context.selected_objects
        #we need to check if the number of currently selected objects matches the number of objects in the file
        if len(selected_objects) != len(header) // valuesPerObject:
            bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Number of selected objects does not match number of objects in file"), title="Warning", icon='ERROR')
            return{'CANCELLED'}
         # Loop through each frame
        for j in range(len(data)):
            # Get the frame number
            frame_number = j+1
            # Loop through each object in the file
            for i in range(0, len(header), valuesPerObject):
                # Get the object index
                index = i // valuesPerObject
                # Get the object reference from the selected objects
                obj = selected_objects[index]
                # Get the x,y,z values
                if doTrans:
                    x = float(data[j][i])
                    y = float(data[j][i+1])
                    z = float(data[j][i+2])
                    # Set the location
                    obj.location = (x,y,z)
                    #keyframe it if there are no NANs
                    if not (x == 'NAN' or y == 'NAN' or z == 'NAN'):
                        obj.keyframe_insert(data_path='location', frame=frame_number)
                # Get the rotation values
                if doRot:
                    rx = float(data[j][i+3])
                    ry = float(data[j][i+4])
                    rz = float(data[j][i+5])
                    # Set the rotation
                    obj.rotation_euler = (rx,ry,rz)
                    #keyframe it if there are no NANs
                    if not (rx == 'NAN' or ry == 'NAN' or rz == 'NAN'):
                        obj.keyframe_insert(data_path='rotation_euler', frame=frame_number)