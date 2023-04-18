import bpy
import random

from ...algorithmsSS.algorithmsSS import best_first_graph_multiple_search as ss_best_fms
from ...algorithmsSS.algorithmsSS import hill_climbing as hillClimbing
from ...algorithmsSS.algorithmsSS import simulated_annealing_multiples as simulatedAnnealingMultiple


def update_asset(self, context):
    context.scene.asset = context.scene.assets[context.scene.asset_index].obj

class Main_Object_Collection(bpy.types.PropertyGroup):
     obj: bpy.props.PointerProperty(
        name="Object",
        type=bpy.types.Object, update=update_asset)

class MAIN_PT_Panel(bpy.types.Panel):
    bl_idname = "MAIN_PT_Panel"
    bl_label = "Object To Distribute"
    bl_category = "SurfaceSpray"
    bl_description = "Entry Data Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        # Add-on distribute buttons
        row.operator('addon.distribute', icon='OUTLINER_OB_POINTCLOUD', text = "Distribute")
        row.operator('addon.multidistribute', icon='GEOMETRY_NODES', text = "Multi Distribute")
        row.operator('addon.clear', icon='OUTLINER_DATA_POINTCLOUD', text = "Clear Distribution")

        row2 = layout.row()
        row2.template_list("ASSETS_UL_items", "",  bpy.context.scene, "assets",  bpy.context.scene, "asset_index", rows=2)

        col = row2.column(align=True)
        col.operator("assets.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("assets.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("assets.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("assets.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        
        row.operator("assets.update_list", icon="FILE_REFRESH")
        # row.operator("assets.add_viewport_selection", icon="HAND") #LINENUMBERS_OFF, ANIM
        row.operator("assets.clear_list", icon="X")
        row = col.row(align=True)
        row.operator("assets.select_items", icon="VIEW3D", text="Select Item in 3D View")
        selectItems = row.operator("assets.select_items", icon="GROUP", text="Select All Items in 3D View")
        selectItems.select_all = True

        row = col.row(align=True)

        col.separator()
        col.separator()
        row = layout.row()
        col = layout.column()

        # Target and asset prop search
        # col.prop_search(context.scene, "asset", context.scene, "objects", text="Asset")
        row.prop_search(context.scene, "target", context.scene, "objects", text="Target Object")
        row = layout.row()
        row.operator('addon.toggle_face_orientation', icon='NORMALS_FACE', text = "Toggle Face Orientation")
        row.operator('addon.recalc_normals', icon='MOD_NORMALEDIT', text = "Recalc Normals")
        

        #Painting Mode
        box1 = layout.box()
        row = box1.row()

        if(context.scene.target is not None):
            row.prop_search(context.scene, "vgr_profile", context.scene.target, "vertex_groups", text="Profile")
            row.operator("addon.vertex_profile_add", icon='ADD', text="")
            row.operator("addon.vertex_profile_remove", icon='REMOVE', text="")

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
        box3.column().prop(context.scene, "random_seed")
        box3.column().prop(context.scene, "collectName")

        box2 = layout.box()

        box2.label(text="Distribution Variations")

        box2.row().prop(context.scene, "num_searches")
        box2.row().prop(context.scene, "current_search")

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
        
        bpy.types.Scene.asset = bpy.props.PointerProperty(type=bpy.types.Object)

        bpy.types.Scene.assets = bpy.props.CollectionProperty(type=Main_Object_Collection)

        bpy.types.Scene.asset_index = bpy.props.IntProperty(
            name = "Asset Collection Index",
            update = update_asset_rules,
            default=-1
        )

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
        bpy.types.Scene.objects_data = []

        bpy.types.Scene.vgr_profile = bpy.props.StringProperty(
             name="vertex_group_profile",
             update= update_vertexGroupSelection)
        
        bpy.types.Scene.random_seed = bpy.props.IntProperty(
            name="Random Seed",
            default=11092022,
            min = 0,
            update=update_random_seed
        )
        
        

    def unregister():
        del (bpy.types.Scene.threshold, bpy.types.Scene.num_assets, 
             bpy.types.Scene.target, bpy.types.Scene.asset,
             bpy.types.Scene.algorithm_enum, bpy.types.Scene.collectName,
             bpy.types.Scene.num_searches, bpy.types.Scene.current_search,
             bpy.types.Scene.solution_nodes, bpy.types.Scene.algorithms_HashMap,
             bpy.types.Scene.vgr_profile)

def update_max_searches(self, context):
    self["current_search"] = 1

def update_random_seed(self, context):
    random.seed(self["Random Seed"])

def update_current_search(self, context):
    self["current_search"] = min(self["current_search"], self["num_searches"])
    bpy.ops.addon.redistribute()

def update_asset_rules(self, context):
    scn = context.scene

    context.scene.asset = context.scene.assets[context.scene.asset_index].obj

    scn.rules_panel_asset_index = scn.asset_index 

    scn.rotate_x = scn.itemRules_HashMap["rotate_x"][scn.asset_index]
    scn.rotate_y = scn.itemRules_HashMap["rotate_y"][scn.asset_index]
    scn.rotate_z = scn.itemRules_HashMap["rotate_z"][scn.asset_index]

    scn.rot_range_x = scn.itemRules_HashMap["rot_range_x"][scn.asset_index]
    scn.rot_range_y = scn.itemRules_HashMap["rot_range_y"][scn.asset_index]
    scn.rot_range_z = scn.itemRules_HashMap["rot_range_z"][scn.asset_index]

    scn.rot_steps_x = scn.itemRules_HashMap["rot_steps_x"][scn.asset_index]
    scn.rot_steps_y = scn.itemRules_HashMap["rot_steps_y"][scn.asset_index]
    scn.rot_steps_z = scn.itemRules_HashMap["rot_steps_z"][scn.asset_index]

    scn.overlap_bool = scn.itemRules_HashMap["overlap_bool"][scn.asset_index]
    scn.bbox_bool = scn.itemRules_HashMap["bbox_bool"][scn.asset_index]

    scn.item_distance = scn.itemRules_HashMap["item_distance"][scn.asset_index]

    scn.scale_factor_min = scn.itemRules_HashMap["scale_factor_min"][scn.asset_index]
    scn.scale_factor_max = scn.itemRules_HashMap["scale_factor_max"][scn.asset_index]

    scn.item_percentage = scn.itemRules_HashMap["item_percentage"][scn.asset_index]

def update_vertexGroupSelection(self, context):
    # context.scene.target.vertex_groups[context.scene.vgr_profile].select = True
    #Save current mode
    current_mode = context.scene.target.mode

    #Get target vertex groups
    vgroups = context.scene.target.vertex_groups
    found = True
    try:
        #Search if exist profile name as vertex group
        selectedGroup = vgroups[context.scene.vgr_profile]
    except:
        found = False
    
    #In case it doesn't exist we reset to default value
    if not found:
        context.scene.property_unset("vgr_profile")
        return 

    #Get index vertex group
    vgroups.active_index = selectedGroup.index 

    #Assing to active vertex group 
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.object.vertex_group_select()
    # bpy.ops.object.vertex_group_set_active(group='Group')
    #Get back to old mode
    bpy.ops.object.mode_set(mode=current_mode)