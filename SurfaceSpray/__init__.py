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
import sys, os, site

from bpy.props import (PointerProperty,IntProperty, CollectionProperty)

from .Panels.distribute.ss_clear_op import Clear_OT_Operator
from .Panels.distribute.ss_distribute_op import SurfaceSpray_OT_Operator
from .Panels.distribute.ss_demo_distribute_op import SurfaceSpray_OT_Operator_DEMO_SELECTION
from .Panels.distribute.ss_redistribute_op import Redistribute_OT_Operator

from .Panels.distribute.distribute_panel import MAIN_PT_Panel

from .Panels.partialSol.partialSol_ops import (PARTIAL_SOL_OT_actions,
                                               PARTIAL_SOL_OT_addViewportSelection,
                                               PARTIAL_SOL_OT_clearList,
                                               PARTIAL_SOL_OT_removeDuplicates,
                                               PARTIAL_SOL_OT_selectItems,
                                               PARTIAL_SOL_OT_update_list)

from .Panels.partialSol.partialSol_panel import (PARTIAL_SOL_PG_objectCollection,
                                                 PARTIAL_SOL_UL_items,
                                                 PARTIAL_SOL_PT_Panel)

from .Panels.rules_panel  import RULES_PT_Panel
from .Panels.subdivide_panel import SUBDIVIDE_PT_Panel

# from.ss_panel import MY_OT_AddItem

classes = ( MAIN_PT_Panel, PARTIAL_SOL_PG_objectCollection,PARTIAL_SOL_OT_actions,PARTIAL_SOL_OT_addViewportSelection,
           PARTIAL_SOL_OT_clearList,PARTIAL_SOL_OT_removeDuplicates,PARTIAL_SOL_OT_selectItems,
           PARTIAL_SOL_UL_items,PARTIAL_SOL_OT_update_list,PARTIAL_SOL_PT_Panel,
           SUBDIVIDE_PT_Panel ,RULES_PT_Panel, SurfaceSpray_OT_Operator, 
           SurfaceSpray_OT_Operator_DEMO_SELECTION, 
           Redistribute_OT_Operator, Clear_OT_Operator)

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