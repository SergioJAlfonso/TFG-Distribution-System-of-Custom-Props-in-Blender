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
    "name" : "MegaTron",
    "author" : "SuperNenas",
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

from .mg_op import MegaTron_OT_Operator
from.mg_panel import Main_PT_Panel
from.mg_panel import Groups_PT_Panel
classes = ( Main_PT_Panel,Groups_PT_Panel, MegaTron_OT_Operator )

# register, unregister = bpy.utils.register_classes_factory(classes)
def get_threshold(self):
    return self.get('threshold', 0)

def register():

    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.threshold = bpy.props.FloatProperty(
        name='Threshold',
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

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.threshold, bpy.types.Scene.num_assets 
    
