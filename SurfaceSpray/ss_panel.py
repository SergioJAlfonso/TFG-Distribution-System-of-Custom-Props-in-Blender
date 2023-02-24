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

#definimos que lo que queremos seleccionar(target de la escena) es de tipo Object
bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Object)
bpy.types.Scene.asset = bpy.props.PointerProperty(type=bpy.types.Object)


class CUSTOM_OT_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "custom.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}
    
    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.custom) - 1:
                item_next = scn.custom[idx+1].name
                scn.custom.move(idx, idx+1)
                scn.custom_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.custom[idx-1].name
                scn.custom.move(idx, idx-1)
                scn.custom_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.custom[idx].name)
                scn.custom_index -= 1
                scn.custom.remove(idx)
                self.report({'INFO'}, info)
                
        if self.action == 'ADD':
            if context.object:
                item = scn.custom.add()
                item.name = context.object.name
                item.obj = context.object
                scn.custom_index = len(scn.custom)-1
                info = '"%s" added to list' % (item.name)
                self.report({'INFO'}, info)
            else:
                self.report({'INFO'}, "Nothing selected in the Viewport")
        return {"FINISHED"}
    

class CUSTOM_OT_addViewportSelection(Operator):
    """Add all items currently selected in the viewport"""
    bl_idname = "custom.add_viewport_selection"
    bl_label = "Add Viewport Selection to List"
    bl_description = "Add all items currently selected in the viewport"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scn = context.scene
        selected_objs = context.selected_objects
        if selected_objs:
            new_objs = []
            for i in selected_objs:
                item = scn.custom.add()
                item.name = i.name
                item.obj = i
                new_objs.append(item.name)
            info = ', '.join(map(str, new_objs))
            self.report({'INFO'}, 'Added: "%s"' % (info))
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")
        return{'FINISHED'}
    
    
class CUSTOM_OT_printItems(Operator):
    """Print all items and their properties to the console"""
    bl_idname = "custom.print_items"
    bl_label = "Print Items to Console"
    bl_description = "Print all items and their properties to the console"
    bl_options = {'REGISTER', 'UNDO'}
    
    reverse_order: BoolProperty(
        default=False,
        name="Reverse Order")
    
    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)
    
    def execute(self, context):
        scn = context.scene
        if self.reverse_order:
            for i in range(scn.custom_index, -1, -1):        
                ob = scn.custom[i].obj
                print ("Object:", ob,"-",ob.name, ob.type)
        else:
            for item in scn.custom:
                ob = item.obj
                print ("Object:", ob,"-",ob.name, ob.type)
        return{'FINISHED'}


class CUSTOM_OT_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "custom.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
        
    def execute(self, context):
        if bool(context.scene.custom):
            context.scene.custom.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}
    
    
