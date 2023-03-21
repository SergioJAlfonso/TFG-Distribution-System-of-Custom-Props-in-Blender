import bpy

from bpy.props import (BoolProperty)

from bpy.types import (Operator)

class ASSET_SELECT_OT_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "assets.list_action"
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
        idx = scn.asset_index

        try:
            item = scn.assets[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.assets) - 1:
                item_next = scn.assets[idx+1].name
                scn.assets.move(idx, idx+1)
                scn.asset_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.asset_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.assets[idx-1].name
                scn.assets.move(idx, idx-1)
                scn.asset_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.asset_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.assets[idx].name)
                scn.asset_index -= 1
                scn.assets.remove(idx)
                self.report({'INFO'}, info)
            
            if(len(context.scene.assets) > 0):
                context.scene.asset = context.scene.assets[0].obj

        if self.action == 'ADD':
            if context.object:

                if(context.object == context.scene.target):
                    self.report({'INFO'}, "Shouldn't add TARGET object!")
                else:
                    item = scn.assets.add()
                    item.name = context.object.name
                    item.obj = context.object
                    scn.asset_index = len(scn.assets)-1
                    info = '"%s" added to list' % (item.name)
                    self.report({'INFO'}, info)
            else:
                self.report({'INFO'}, "Nothing selected in the Viewport")
        return {"FINISHED"}
    

class ASSET_SELECT_OT_addViewportSelection(Operator):
    """Add all items currently selected in the viewport"""
    bl_idname = "assets.add_viewport_selection"
    bl_label = "Add Selected Objects"
    bl_description = "Add all items currently selected in the viewport"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scn = context.scene
        selected_objs = context.selected_objects
        if selected_objs:
            new_objs = []
            for i in selected_objs:
                if(i == context.scene.target):
                    self.report({'INFO'}, "Shouldn't add TARGET object!")
                else:
                    item = scn.assets.add()
                    item.name = i.name
                    item.obj = i
                    new_objs.append(item.name)
            info = ', '.join(map(str, new_objs))
            if(len(new_objs) > 0):
                self.report({'INFO'}, 'Added: "%s"' % (info))
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")
        return{'FINISHED'}

class ASSET_SELECT_OT_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "assets.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.assets)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
        
    def execute(self, context):
        if bool(context.scene.assets):
            context.scene.assets.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}
    
    
class ASSET_SELECT_OT_removeDuplicates(Operator):
    """Remove all duplicates"""
    bl_idname = "assets.remove_duplicates"
    bl_label = "Remove Duplicates"
    bl_description = "Remove all duplicates"
    bl_options = {'INTERNAL'}

    def find_duplicates(self, context):
        """find all duplicates by name"""
        name_lookup = {}
        for c, i in enumerate(context.scene.assets):
            name_lookup.setdefault(i.obj.name, []).append(c)
        duplicates = set()
        for name, indices in name_lookup.items():
            for i in indices[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))
        
    @classmethod
    def poll(cls, context):
        # return bool(context.scene.asset)
        return True
        
    def execute(self, context):
        scn = context.scene
        removed_items = []

        # Reverse the list before removing the items
        for i in self.find_duplicates(context)[::-1]:
            scn.assets.remove(i)
            removed_items.append(i)
        if removed_items:
            scn.asset_index = len(scn.assets)-1
            info = ', '.join(map(str, removed_items))
            self.report({'INFO'}, "Removed indices: %s" % (info))
        else:
            self.report({'INFO'}, "No duplicates")
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
    
    
class ASSET_SELECT_OT_selectItems(Operator):
    """Select Items in the Viewport"""
    bl_idname = "assets.select_items"
    bl_label = "Select Item"
    bl_description = "Select Items in the Viewport"
    bl_options = {'REGISTER', 'UNDO'}

    select_all : BoolProperty(
        default=False,
        name="Select all Items of List",
        options={'SKIP_SAVE'})
        
    @classmethod
    def poll(cls, context):
        return bool(context.scene.assets)
    
    def execute(self, context):
        scn = context.scene
        idx = scn.asset_index
        
        try:
            item = scn.assets[idx]
        except IndexError:
            self.report({'INFO'}, "Nothing selected in the list")
            return{'CANCELLED'}
                   
        obj_error = False
        bpy.ops.object.select_all(action='DESELECT')
        if not self.select_all:
            name = scn.assets[idx].obj.name
            obj = scn.objects.get(name, None)
            if not obj: 
                obj_error = True
            else:
                obj.select_set(True)
                info = '"%s" selected in Vieport' % (obj.name)
        else:
            selected_items = []
            unique_objs = set([i.obj.name for i in scn.assets])
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
    
    def setSelectAll(self, selected_items):
        print("funciona")

class ASSET_SELECT_OT_update_list(Operator):
    """Update list of objects"""
    bl_idname = "assets.update_list"
    bl_label = "Updates list of objects"
    bl_description = "Updates list of objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    reverse_order: BoolProperty(
        default=False,
        name="Reverse Order")
    
    def execute(self, context):
        scn = context.scene

        index_toRemove = []
        for index, item in enumerate(context.scene.assets):
            if (item.obj is None):
                index_toRemove.append(index)
                continue

            obj_ = scn.objects.get(item.name, None)
            if (obj_ is None):
                index_toRemove.append(index)

        for i in index_toRemove[::-1]:
            scn.assets.remove(i)
 
        scn.asset_index = max(0, len(scn.assets) - 1) 
        return{'FINISHED'}