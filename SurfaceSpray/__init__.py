# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "SurfaceSpray",
    "author" : "Jose Daniel Rave Robayo, Daniel illanes Morillas, Sergio José Alfonso Rojas",
    "description" : " ",
    "blender" : (3, 3, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

# from codecs import unregister
from gc import get_threshold
import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       PointerProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

from .ss_clear_op import Clear_OT_Operator
from .ss_distribute_op import SurfaceSpray_OT_Operator
from .ss_demo_distribute_op import SurfaceSpray_OT_Operator_DEMO_SELECTION
from .ss_redistribute_op import Redistribute_OT_Operator
from.ss_panel import MAIN_PT_Panel
from.ss_panel import RULES_PT_Panel
from.ss_panel import SUBDIVIDE_PT_Panel

from.ss_panel import CUSTOM_PG_objectCollection
from.ss_panel import CUSTOM_OT_actions
from.ss_panel import CUSTOM_OT_addViewportSelection
from.ss_panel import CUSTOM_OT_printItems
from.ss_panel import CUSTOM_OT_clearList
from.ss_panel import CUSTOM_OT_removeDuplicates
from.ss_panel import CUSTOM_OT_selectItems
from.ss_panel import CUSTOM_OT_deleteObject
from.ss_panel import CUSTOM_UL_items
from.ss_panel import SOLUTION_OBJECTS_PT_Panel

# from.ss_panel import MY_OT_AddItem

classes = ( MAIN_PT_Panel,RULES_PT_Panel, SUBDIVIDE_PT_Panel, SurfaceSpray_OT_Operator, 
           SurfaceSpray_OT_Operator_DEMO_SELECTION, 
           Redistribute_OT_Operator, Clear_OT_Operator,
           CUSTOM_PG_objectCollection,CUSTOM_OT_actions,CUSTOM_OT_addViewportSelection,
           CUSTOM_OT_printItems,CUSTOM_OT_clearList,CUSTOM_OT_removeDuplicates,CUSTOM_OT_selectItems,
           CUSTOM_OT_deleteObject,CUSTOM_UL_items,SOLUTION_OBJECTS_PT_Panel)

import sys, os, site

def verify_user_sitepackages():
    usersitepackagespath = site.getsitepackages()

    if os.path.exists(usersitepackagespath) and usersitepackagespath not in sys.path:
        sys.path.append(usersitepackagespath)

# register, unregister = bpy.utils.register_classes_factory(classes)
def get_threshold(self):
    return self.get('threshold', 0)

def update_max_searches(self, context):
    self["actual_search"] = 1

def update_actual_search(self, context):
    self["actual_search"] = min(self["actual_search"], self["num_searches"])
    bpy.ops.addon.redistribute()
    
addon_keymaps = []

def register():
    print("Registering usersitepackagespath")
    # verify_user_sitepackages()

    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.solution_nodes = []

    bpy.types.Scene.custom = CollectionProperty(type=CUSTOM_PG_objectCollection)
    bpy.types.Scene.custom_index = IntProperty()

    bpy.types.Scene.num_cuts = bpy.props.IntProperty(
        name='Number of Cuts',
        default=0,
        description = "Number of Cuts. If zero (Only if one type of asset is going to "+
        "be distributed), cuts are made based in the size of the asset",
        min = 0,
        max = 100
    )

    bpy.types.Scene.threshold = bpy.props.FloatProperty(
        name='Threshold',
        default=0.5,
        min = 0.0,
        max = 1.0,
    )

    bpy.types.Scene.collectName = bpy.props.StringProperty(
        name='Collection Name',
        default="Objects Distributed"
    )

    bpy.types.Scene.num_assets = bpy.props.IntProperty(
        name='Number of Assets',
        default=1,
        min = 1,
        max = 100000
    )

    bpy.types.Scene.num_searches = bpy.props.IntProperty(
        name='Number of searches',
        default=1,
        min = 1,
        max = 20,
        update=update_max_searches
    )

    bpy.types.Scene.actual_search = bpy.props.IntProperty(
        name='Number of the actual selected search',
        default=1,
        min = 1,
        max = 20,
        update=update_actual_search
    )

    bpy.types.Scene.subdivide = bpy.props.BoolProperty(
        name='Subdivide Target',
        description = "This checkbox makes subdivisions of the target to fit "+
        "the asset in every possible position of the surface\n\nMake sure that"+
        " you normalize the scale of the asset before marking this checkbox",
        default=False
    )

    # Item rotation constraints
    bpy.types.Scene.rotate_x = bpy.props.BoolProperty(
        name='X',
        description = "This checkbox allows the rotation of the object in the X axis",
        default=False
    )

    bpy.types.Scene.rotate_y = bpy.props.BoolProperty(
        name='Y',
        description = "This checkbox allows the rotation of the object in the Y axis",
        default=False
    )

    bpy.types.Scene.rotate_z = bpy.props.BoolProperty(
        name='Z',
        description = "This checkbox allows the rotation of the object in the Z axis",
        default=False
    )

    # Item rotation range
    bpy.types.Scene.rot_range_x = bpy.props.FloatProperty(
        name='X',
        description = "Sets rotation range in the X axis",
        default=180.0,
        min = 0.0,
        max = 180.0,
    )
    
    bpy.types.Scene.rot_range_y = bpy.props.FloatProperty(
        name='Y',
        description = "Sets rotation range in the Y axis",
        default=180.0,
        min = 0.0,
        max = 180.0,
    )

    bpy.types.Scene.rot_range_z = bpy.props.FloatProperty(
        name='Z',
        description = "Sets rotation range in the Z axis",
        default=180.0,
        min = 0.0,
        max = 180.0,
    )

    # Item rotation steps
    bpy.types.Scene.rot_steps_x = bpy.props.FloatProperty(
        name='X',
        description = "Sets rotation steps in the X axis",
        default=1.0,
        min = 0.02,
        max = 360.0,
    )
    
    bpy.types.Scene.rot_steps_y = bpy.props.FloatProperty(
        name='Y',
        description = "Sets rotation steps in the Y axis",
        default=1.0,
        min = 0.02,
        max = 360.0,
    )

    bpy.types.Scene.rot_steps_z = bpy.props.FloatProperty(
        name='Z',
        description = "Sets rotation steps in the Z axis",
        default=1.0,
        min = 0.02,
        max = 360.0,
    )

    # Item distance to other objects
    bpy.types.Scene.item_distance = bpy.props.FloatProperty(
        name='Min Distance Between Assets',
        description = "Sets minumum distance of the asset to any other object "+
        "in the scene while placing it",
        default=0,
        min = 0.0,
        max = 100.0,
    )

    bpy.types.Scene.overlap_bool = bpy.props.BoolProperty(
        name='Allow Overlap',
        description = "This checkbox allows the assets to overlap with each other",
        default=False
    )

    bpy.types.Scene.bbox_bool = bpy.props.BoolProperty(
        name='Use Box',
        description = "This checkbox determines that the overlap between assets is"+
        " going to be\nchecked using a bounding box (Recomended if the asset is not going to be rotated)."+
        "\n\nLeaving it unchecked makes use of a bounding sphere (More reliable\n if the asset allows "+
        "rotation but not very accurate with oblong objects)",
        default=False
    )

    bpy.types.Scene.algorithm_enum = bpy.props.EnumProperty(
        name = "Algorithms",
        description = "Select an option",
        items = [('OP1', "Random", "Random Distribution", 1),
                 ('OP2', "Poisson", "Poisson Distribution", 2),
                 ('OP3', "Threshold", "Threshold Distribution", 3) 
        ]
    )

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu', 'A', 'PRESS', ctrl=True, shift=True)
    kmi.properties.name = "MY_MT_Menu"

    addon_keymaps.append((km, kmi))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.threshold, bpy.types.Scene.num_assets 

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index
    