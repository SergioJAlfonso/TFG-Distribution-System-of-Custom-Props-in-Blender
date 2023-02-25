import bpy

class SUBDIVIDE_PT_Panel(bpy.types.Panel):
    bl_idname = "Subdivide_PT_Panel"
    bl_label = "Subdivide Target"
    bl_category = "SurfaceSpray"
    bl_description = "Subdivide Target"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        # Subdivision box
        box = layout.box()

        box.label(text="Subdivision")

        box.row().prop(context.scene, "subdivide")

        if(context.scene.subdivide):
            box.row().prop(context.scene, "num_cuts")