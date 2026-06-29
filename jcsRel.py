########################################
# JCS relative motion between two ACS objects (ACSf and ACSm)
# Written by Peter Falkingham, June 2026
# Based on Grood & Suntay (1983) and Manafzadeh & Gatesy (2021)
########################################

import bpy
import math
from mathutils import Matrix, Vector


def calc_jcs_relative_motion(acsf_obj, acsm_obj, mode):
    rel_name = acsm_obj.name + "_Data"

    data_obj = bpy.data.objects.new(rel_name, None)
    data_obj.name = rel_name
    bpy.context.collection.objects.link(data_obj)
    data_obj.rotation_mode = 'XYZ'

    for frame in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
        bpy.context.scene.frame_set(frame)

        R = acsf_obj.matrix_world.inverted() @ acsm_obj.matrix_world
        m = R.to_3x3()
        v = R.to_translation()

        ad_ab = math.asin(max(-1.0, min(1.0, -m[2][0])))

        if abs(math.cos(ad_ab)) > 1e-8:
            fe = math.atan2(m[1][0], m[0][0])
            lar = math.atan2(m[2][1], m[2][2])
        else:
            fe = math.atan2(-m[0][1], m[1][1])
            lar = 0.0

        data_obj.rotation_euler = (round(lar, 6), round(ad_ab, 6), round(fe, 6))

        if mode == 'ISB':
            tx = v.dot(m.col[0])
            ty = v.dot(m.col[1])
            tz = v.dot(m.col[2])
        else:
            cos_fe = math.cos(fe)
            sin_fe = math.sin(fe)
            tx = v.x * cos_fe + v.y * sin_fe
            ty = -v.x * sin_fe + v.y * cos_fe
            tz = v.z

        data_obj.location = (round(tx, 6), round(ty, 6), round(tz, 6))

        data_obj.keyframe_insert(data_path='location', frame=frame)
        data_obj.keyframe_insert(data_path='rotation_euler', frame=frame)
