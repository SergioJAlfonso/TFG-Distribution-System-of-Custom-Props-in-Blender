import bpy

class SUBDIVIDE_PT_Panel(bpy.types.Panel):
    bl_idname = "SUBDIVIDE_PT_Panel"
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

    def register():
        bpy.types.Scene.num_cuts = bpy.props.IntProperty(
        name='Number of Cuts',
        default=0,
        description = "Number of Cuts. If zero (Only if one type of asset is going to "+
        "be distributed), cuts are made based in the size of the asset",
        min = 0,
        max = 100
        )

        bpy.types.Scene.subdivide = bpy.props.BoolProperty(
            name='Subdivide Target',
            description = "This checkbox makes subdivisions of the target to fit "+
            "the asset in every possible position of the surface\n\nMake sure that"+
            " you normalize the scale of the asset before marking this checkbox",
            default=False
        )
    
    def unregister():
        del (bpy.types.Scene.num_cuts, bpy.types.Scene.subdivide)
    