class CUSTOM_OT_removeDuplicates(Operator):
    """Remove all duplicates"""
    bl_idname = "custom.remove_duplicates"
    bl_label = "Remove Duplicates"
    bl_description = "Remove all duplicates"
    bl_options = {'INTERNAL'}

    def find_duplicates(self, context):
        """find all duplicates by name"""
        name_lookup = {}
        for c, i in enumerate(context.scene.custom):
            name_lookup.setdefault(i.obj.name, []).append(c)
        duplicates = set()
        for name, indices in name_lookup.items():
            for i in indices[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))
        
    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)
        
    def execute(self, context):
        scn = context.scene
        removed_items = []
        # Reverse the list before removing the items
        for i in self.find_duplicates(context)[::-1]:
            scn.custom.remove(i)
            removed_items.append(i)
        if removed_items:
            scn.custom_index = len(scn.custom)-1
            info = ', '.join(map(str, removed_items))
            self.report({'INFO'}, "Removed indices: %s" % (info))
        else:
            self.report({'INFO'}, "No duplicates")
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
    
    
class CUSTOM_OT_selectItems(Operator):
    """Select Items in the Viewport"""
    bl_idname = "custom.select_items"
    bl_label = "Select Item(s) in Viewport"
    bl_description = "Select Items in the Viewport"
    bl_options = {'REGISTER', 'UNDO'}

    select_all = BoolProperty(
        default=False,
        name="Select all Items of List",
        options={'SKIP_SAVE'})
        
    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)
    
    def execute(self, context):
        scn = context.scene
        idx = scn.custom_index
        
        try:
            item = scn.custom[idx]
        except IndexError:
            self.report({'INFO'}, "Nothing selected in the list")
            return{'CANCELLED'}
                   
        obj_error = False
        bpy.ops.object.select_all(action='DESELECT')
        if not self.select_all:
            name = scn.custom[idx].obj.name
            obj = scn.objects.get(name, None)
            if not obj: 
                obj_error = True
            else:
                obj.select_set(True)
                info = '"%s" selected in Vieport' % (obj.name)
        else:
            selected_items = []
            unique_objs = set([i.obj.name for i in scn.custom])
            for i in unique_objs:
                obj = scn.objects.get(i, None)
                if obj:
                    obj.select_set(True)
                    selected_items.append(obj.name)
            
            if not selected_items: 
                obj_error = True
            else:
                missing_items = unique_objs.difference(selected_items)
                if not missing_items:
                    info = '"%s" selected in Viewport' \
                        % (', '.join(map(str, selected_items)))
                else:
                    info = 'Missing items: "%s"' \
                        % (', '.join(map(str, missing_items)))
        if obj_error: 
            info = "Nothing to select, object removed from scene"
        self.report({'INFO'}, info)    
        return{'FINISHED'}


class CUSTOM_OT_deleteObject(Operator):
    """Delete object from scene"""
    bl_idname = "custom.delete_object"
    bl_label = "Remove Object from Scene"
    bl_description = "Remove object from scene"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
        
    def execute(self, context):
        scn = context.scene
        selected_objs = context.selected_objects
        idx = scn.custom_index
        try:
            item = scn.custom[idx]
        except IndexError:
            pass
        else:        
            ob = scn.objects.get(item.obj.name)
            if not ob:
                self.report({'INFO'}, "No object of that name found in scene")
                return {"CANCELLED"}
            else:
                bpy.ops.object.select_all(action='DESELECT')
                ob.select_set(True)
                bpy.ops.object.delete()
                
            info = ' Item "%s" removed from Scene' % (len(selected_objs))
            scn.custom_index -= 1
            scn.custom.remove(idx)
            self.report({'INFO'}, info)
        return{'FINISHED'}
    

# -------------------------------------------------------------------
#   Drawing
# -------------------------------------------------------------------

class CUSTOM_UL_items(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = item.obj
        custom_icon = "OUTLINER_OB_%s" % obj.type
        split = layout.split(factor=0.3)
        split.label(text="Index: %d" % (index))
        split.prop(obj, "name", text="", emboss=False, translate=False, icon=custom_icon)
            
    def invoke(self, context, event):
        pass   


# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class CUSTOM_PG_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    obj: PointerProperty(
        name="Object",
        type=bpy.types.Object)

class MAIN_PT_Panel(bpy.types.Panel):
    bl_idname = "Main_PT_Panel"
    bl_label = "Object To Distribute"
    bl_category = "SurfaceSpray"
    bl_description = "Entry Data Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = layout.column()

        # Target and asset prop search
        col.prop_search(context.scene, "asset", context.scene, "objects", text="Asset")
        col.prop_search(context.scene, "target", context.scene, "objects", text="Target Object")
        
        # Add-on distribute buttons
        row.operator('addon.distribute', text = "Distribute")
        row.operator('addon.distributedemo', text = "DistributeDemo")
        row.operator('addon.clear', text = "Clear")

        # Distribution Parameters box
        box3 = layout.box()

        box3.label(text="Distribution Parameters")

        box3.column().prop(context.scene, "algorithm_enum")
        
        if (context.scene.algorithm_enum == "OP1"):
            box3.column().prop(context.scene, "threshold")

        box3.column().prop(context.scene, "num_assets")
        box3.column().prop(context.scene, "collectName")

        box2 = layout.box()

        box2.label(text="Distribute Demo")

        box2.row().prop(context.scene, "num_searches")
        box2.row().prop(context.scene, "actual_search")
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

