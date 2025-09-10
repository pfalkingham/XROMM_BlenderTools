########################################
#import rigid body transformation matrix and apply to selected object
#Written by Peter Falkingham, July 2023
#Credit for original Maya Mel scripts on which this is based goes to: Dave Baier.
########################################



import bpy
import csv
import numpy as np
from mathutils import Matrix, Vector

#file name: hardcoded for now
#importCSV = "C:\\Users\\pfalk\\OneDrive\\WORK\\CurrentWork\\MyBlenderStuff\\XROMM ToolKit for Blender\\Sample Data\\RigidBody001_Upper_transformation.csv"



def importRBT(importCSV, object_mapping=None):
    """
    Imports rigid body transformation data from a CSV file and applies it to Blender objects.

    Args:
        importCSV (str): Path to the CSV file.
        object_mapping (dict, optional): A dictionary mapping object names from the CSV header
                                         to object names in the Blender scene.
                                         e.g., {'cranium': 'Suzanne', 'jaw': 'Cube'}.
                                         If None, attempts to import to the selected object.
    """
    
    # --- 1. Analyze CSV structure ---
    try:
        with open(importCSV, newline='') as csvfile:
            # Read the first line to determine structure
            first_row_str = csvfile.readline()
            if not first_row_str:
                print("Error: CSV file is empty.")
                return

            # Check for header by trying to convert first value to a number
            try:
                float(first_row_str.split(',')[0])
                has_header = False
            except ValueError:
                has_header = True

            # Reset and read properly with a csv.reader
            csvfile.seek(0)
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            header = next(reader)
            
            if not has_header:
                # If no header, the 'header' we just read is actually the first data row.
                # We need to put it back to be processed.
                # We'll also generate a placeholder header.
                num_cols = len(header)
                header = [f'col_{i}' for i in range(num_cols)]
                csvfile.seek(0) # Reset again to read all data rows
            
            # Check for frame column from the (real or generated) header
            has_frame_col = header[0].lower() == 'frame'
            
            # Determine number of objects
            data_cols = len(header) - (1 if has_frame_col else 0)
            if data_cols % 16 != 0:
                print(f"Error: CSV file has an incorrect number of data columns ({data_cols}). Should be a multiple of 16.")
                # Here you might want to raise an exception to be caught by the UI
                return
            
            num_objects = data_cols // 16
            
            # Extract / create object (bone) names
            file_object_names = []
            for i in range(num_objects):
                col_index = (i * 16) + (1 if has_frame_col else 0)
                base_name = header[col_index].split('_')[0]
                file_object_names.append(base_name)

            # If there was no header the base_name will repeat (e.g. 'col') – replace with bone1, bone2, ...
            if not has_header:
                file_object_names = [f"bone{i+1}" for i in range(num_objects)]

            # --- 2. Finalize Object Mapping ---
            if object_mapping is None:
                if num_objects == 1:
                    if bpy.context.selected_objects:
                        selected_obj = bpy.context.selected_objects[0]
                        object_mapping = {file_object_names[0]: selected_obj.name}
                    else:
                        print("Error: Please select an object to import the data to.")
                        return
                else:
                    # Multi-object file with no mapping supplied (should be created via UI before calling this).
                    print(f"Info: Multi-object file detected ({', '.join(file_object_names)}). Provide an object_mapping.")
                    return
            
            # --- 3. Read and Apply Data ---
            data_rows = list(reader)

    except FileNotFoundError:
        print(f"Error: File not found at {importCSV}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # --- 4. Apply Transformations to Objects ---
    for i, row in enumerate(data_rows):
        if not row: continue # Skip empty rows

        frame_number = 0
        data_offset = 0
        if has_frame_col:
            frame_number = int(float(row[0]))
            data_offset = 1
        else:
            frame_number = i + 1 # Fallback to sequential frames

        for obj_idx, file_obj_name in enumerate(file_object_names):
            blender_obj_name = object_mapping.get(file_obj_name)
            if not blender_obj_name:
                continue

            blender_obj = bpy.data.objects.get(blender_obj_name)
            if not blender_obj:
                continue

            start_col = data_offset + (obj_idx * 16)
            end_col = start_col + 16
            
            try:
                matrix_elements = [float(x) for x in row[start_col:end_col]]
            except (ValueError, IndexError):
                # Skip row if data is malformed or missing
                continue

            matrix = Matrix((
                matrix_elements[0:4],
                matrix_elements[4:8],
                matrix_elements[8:12],
                matrix_elements[12:16]
            ))
            
            matrix.transpose()

            if not np.isnan(matrix).any():
                blender_obj.matrix_world = matrix
                blender_obj.keyframe_insert(data_path='location', frame=frame_number)
                blender_obj.keyframe_insert(data_path='rotation_euler', frame=frame_number)
                blender_obj.keyframe_insert(data_path='scale', frame=frame_number)