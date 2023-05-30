bl_info = {
    "name": "Procedural Textures",
    "author": "Ani V.",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf",
    "description": "Generates and adds procedural textures like muskgrave, vornoi etc to the selected mesh.",
    "category": "Material",
}

import bpy

class OBJECT_OT_procedural_textures(bpy.types.Panel):
  def execute(self, context):
        
    return {'FINISHED'}