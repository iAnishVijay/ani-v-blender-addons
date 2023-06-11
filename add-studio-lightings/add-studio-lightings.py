bl_info = {
    "name": "Studio Lighting Addon",
    "author": "Ani V.",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf",
    "description": "Adds a button to set up studio lighting",
    "category": "Object",
}

import bpy
import random
from bpy.types import Operator, Panel
from bpy.props import IntProperty, FloatProperty


class OBJECT_OT_studio_lighting(bpy.types.Operator):
    """Operator to add studio lighting"""
    bl_idname = "object.studio_lighting_addon"
    bl_label = "Add Studio Lighting"

    def execute(self, context):
        scene = context.scene
        # Remove all existing lights
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='LIGHT')
        bpy.ops.object.delete(use_global=False)

        # Set up three area lights
        light_size = scene.light_size

        # Key light
        bpy.ops.object.light_add(type='AREA', location=(0, 0, 5))
        key_light = bpy.context.active_object
        key_light.rotation_euler = (0, 0, 0)  # Set light rotation to 45 degrees
        key_light.data.energy = 2000.0
        key_light.data.color = (1.0, 1.0, 1.0)
        key_light.data.size = light_size

        # Fill light
        bpy.ops.object.light_add(type='AREA', location=(-5, 0, 5))
        fill_light = bpy.context.active_object
        fill_light.rotation_euler = (0, -0.7854, 0)  # Set light rotation to 45 degrees
        fill_light.data.energy = 1000.0
        fill_light.data.color = (0.5, 0.5, 0.5)
        fill_light.data.size = light_size

        # Back light
        bpy.ops.object.light_add(type='AREA', location=(5, 0, 5))
        back_light = bpy.context.active_object
        back_light.rotation_euler = (0, 0.7854, 0)  # Set light rotation to 45 degrees
        back_light.data.energy = 1000.0
        back_light.data.color = (0.5, 0.5, 0.5)
        back_light.data.size = light_size

        # Set up camera
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='CAMERA')
        bpy.ops.object.delete(use_global=False)
        bpy.ops.object.camera_add(location=(0, -10, 5))
        camera = bpy.context.active_object
        camera.rotation_euler = (1.0472, 0, 0)  # Set camera rotation to face the objects

        # Set up render settings
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        bpy.context.scene.eevee.use_bloom = False
        bpy.context.scene.eevee.use_ssr = False
        bpy.context.scene.eevee.use_ssr_refraction = False
        bpy.context.scene.eevee.use_soft_shadows = True
        bpy.context.scene.eevee.shadow_cube_size = '1024'
        bpy.context.scene.eevee.use_motion_blur = False
        bpy.context.scene.eevee.use_volumetric_lights = False
        bpy.context.scene.render.image_settings.file_format = 'PNG'

        # Set up lighting environment
        bpy.context.scene.world.use_nodes = True
        tree = bpy.context.scene.world.node_tree
        for node in tree.nodes:
            tree.nodes.remove(node)

        background_node = tree.nodes.new(type='ShaderNodeBackground')
        background_node.inputs[0].default_value = (0.1, 0.1, 0.1, 1.0)  # Set background color

        output_node = tree.nodes.new(type='ShaderNodeOutputWorld')

        tree.links.new(background_node.outputs[0], output_node.inputs[0])

        # Set up viewport shading
        bpy.context.space_data.shading.type = 'SOLID'

        return {'FINISHED'}

class OBJECT_PT_studio_light_panel(bpy.types.Panel):
    """Creates a Sub-Panel in the Property Area of the 3D View"""
    bl_label = "Add Studio Lighting"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ani V. Tools"
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Light Size")
        row = layout.row()
        row.prop(scene, "light_size", text="Light Size")
        row = layout.row()
        layout.operator("object.studio_lighting_addon", text="Add Studio Lighting")


def register():
    bpy.utils.register_class(OBJECT_OT_studio_lighting)
    bpy.utils.register_class(OBJECT_PT_studio_light_panel)
    bpy.types.Scene.light_size = FloatProperty(
        name="Light size",
        description="Size of lights",
        default=2,
        min=1
    )


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_studio_lighting)
    bpy.utils.unregister_class(OBJECT_PT_studio_light_panel)    


register()
