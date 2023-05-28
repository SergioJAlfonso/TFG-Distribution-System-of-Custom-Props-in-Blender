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
    "description" : "Addon to distribute custom objects over a surface.",
    "blender" : (3, 3, 0),
    "version" : (0, 1, 0),
    "location" : "View3D",
    "warning" : "Uses AIMA. Need to have installed the add-on SurfacePreparer, and install its dependencies.",
    "category" : "Mesh"
}

# from codecs import unregister
from gc import get_threshold
import bpy
import sys, os, site

from bpy.props import (PointerProperty,IntProperty, CollectionProperty)

from .Panels.rules.ss_rotate_op import Rotate_Operator

from .Panels.distribute.ss_clear_distribution_op import Clear_OT_Operator
from .Panels.ui_utilities.ss_paint_op import (PaintMode_OT_Operator, 
                                            ExitPaintMode_OT_Operator,
                                            InvertPainting_OT_Operator,
                                            PaintAll_OT_Operator,
                                            FaceOrientation_OT_Operator,
                                            RecalcNormals_OT_Operator)

from .Panels.ui_utilities.ss_vertexProfile_op import (VertexProfile_ADD_OT_Operator, VertexProfile_REMOVE_OT_Operator)

from .Panels.distribute.ss_single_distribute_op import SurfaceSpray_OT_Operator
from .Panels.distribute.ss_multi_distribute_op import SurfaceSpray_OT_Operator_DEMO_MULTI

from .Panels.distribute.ss_redistribute_op import Redistribute_OT_Operator


from .Panels.distribute.distribute_panel import *

from .Panels.rules.rules_panel  import RULES_PT_Panel


from .Panels.ui_utilities.ss_asset_select_op import *

from .Panels.distribute.ss_replace_op import *


from .Panels.partialSol.partialSol_ops import (PARTIAL_SOL_OT_actions,
                                               PARTIAL_SOL_OT_addViewportSelection,
                                               PARTIAL_SOL_OT_clearList,
                                               PARTIAL_SOL_OT_removeDuplicates,
                                               PARTIAL_SOL_OT_selectItems,
                                               PARTIAL_SOL_OT_update_list)

from .Panels.partialSol.partialSol_panel import (PARTIAL_SOL_PG_objectCollection,
                                                 PARTIAL_SOL_UL_items,
                                                 PARTIAL_SOL_PT_Panel,
                                                 ASSETS_UL_items)

from .Panels.rules.subdivide_panel import SUBDIVIDE_PT_Panel
from .Panels.rules.ss_reset_rules_op import Reset_Rules_OT_Operator


classes = (ASSET_SELECT_OT_actions, ASSET_SELECT_OT_addViewportSelection, ASSET_SELECT_OT_clearList,
           ASSET_SELECT_OT_removeDuplicates, ASSET_SELECT_OT_selectItems, ASSET_SELECT_OT_update_list, ASSETS_UL_items,Main_Object_Collection,
           PARTIAL_SOL_PG_objectCollection,PARTIAL_SOL_OT_actions,PARTIAL_SOL_OT_addViewportSelection, MAIN_PT_Panel, 
           RULES_PT_Panel,PARTIAL_SOL_OT_clearList,PARTIAL_SOL_OT_removeDuplicates,PARTIAL_SOL_OT_selectItems,
           PARTIAL_SOL_UL_items,PARTIAL_SOL_OT_update_list,PARTIAL_SOL_PT_Panel,
           SUBDIVIDE_PT_Panel, PARAMS_PT_Panel, SurfaceSpray_OT_Operator, 
           PaintMode_OT_Operator,
           ExitPaintMode_OT_Operator,
           InvertPainting_OT_Operator,
           PaintAll_OT_Operator,
           FaceOrientation_OT_Operator,
           RecalcNormals_OT_Operator,
           SurfaceSpray_OT_Operator_DEMO_MULTI, 
           Redistribute_OT_Operator, Clear_OT_Operator, Rotate_Operator,
           VertexProfile_ADD_OT_Operator, VertexProfile_REMOVE_OT_Operator,
           Reset_Rules_OT_Operator, ReplaceExistingCollectionName_ADD_OT_Operator)
def verify_user_sitepackages():
    usersitepackagespath = site.getsitepackages()

    if os.path.exists(usersitepackagespath) and usersitepackagespath not in sys.path:
        sys.path.append(usersitepackagespath)

def get_threshold(self):
    return self.get('threshold', 0)
    
def register():
    print("Registering classes")
    # verify_user_sitepackages()

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    print("Unregistering classes")
    for cls in classes:
        bpy.utils.unregister_class(cls) 