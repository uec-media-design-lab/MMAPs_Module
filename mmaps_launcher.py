import mmaps 
import bpy
import myutil
import math
from bpy.props import *

bl_info = {
    "name": "MMAPs Launcher",
    "author": "Shunji Kiuchi",
    "version": (3, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "This addon is to create MMAPs in scene.",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

class MMAP_OT_MMAPsLancher(bpy.types.Operator):
    bl_idname = "object.launch_mmaps"
    bl_label = "MMAPs Launch"
    bl_description = "Launch the MMAPs in scene."


    @classmethod
    def __launch(cls, context):
        '''
        Create MMAPs object include mirrors and glass with specified parameters. 
        '''
        scene = context.scene
        print("Start creating the MMAPs...")

        digit_func = myutil.getRoundDigit
        
        size = round(scene.mmaps_size, digit_func(scene.mmaps_size))
        spacing = round(scene.slit_spacing, digit_func(scene.slit_spacing)) 
        height_scale = round(scene.slit_heightscale, 2)
        detailing = int(scene.plane_detailing)
        ior = round(scene.glass_ior, 2)
        mmaps.createDetailedMMAPs(size=size, spacing=spacing, detailing=detailing, height_scale=height_scale, ior=ior)

    @classmethod 
    def is_exist(cls, context):
        '''
        Check if mmaps is existed
        '''
        scene = context.scene
        parent_name = scene.parent_name
        return bpy.data.objects.get(parent_name) is not None

    # This function is called when "Launch" button is pressed.
    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":
            if self.is_exist(context):
                print('MMAPs is already existed. Please be sure to clear MMAPs before creating it.')
            else:
                self.__launch(context)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

class MMAP_OT_MMAPsClearer(bpy.types.Operator):
    bl_idname = "object.clear_mmaps"
    bl_label = "MMAPs Clear"
    bl_description = "Clear the MMAPs in scene."

    @classmethod
    def __clear(cls, context):
        '''
        Remove all objects that consist the MMAPs with the name specified in Panel.
        '''

        scene = context.scene

        mirror_name = scene.mirror_name
        glass_name = scene.glass_name 
        parent_name = scene.parent_name
        mmaps.clearMMAPs(mirror_name=mirror_name, glass_name=glass_name, parent_name=parent_name)

    # This function is called when "Clear" button is pressed.
    def invoke(self, context, event):
        op_cls = MMAP_OT_MMAPsLancher
        if context.area.type == "VIEW_3D":
            if op_cls.is_exist(context):
                self.__clear(context)
            else:
                print("MMAPs is not existed.")
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

# -----------------------------------------------------------------------------------
class MMAP_PT_MMAPsManager(bpy.types.Panel):
    '''
    Panel class to manage MMAPs parameters
    '''
    bl_label = 'MMAPs'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MMAPs'
    bl_context = 'objectmode'

    def draw(self, context):
        scene = context.scene 
        # Operator class to create or clear MMAPs object.
        launch_op_cls = MMAP_OT_MMAPsLancher
        clear_op_cls = MMAP_OT_MMAPsClearer

        layout = self.layout
        layout.use_property_split = True 
        layout.use_property_decorate = False 

        # Create properties of MMAPs.  
        layout.label(text="MMAPs parameters")
        col = layout.column()
        col.prop(scene, "mmaps_size", text="Size")
        col.prop(scene, "slit_spacing", text="Slit spacing")
        col.prop(scene, "slit_heightscale", text="Height scale")
        col.prop(scene, "plane_detailing", text="Mirror detailing")
        col.prop(scene, "glass_ior", text="IOR (glass)")
        # Add button to call 'invoke()' in MMAP_OT_MMAPsLauncher
        row = layout.row()
        row.operator(launch_op_cls.bl_idname, text='Launch', icon='PLAY')

        # Create object names to delete.
        layout.label(text="Object names of MMAPs")
        col = layout.column()
        col.prop(scene, "mirror_name", text="Mirror name")
        col.prop(scene, "glass_name", text="Glass name")
        col.prop(scene, "parent_name", text="MMAPs name")
        # Add button to call 'invoke()' in MMAP_OT_MMAPsClearer
        row = layout.row()
        row.operator(clear_op_cls.bl_idname, text='Clear', icon='REMOVE')

def init_props():
    scene = bpy.types.Scene 
    
    scene.mmaps_size = FloatProperty(
        name="MMAPs size",
        min=0.1,
        default=48.8
    )

    scene.slit_spacing = FloatProperty(
        name="Slit spacing of MMAPs",
        min = 0.0001,
        default = 0.05
    )

    scene.slit_heightscale = FloatProperty(
        name="Height scale of mirror to slit spacing.",
        min = 0.1,
        default=2.5
    )

    scene.plane_detailing = FloatProperty(
        name="The number of detailing of mirror.",
        min = 1,
        default=10
    )

    scene.glass_ior = FloatProperty(
        name="Index of reflaction of glass.",
        min = 0.1,
        default=1.52
    )

    scene.mirror_name = StringProperty(
        name="The name of mirror object.",
        default="Mirror"
    )
    scene.glass_name = StringProperty(
        name="The name of glass object.",
        default = "Glass"
    )
    scene.parent_name = StringProperty(
        name="The name of MMAPs",
        default="MMAPs"
    )

def clear_props():
    scene = bpy.types.Scene 
    del scene.mmaps_size
    del scene.slit_spacing
    del scene.slit_heightscale 
    del scene.plane_detailing
    del scene.glass_ior
    del scene.mirror_name
    del scene.glass_name
    del scene.parent_name

classes = [
    MMAP_OT_MMAPsLancher,
    MMAP_OT_MMAPsClearer,
    MMAP_PT_MMAPsManager,
]               

def register():
    init_props()
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    clear_props()

if __name__ == '__main__':
    register()