class SOLUTION_OBJECTS_PT_Panel(bpy.types.Panel):
    bl_idname = "SolutionObject_PT_Panel"
    bl_label = "Objects part of the solution"
    bl_category = "SurfaceSpray"
    bl_description = "Collection of objects in the solution."
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        scn = bpy.context.scene

        rows = 2
        row2 = layout.row()
        row2.template_list("CUSTOM_UL_items", "", scn, "custom", scn, "custom_index", rows=rows)

        col = row2.column(align=True)
        col.operator("custom.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("custom.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("custom.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("custom.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("custom.print_items", icon="LINENUMBERS_ON")
        row = col.row(align=True)
        row.operator("custom.clear_list", icon="X")
        row.operator("custom.remove_duplicates", icon="GHOST_ENABLED")
        
        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("custom.add_viewport_selection", icon="HAND") #LINENUMBERS_OFF, ANIM
        row = col.row(align=True)
        row.operator("custom.select_items", icon="VIEW3D", text="Select Item in 3D View")
        row.operator("custom.select_items", icon="GROUP", text="Select All Items in 3D View")
        row = col.row(align=True)
        row.operator("custom.delete_object", icon="X")     

class RULES_PT_Panel(bpy.types.Panel):
    bl_idname = "Rules_PT_Panel"
    bl_label = "Asset Rules"
    bl_category = "SurfaceSpray"
    bl_description = "Rules that specify how the asset is placed"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        # Item Rules box
        box = layout.box()

        box.label(text="Asset Rules")

        rotationBox = box.box()

        rotation_row = rotationBox.row()

        rotation_row.alignment = "CENTER"

        # Rotation
        rotation_row.label(text="Allow Rotation:")
        rotation_row.prop(context.scene, "rotate_x")
        rotation_row.prop(context.scene, "rotate_y")
        rotation_row.prop(context.scene, "rotate_z")

        if(context.scene.rotate_x or context.scene.rotate_y or context.scene.rotate_z):
            #Range and steps
            
            rotation_range_row = rotationBox.row()
            rotation_step_row = rotationBox.row()

            rotation_range_row.alignment = "CENTER"
            rotation_step_row.alignment = "CENTER"

            rotation_range_row.label(text="Range:")
            rotation_step_row.label(text="Steps:")

            if(context.scene.rotate_x):
                rotation_range_row.prop(context.scene, "rot_range_x")
                rotation_step_row.prop(context.scene, "rot_steps_x")

            if(context.scene.rotate_y):
                rotation_range_row.prop(context.scene, "rot_range_y")
                rotation_step_row.prop(context.scene, "rot_steps_y")
            
            if(context.scene.rotate_z):
                rotation_range_row.prop(context.scene, "rot_range_z")
                rotation_step_row.prop(context.scene, "rot_steps_z")
            

        # Distance
        box.row().prop(context.scene, "item_distance")

        # Overlap
        row = box.row()

        row.prop(context.scene, "overlap_bool")

        if(context.scene.overlap_bool):
            row.prop(context.scene, "bbox_bool")
    
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

# class VGRUP_PT_Panel(bpy.types.Panel):
#     bl_idname = "VGoup_PT_Panel"
#     bl_label = "Vertex weight groups"
#     bl_category = "SurfaceSpray"
#     bl_description = "Vertex weight groups"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"

#     def draw(self, context):
#         layout = self.layout