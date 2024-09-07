### CLEAN UI: 3DVIEW > N-PANEL ###
import bpy
from .core.clean_export import CleanAssetExporter
from bpy.props import (StringProperty,
                       BoolProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       PropertyGroup,
                       )

# ------------------------------------------------------------------------
#    Store properties in the active scene
# ------------------------------------------------------------------------
class CleanSettings(PropertyGroup):
    ''' property settings '''
    bool_position : BoolProperty(
        name="Enable or Disable position",
        description="Position stream",
        default = True
        )

    bool_normal : BoolProperty(
        name="Enable or Disable normal stream",
        description="Normals stream",
        default = False
        )
        
    bool_tangent : BoolProperty(
        name="Enable or Disable tangent stream",
        description="Tangent stream",
        default = False
        )
    
    bool_uv : BoolProperty(
        name="Enable or Disable uv stream",
        description="UV coordinates stream",
        default = False
        )
        
    bool_color : BoolProperty(
        name="Enable or Disable color stream",
        description="Vertex color stream",
        default = False
        )

    bool_yup : BoolProperty(
        name="Orient Y-UP",
        description="Orient Y-UP",
        default = False
        )

    output_dir: StringProperty(
        name="Output Directory",
        description="Choose export directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )

# ------------------------------------------------------------------------
#    N PANEL GUI
# ------------------------------------------------------------------------
class CLEAN_PT_panel(Panel):
    ''' add-on panel '''
    bl_idname = "CLEAN_PT_panel"
    bl_label = "CLEAN GAME ASSET EXPORTER"
    bl_category = "CLEAN"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='', icon_value=93)

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        selection = bpy.context.selected_objects
        obj_count = len(selection)
        obj_name = bpy.context.object.name

        box_selected = layout.box()
        box_selected.alert = False
        box_selected.enabled = True
        box_selected.active = True
        box_selected.use_property_split = False
        box_selected.use_property_decorate = False
        box_selected.alignment = 'Center'.upper()
        box_selected.scale_x = 1.2
        box_selected.scale_y = 1.2
        # Display object name or object count when more than one object selected
        if (obj_count > 1):
             ob_text = str(obj_count) + ' Objects'
             ob_icon = 'GEOMETRY_NODES'
        elif (obj_count == 1):
             ob_text = obj_name
             ob_icon = 'RADIOBUT_ON'
        else:
             ob_text = 'None'
             ob_icon = 'HOLDOUT_OFF'
        box_selected.label(text='Selected: ' + ob_text, icon= ob_icon)

        # display stream properties
        box_streams = box_selected.box()
        box_streams.alert = False
        box_streams.enabled = True
        box_streams.active = True
        box_streams.use_property_split = False
        box_streams.use_property_decorate = False
        box_streams.alignment = 'Left'.upper()
        box_streams.scale_x = 1.2
        box_streams.scale_y = 1.2
        box_streams.label(text='--- Streams for export ---', icon='FILE_VOLUME')
        
        # Position stream exported by default
        box_default = box_streams.box()
        box_default.enabled = False
        box_default.active = False
        box_default.prop(mytool, "bool_position", text=" ∙ Vertex position")
        # Checkbox optional streams for export
        box_streams.prop(mytool, "bool_normal", text=" ∙ Normals")
        box_streams.prop(mytool, "bool_tangent", text=" ∙ Tangents")
        box_streams.prop(mytool, "bool_uv", text=" ∙ UV coordinates")
        box_streams.prop(mytool, "bool_color", text=" ∙ Vertex colors")
        box_selected.prop(mytool, "bool_yup", text="Y-UP")
        # Output export folder directory
        filepath = mytool.output_dir
        if not filepath:
            box_selected.alert = True
        else:
            box_selected.alert = False
        box_selected.prop(mytool, "output_dir")

        # Enable export operator only when mesh(s) are selected
        box_export = layout.box()
        mesh_count = 0
        for obj in selection:
            if obj.type == "MESH":
                mesh_count += 1
        if mesh_count > 0:
            box_export.enabled = True
            box_export.operator("clean.asset_export", text="Ready For Export")
        else:
            box_export.enabled = False
            box_export.operator("clean.asset_export", text="No Mesh(s) Selected")
        layout.separator()

# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------

classes = (
    CleanSettings,
    CLEAN_PT_panel,
    CleanAssetExporter,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.my_tool = PointerProperty(type=CleanSettings)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()