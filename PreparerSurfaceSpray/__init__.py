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

import bpy
import subprocess
import os
import site
import shutil

bl_info = {
    "name" : "Preparer_SurfaceSpray",
    "author" : "Jose Daniel Rave Robayo, Daniel illanes Morillas, Sergio José Alfonso Rojas",
    "description" : " ",
    "blender" : (3, 3, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Mesh"
}


class install_Dependencies_OT_Operator(bpy.types.Operator):
    bl_idname = 'p_ss.install_dependencies'
    bl_label = 'Add Cube'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        result = subprocess.run(['pip', 'install', 'aima3'], capture_output=True, text=True)

        result = subprocess.run(['where', 'python'], capture_output=True, text=True)

        rutas = result.stdout.split("\n")

        print(rutas)

        found = False

        for ruta in rutas:
            if found:
                break

            ruta_aima = os.path.dirname(ruta)

            # Lista de carpetas para navegar
            carpetas = ['Lib', 'site-packages', 'aima3']

            # Navegar por las carpetas una por una
            for carpeta in carpetas:
                ruta_aima = os.path.join(ruta_aima, carpeta)  # Unir la ruta actual con la siguiente carpeta
                if not os.path.exists(ruta_aima):  # Verificar si la carpeta existe
                    print(f'Error: La carpeta {ruta_aima} no existe.')
                    break
                else:
                    if (carpeta == carpetas[-1]):
                        found = True

        print(f'Aima path: {ruta_aima}')

        usersitepackagespath = site.getsitepackages()[-1]
        usersitepackagespath += "\\aima3"
 
        print(f'Blender\'s packages path: {usersitepackagespath}')
              
        if not os.path.exists(usersitepackagespath):
            shutil.copytree(ruta_aima, usersitepackagespath)

        return {"FINISHED"}
 

class InstallDependecies_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
 
    # add_bevel: bpy.props.EnumProperty(
    #     items=[
    #         ('bevel', 'Add bevel', '', '', 0),
    #         ('no_bevel', 'No bevel', '', '', 1)
    #     ],
    #     default='no_bevel'
    # )
 
    def draw(self, context):
        layout = self.layout
        layout.label(text='Press to install addon dependecies:')

        usersitepackagespath = site.getsitepackages()[-1]
        usersitepackagespath += "\\aima3"

        dependenciesInstalled = ""
        if os.path.exists(usersitepackagespath):
            dependenciesInstalled = "(Already Installed)"


        row = layout.row()
        row.operator("p_ss.install_dependencies", icon='PREFERENCES', text=f"Install Dependencies {dependenciesInstalled}")
 
 
def register():
    bpy.utils.register_class(install_Dependencies_OT_Operator)
    bpy.utils.register_class(InstallDependecies_Preferences)
 
 
def unregister():
    bpy.utils.unregister_class(InstallDependecies_Preferences)
    bpy.utils.unregister_class(install_Dependencies_OT_Operator)