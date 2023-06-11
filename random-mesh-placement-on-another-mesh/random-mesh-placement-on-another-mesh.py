import bpy
import random
import math

bl_info = {
    "name": "Random Object Placement",
    "author": "Ani V.",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf",
    "description": "Places objects randomly on another object.",
    "category": "Object",
}

# UI panel class
class RockPlacementPanel(bpy.types.Panel):
    bl_label = "Random Object Placement"
    bl_idname = "OBJECT_PT_rock_placement_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ani V. Tools"

    # Draw UI elements
    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Rock Collection selection
        layout.label(text="Rock Collection:")
        layout.prop_search(scene, "rock_collection", bpy.data, "collections", text="")

        # Target Mesh selection
        layout.label(text="Target Mesh:")
        row = layout.row(align=True)
        row.prop_search(scene, "target_mesh", bpy.data, "objects", text="")
        row.operator("object.select_target_mesh", text="", icon='EYEDROPPER')

        # Placement button
        layout.operator("object.place_rocks", text="Place Rocks")

# Operator class for selecting target mesh
class SelectTargetMeshOperator(bpy.types.Operator):
    bl_idname = "object.select_target_mesh"
    bl_label = "Select Target Mesh"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene

        bpy.ops.wm.context_set_string(data_path="scene.target_mesh", value=context.object.name)

        return {'FINISHED'}

# Operator class for placing rocks
class PlaceRocksOperator(bpy.types.Operator):
    bl_idname = "object.place_rocks"
    bl_label = "Place Rocks"
    bl_options = {'REGISTER', 'UNDO'}

    # Execute the placement
    def execute(self, context):
        scene = context.scene

        # Get the selected rock collection
        rock_collection_name = scene.rock_collection
        rock_collection = bpy.data.collections.get(rock_collection_name)
        if not rock_collection:
            self.report({'ERROR'}, "Rock collection not found.")
            return {'CANCELLED'}

        # Get the selected target mesh
        target_mesh_name = scene.target_mesh
        target_mesh = bpy.data.objects.get(target_mesh_name)
        if not target_mesh or target_mesh.type != 'MESH':
            self.report({'ERROR'}, "Target mesh object not found or not a mesh.")
            return {'CANCELLED'}

        # Set the number of rocks to place
        num_rocks = 50

        # Clear the parent of the rocks in the collection
        for rock in rock_collection.objects:
            rock.parent = None

        # Get the vertices of the target mesh
        target_vertices = [v.co for v in target_mesh.data.vertices]

        # Randomly place rocks on the target mesh
        for _ in range(num_rocks):
            # Select a random rock from the collection
            rock = random.choice(rock_collection.objects)

            # Randomly select a vertex from the target mesh
            vertex = random.choice(target_vertices)

            # Create a new instance of the rock and set its location to the selected vertex
            instance = rock.copy()
            instance.data = rock.data.copy()
            instance.location = vertex

            # Set random rotation and scale for the instance
            instance.rotation_euler = (random.uniform(0, 2*math.pi), random.uniform(0, 2*math.pi), random.uniform(0, 2*math.pi))
            instance.scale = (random.uniform(0.5, 2), random.uniform(0.5, 2), random.uniform(0.5, 2))

            # Parent the instance to the target mesh
            instance.parent = target_mesh

            # Link the instance to the scene
            bpy.context.collection.objects.link(instance)

        # Update the scene to reflect the changes
        bpy.context.view_layer.update()

        self.report({'INFO'}, "Rocks placed successfully.")
        return {'FINISHED'}

# Register the UI panel and operator
classes = [
    RockPlacementPanel,
    SelectTargetMeshOperator,
    PlaceRocksOperator,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.rock_collection = bpy.props.StringProperty()
    bpy.types.Scene.target_mesh = bpy.props.StringProperty()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.rock_collection
    del bpy.types.Scene.target_mesh

# Run the script
if __name__ == "__main__":
    register()
