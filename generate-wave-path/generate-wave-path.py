# Generates a random wave like path on the X-axis, length, amplitude and segments of the path are customizable.

bl_info = {
    "name": "Generate Wave Path",
    "author": "Ani V.",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > UI",
    "category": "Add Path",
}

import bpy
import random
from bpy.types import Operator, Panel
from bpy.props import IntProperty, FloatProperty


class OBJECT_OT_generate_wave_path(Operator):
    bl_idname = "object.generate_wave_path"
    bl_label = "Generate Wave Path"

    def execute(self, context):
        scene = context.scene
        num_segments = scene.wave_path_num_segments
        amplitude = scene.wave_path_amplitude
        x_distance = scene.wave_path_x_distance

        # Create a new path
        bpy.ops.curve.primitive_nurbs_path_add(
            radius=1,
            enter_editmode=False,
            align='WORLD',
            location=(0, 0, 0),
            scale=(1, 1, 1)
        )

        # Switch to edit mode
        bpy.ops.object.editmode_toggle()

        # Clear existing vertices
        bpy.ops.curve.delete(type='VERT')

        # Generate random z-coordinates for the path
        z_coords = [random.uniform(-amplitude, amplitude) for _ in range(num_segments + 1)]

        # Create vertices along the x-axis with random z-coordinates
        for i in range(num_segments + 1):
            bpy.ops.curve.vertex_add(location=(x_distance * i, 0, z_coords[i]))

        # Switch back to object mode
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class OBJECT_PT_generate_wave_path_panel(Panel):
    bl_idname = "OBJECT_PT_generate_wave_path_panel"
    bl_label = "Generate Wave Path"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Ani V. Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "wave_path_num_segments", text="Segments")

        row = layout.row()
        row.prop(scene, "wave_path_amplitude", text="Amplitude")
        
        row = layout.row()
        row.prop(scene, "wave_path_x_distance", text="X Distance")

        row = layout.row()
        row.operator("object.generate_wave_path")


def register():
    bpy.utils.register_class(OBJECT_PT_generate_wave_path_panel)
    bpy.utils.register_class(OBJECT_OT_generate_wave_path)
    bpy.types.Scene.wave_path_num_segments = IntProperty(
        name="Number of Segments",
        description="Number of segments in the path",
        default=10,
        min=1
    )
    bpy.types.Scene.wave_path_amplitude = FloatProperty(
        name="Amplitude",
        description="Maximum amplitude of the wave",
        default=0.5,
        min=0.0
    )
    bpy.types.Scene.wave_path_x_distance = FloatProperty(
        name="X Distance",
        description="Distance between each verts in the X-axis",
        default=1,
        min=0.0
    )


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_generate_wave_path_panel)
    bpy.utils.unregister_class(OBJECT_OT_generate_wave_path)
    del bpy.types.Scene.wave_path_num_segments
    del bpy.types.Scene.wave_path_amplitude



register()
