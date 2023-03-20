import bpy

from ...algorithmsSS.algorithmsSS import best_first_graph_multiple_search as ss_best_fms
from ...algorithmsSS.algorithmsSS import hill_climbing as hillClimbing
from ...algorithmsSS.algorithmsSS import simulated_annealing_multiples as simulatedAnnealingMultiple

class Main_Object_Collection(bpy.types.PropertyGroup):
     obj: bpy.props.PointerProperty(
        name="Object",
        type=bpy.types.Object)

class MAIN_PT_Panel(bpy.types.Panel):
    bl_idname = "MAIN_PT_Panel"
    bl_label = "Object To Distribute"
    bl_category = "SurfaceSpray"
    bl_description = "Entry Data Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row2 = layout.row()
        row2.template_list("PARTIAL_SOL_UL_items", "",  bpy.context.scene, "asset",  bpy.context.scene, "asset_index", rows=2)

        col = row2.column(align=True)
        col.operator("asset.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("asset.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("asset.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("asset.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("asset.update_list", icon="FILE_REFRESH")

        row = col.row(align=True)
        row.operator("asset.clear_list", icon="X")
        row.operator("asset.remove_duplicates", icon="GHOST_ENABLED")
        
        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("asset.add_viewport_selection", icon="HAND") #LINENUMBERS_OFF, ANIM
        row = col.row(align=True)
        row.operator("asset.select_items", icon="VIEW3D", text="Select Item in 3D View")
        selectItems = row.operator("asset.select_items", icon="GROUP", text="Select All Items in 3D View")

        selectItems.select_all = True

        row = col.row(align=True)

        row = layout.row()
        col = layout.column()

        # Target and asset prop search
        # col.prop_search(context.scene, "asset", context.scene, "objects", text="Asset")
        col.prop_search(context.scene, "target", context.scene, "objects", text="Target Object")
        
        # Add-on distribute buttons
        row.operator('addon.distribute', icon='OUTLINER_OB_POINTCLOUD', text = "Distribute")
        row.operator('addon.distribute_partialdemo', icon='OUTLINER_OB_POINTCLOUD', text = "Test Distribute")
        row.operator('addon.clear', icon='OUTLINER_DATA_POINTCLOUD', text = "Clear")

        #Painting Mode
        box1 = layout.box()
        row = box1.row()

        
        row.operator('addon.enter_paint_mode', icon='WPAINT_HLT', text = "Paint")
        #In case we are in Weight Painting with Target Object, we show all options
        if ((context.active_object == context.scene.target) and   context.active_object.mode == "WEIGHT_PAINT"):
                row.operator('addon.exit_paint_mode', icon='LOOP_BACK', text = "Exit")
                
                row = box1.row()
                row.operator('addon.invert_painting', icon='UV_SYNC_SELECT', text = "Invert")

                row = box1.row()
                row.operator('addon.paint_all', icon='MATFLUID', text = "Paint All:")
                row.column().prop(context.scene, "allWeightValue", text = "Weight Value")

        # Distribution Parameters box
        box3 = layout.box()

        box3.label(text="Distribution Parameters")

        box3.column().prop(context.scene, "algorithm_enum")

        box3.column().prop(context.scene, "vertexSelection_enum")
        
        # if (context.scene.algorithm_enum == "OP1"):
        box3.column().prop(context.scene, "threshold")

        box3.column().prop(context.scene, "num_assets")
        box3.column().prop(context.scene, "collectName")

        box2 = layout.box()

        box2.label(text="Multi Distribute")

        box2.row().prop(context.scene, "num_searches")
        box2.row().prop(context.scene, "current_search")
        # box2.row().operator('addon.redistribute', text = "Change search")
        # placeholder = context.scene.placeholder
        # col.prop(placeholder, "inc_dec_int", text="Asset Instances")

        # # Show list of vertex groups
        # boxVGroup = layout.box()
        # boxVGroup.label(text="Vertex Groups")

        # obj = context.scene.target
        # row = boxVGroup.row()
        # row.template_list("MESH_UL_vgroups", "", obj, "vertex_groups", obj.vertex_groups, "active_index")
        
        # # Add new vertex group button
        # col = boxVGroup.column()
        # col.operator("object.vertex_group_add", icon='ADD', text="New Vertex Group")

        # # Remove vertex group button
        # if obj.vertex_groups:
        #     col.operator("object.vertex_group_remove", icon='REMOVE', text="Remove Vertex Group")
        
        # # Rename vertex group
        # row = boxVGroup.row()
        # row.prop(context.object.vertex_groups.active, "name")

    def register():
        bpy.types.Scene.threshold = bpy.props.FloatProperty(
        name='Threshold',
        default=0.5,
        min = 0.0,
        max = 1.0,
        )

        bpy.types.Scene.allWeightValue = bpy.props.FloatProperty(
        name='All Weight Value',
        default=0.5,
        min = 0.0,
        max = 1.0,
        )

        bpy.types.Scene.num_assets = bpy.props.IntProperty(
        name='Number of Assets',
        default=1,
        min = 1,
        max = 100000
        )    

        bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Object)
        
        bpy.types.Scene.asset = bpy.props.PointerProperty(type=bpy.types.Object, update=updateAsset)

        bpy.types.Scene.assets = bpy.props.CollectionProperty(type=Main_Object_Collection)

        bpy.types.Scene.asset_index = bpy.props.IntProperty()

        bpy.types.Scene.algorithms_HashMap = {}

        bpy.types.Scene.algorithms_HashMap["BFS"] = ss_best_fms
        bpy.types.Scene.algorithms_HashMap["Hill-Climbing"] = hillClimbing
        bpy.types.Scene.algorithms_HashMap["Simulated Annealing"] = simulatedAnnealingMultiple
        # bpy.types.Scene.algorithms_HashMap["BFS"] = ss_best_fms

        bpy.types.Scene.algorithm_enum = bpy.props.EnumProperty(
                name = "Algorithms",
                description = "Select an option",
                items = [('OP1', "BFS", "Best First Search", 1),
                        ('OP2', "Hill-Climbing", "Hill-climbing", 2),
                        ('OP3', "Simulated Annealing", "Simulated Annealing", 3) 
                ]
            )
        
        bpy.types.Scene.vertexSelection_enum = bpy.props.EnumProperty(
                name = "Vertex Selection by Weight",
                description = "Select an option",
                items = [('OP1', "Random", "Random", 1),
                        ('OP2', "Probability", "Its weight assign its probability", 2),
                ]
            )

        bpy.types.Scene.collectName = bpy.props.StringProperty(
            name='Collection Name',
            default="Objects Distributed"
        )

        bpy.types.Scene.num_searches = bpy.props.IntProperty(
        name='Number of searches',
        default=1,
        min = 1,
        max = 20,
        update= update_max_searches
        )

        bpy.types.Scene.current_search = bpy.props.IntProperty(
            name='Number of current selected search',
            default=1,
            min = 1,
            max = 20,
            update= update_current_search
        )

        bpy.types.Scene.solution_nodes = []



    def unregister():
        del (bpy.types.Scene.threshold, bpy.types.Scene.num_assets, 
             bpy.types.Scene.target, bpy.types.Scene.asset,
             bpy.types.Scene.algorithm_enum, bpy.types.Scene.collectName,
             bpy.types.Scene.num_searches, bpy.types.Scene.current_search,
             bpy.types.Scene.solution_nodes)

def update_max_searches(self, context):
    self["current_search"] = 1

def update_current_search(self, context):
    self["current_search"] = min(self["current_search"], self["num_searches"])
    bpy.ops.addon.redistribute()










# class VGRUP_PT_Panel(bpy.types.Panel):
#     bl_idname = "VGoup_PT_Panel"
#     bl_label = "Vertex weight groups"
#     bl_category = "SurfaceSpray"
#     bl_description = "Vertex weight groups"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"

#     def draw(self, context):
#         layout = self.layout