import bpy

class VertexProfile_ADD_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.vertex_profile_add"
    bl_label = "Simple operator"
    bl_description = "Adds a new vertex group as a profile."

    #Ask por a new name
    profileName : bpy.props.StringProperty(name="Vertex Profile Name", default="")

    def execute(self, context):

        #Save current object and mode 
        oldObject = bpy.context.view_layer.objects.active
        current_mode = context.scene.target.mode

        #Change to objects
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        #Deselect everything
        bpy.ops.object.select_all(action='DESELECT')
        
        #Change any selected object to Target object so it can be switched to weight painting. 
        bpy.context.view_layer.objects.active = context.scene.target

        #Adds new vertex group
        bpy.ops.object.vertex_group_add()
        context.scene.target.vertex_groups[-1].name = self.profileName
        
        #ALTERNATIVE CODE
        # obj.vertex_groups.new(name="mygroup")
        # bpy.ops.object.vertex_group_assign()

        #Assings property to new name
        context.scene.vgr_profile = self.profileName

        #Assign previous objects and return to previous mode 
        bpy.context.view_layer.objects.active = oldObject
        bpy.ops.object.mode_set(mode=current_mode)
        oldObject.select_set(True)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class VertexProfile_REMOVE_OT_Operator(bpy.types.Operator):
    bl_idname = "addon.vertex_profile_remove"
    bl_label = "Simple operator"
    bl_description = "Removes current vertex group profile."

    def execute(self, context):        
        if (len(context.scene.target.vertex_groups) == 0):
            return {'FINISHED'}

        #Save current object and mode 
        oldObject = bpy.context.view_layer.objects.active
        current_mode = context.scene.target.mode

        #Change to objects
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        #Deselect everything
        bpy.ops.object.select_all(action='DESELECT')
        
        #Change any selected object to Target object so it can be switched to weight painting. 
        bpy.context.view_layer.objects.active = context.scene.target

        #Removes current vertex group
        # bpy.ops.object.vertex_group_add()
        props = bpy.ops.object.vertex_group_remove()
        # props.all_unlocked = props.all = False

        #Assings property to last name
        if (len(context.scene.target.vertex_groups)>0):
            context.scene.vgr_profile = context.scene.target.vertex_groups[-1].name
        else:
            context.scene.vgr_profile = " "

        #Assign previous objects and return to previous mode 
        bpy.context.view_layer.objects.active = oldObject
        bpy.ops.object.mode_set(mode=current_mode)
        oldObject.select_set(True)

        return {'FINISHED'}
