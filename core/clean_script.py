#######################################################################################
# MIT No Attribution

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
""" This module contains main functions for exporting """
""" CREDIT: Code reference defold_mesh.py - https://forum.defold.com/t/mesh-component/65137 """

import bpy
import json

from collections import OrderedDict
def make_stream(name, component_count, data, typ="float32"):
    return OrderedDict([('name', name),
                        ('type', typ),
                        ('count', component_count),
                        ('data', data)
                        ])

def orient_y(rot):
    # Rotate object and apply transform to match defolds right hand cartesian coordinate system
    bpy.ops.transform.rotate(value=rot, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)


def export_mesh(mesh, b_normal, b_tanget, b_uv, b_color):
    mesh.calc_loop_triangles()
    mesh.calc_tangents()
    mesh_loops = mesh.loops
    mesh_vertices = mesh.vertices
    mesh_uv_layers = mesh.uv_layers
    mesh_color_layers = mesh.vertex_colors

    bool_normal = b_normal
    bool_tangent = b_tanget
    bool_uv = b_uv
    bool_color = b_color

    position_values = []
    normal_values = []
    tangent_values = []
    uv_values_by_layer = [[]] * len(mesh_uv_layers)
    color_values_by_layer = [[]] * len(mesh_color_layers)

    for triangle in mesh.loop_triangles:
        use_smooth = triangle.use_smooth

        for triangle_vertex_index, mesh_vertex_index in enumerate(triangle.vertices):
            mesh_loop = mesh_loops[triangle.loops[triangle_vertex_index]]
            mesh_vertex = mesh_vertices[mesh_vertex_index]
            
            position = mesh_vertex.co.to_tuple()
            normal = (mesh_vertex.normal if use_smooth else triangle.normal).to_tuple()
            tangent = mesh_loop.tangent.to_tuple()

            position_values.extend(position)
            normal_values.extend(normal)
            tangent_values.extend(tangent)

        for loop_index in triangle.loops:

            for mesh_uv_layer_index, mesh_uv_layer in enumerate(mesh_uv_layers):
                uv = mesh_uv_layer.data[loop_index].uv
                uv_values_by_layer[mesh_uv_layer_index].extend(uv)

            for mesh_color_layer_index, mesh_color_layer in enumerate(mesh_color_layers):
                color = mesh_color_layer.data[loop_index].color
                color_values_by_layer[mesh_color_layer_index].extend(color)

    streams = [make_stream("position", 3, position_values)]
    if bool_normal:
        streams.append(make_stream("normal", 3, normal_values))
    else:
        pass
    if bool_tangent:
        streams.append(make_stream("tangent", 3, tangent_values))
    else:
        pass
    if bool_uv:
        streams.extend(map(lambda mesh_uv_layer, uv_values: make_stream(mesh_uv_layer.name, 2, uv_values), mesh_uv_layers, uv_values_by_layer))
    else:
        pass
    if bool_color:
        streams.extend(map(lambda mesh_color_layer, color_values: make_stream("color", 4, color_values), mesh_color_layers, color_values_by_layer))
    else:
        pass

    return streams
    
def export_to_file(f, obj, normal, tangent, uv, color):
# If in edit mode toggle to object mode before exporting
    if obj.mode == 'EDIT':
        bpy.ops.object.editmode_toggle()

    mesh = obj.data
    streams = export_mesh(mesh, normal, tangent, uv, color)
    s = json.dumps(streams, separators=(',', ':'), indent=None)
    f.write(bytearray(s, 'utf-8'))
