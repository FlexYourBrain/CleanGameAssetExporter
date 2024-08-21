#######################################################################################
# MIT No Attribution
# Copyright 2024 Agustin R.

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#######################################################################################
""" CLEAN Operator class """

import bpy
import os
from .clean_script import export_to_file , orient_y
from bpy.types import (Operator)

class CleanExporter(Operator):
    ''' clean exporter - Export mesh buffer files '''
    bl_idname       = "clean.buffer_export"
    bl_label        = "Export"
    bl_description  = "Export Mesh Buffer"

    def execute(self, context):

        mytool = context.scene.my_tool
        bool_normal = mytool.bool_normal
        bool_tangent = mytool.bool_tangent
        bool_uv = mytool.bool_uv
        bool_color = mytool.bool_color
        bool_yup = mytool.bool_yup
        output_dir = os.path.realpath(bpy.path.abspath(mytool.output_dir))
        if not output_dir:
            raise Exception("No output directory(folderpath) defined! Please select a directory for exporting.")

        view_layer = bpy.context.view_layer
        obj_active = view_layer.objects.active
        selection = bpy.context.selected_objects
        tool_trans = bpy.context.scene.tool_settings.transform_pivot_point

        for obj in selection:
            if obj.type == "MESH":
                obj.select_set(True)
                view_layer.objects.active = obj
                name = bpy.path.clean_name(obj.name)
                fn = os.path.join(output_dir, name) + ".buffer"
                if bool_yup:
                    bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
                    orient_y(-1.5708)
                with open(fn, 'wb') as f:
                    export_to_file(f, obj, bool_normal, bool_tangent, bool_uv, bool_color)
                    print('File has been saved!',fn)
                if bool_yup:
                    orient_y(1.5708)
                    bpy.context.scene.tool_settings.transform_pivot_point = tool_trans
                obj.select_set(False)
        view_layer.objects.active = obj_active
        for obj in selection:
            obj.select_set(True)
        return {'FINISHED'}
