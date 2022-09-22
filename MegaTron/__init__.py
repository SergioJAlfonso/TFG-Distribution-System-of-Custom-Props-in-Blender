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
import bpy

from .mg_op import MegaTron_OT_Operator
from.mg_panel import MegaTron_PT_Panel

classes = (MegaTron_OT_Operator, MegaTron_PT_Panel)

register, unregister = bpy.utils.register_classes_factory(classes)
