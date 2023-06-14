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

        # object Collection selection
        layout.label(text="Spawnable Collection:")
        layout.prop_search(scene, "spawnable_collection", bpy.data, "collections", text="")

        # Target Mesh selection
        layout.label(text="Target Mesh:")
        row = layout.row(align=True)
        row.prop_search(scene, "target_mesh", bpy.data, "objects", text="")
        row.operator("object.select_target_mesh", text="", icon='EYEDROPPER')

        # Parenting checkbox
        layout.prop(scene, "parent_objects", text="Parent Objects")

        # Placement button
        layout.operator("object.place_objects", text="Place Objects")

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

# Operator class for placing objects
class PlaceObjectsOperator(bpy.types.Operator):
    bl_idname = "object.place_objects"
    bl_label = "Place Objects"
    bl_options = {'REGISTER', 'UNDO'}

    # Execute the placement
    def execute(self, context):
        scene = context.scene

        # Get the selected object collection
        spawnable_collection_name = scene.spawnable_collection
        spawnable_collection = bpy.data.collections.get(spawnable_collection_name)
        if not spawnable_collection:
            self.report({'ERROR'}, "Object collection not found.")
            return {'CANCELLED'}

        # Get the selected target mesh
        target_mesh_name = scene.target_mesh
        target_mesh = bpy.data.objects.get(target_mesh_name)
        if not target_mesh or target_mesh.type != 'MESH':
            self.report({'ERROR'}, "Target mesh object not found or not a mesh.")
            return {'CANCELLED'}

        # Set the number of objects to place
        num_objects = 50

        # Clear the parent of the objects in the collection
        for rock in spawnable_collection.objects:
            rock.parent = None

        # Get the vertices of the target mesh
        target_vertices = [v.co for v in target_mesh.data.vertices]

        # Create a new collection with the same name as the target mesh
        collection_name = target_mesh.name
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)

        # Randomly place objects on the target mesh
        for _ in range(num_objects):
            # Select a random rock from the collection
            rock = random.choice(spawnable_collection.objects)

            # Randomly select a vertex from the target mesh
            vertex = random.choice(target_vertices)

            # Create a new instance of the rock and set its location to the selected vertex
            instance = rock.copy()
            instance.data = rock.data.copy()
            instance.location = vertex

            # Set random rotation and scale for the instance
            instance.rotation_euler = (
                random.uniform(0, 2*math.pi),
                random.uniform(0, 2*math.pi),
                random.uniform(0, 2*math.pi)
            )
            instance.scale = (
                random.uniform(0.5, 2),
                random.uniform(0.5, 2),
                random.uniform(0.5, 2)
            )

            # Parent the instance to the target mesh if the checkbox is toggled
            if scene.parent_objects:
                instance.parent = target_mesh

            # Link the instance to the new collection
            new_collection.objects.link(instance)

        # Add the target mesh to the new collection
        new_collection.objects.link(target_mesh)

        # Update the scene to reflect the changes
        bpy.context.view_layer.update()

        self.report({'INFO'}, "Objects placed successfully.")
        return {'FINISHED'}

# Register the UI panel and operator
classes = [
    RockPlacementPanel,
    SelectTargetMeshOperator,
    PlaceObjectsOperator,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.spawnable_collection = bpy.props.StringProperty()
    bpy.types.Scene.target_mesh = bpy.props.StringProperty()
    bpy.types.Scene.parent_objects = bpy.props.BoolProperty(
        name="Parent Objects",
        description="Toggle parenting of objects to the target mesh",
        default=True,
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.spawnable_collection
    del bpy.types.Scene.target_mesh
    del bpy.types.Scene.parent_objects

# Run the script
if __name__ == "__main__":
    register()
