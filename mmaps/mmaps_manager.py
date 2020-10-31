import bpy 
import math 
from . import mmaps_launcher 
from . import mmaps_clearer

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
        launch_op_cls = mmaps_launcher.MMAP_OT_MMAPsLancher
        clear_op_cls = mmaps_clearer.MMAP_OT_MMAPsClearer

        layout = self.layout
        layout.use_property_split = True 
        layout.use_property_decorate = False 

        # Create properties of MMAPs.  
        layout.label(text="MMAPs parameters")
        col = layout.column()
        col.prop(scene, "mmaps_size", text="Size")
        col.prop(scene, "mmaps_slit_spacing", text="Slit spacing")
        col.prop(scene, "mmaps_slit_heightscale", text="Height scale")
        col.prop(scene, "mmaps_detailing", text="Mirror detailing")
        col.prop(scene, "mmaps_glass_ior", text="IOR (glass)")
        # Add button to call 'invoke()' in MMAP_OT_MMAPsLauncher
        row = layout.row()
        row.operator(launch_op_cls.bl_idname, text='Launch', icon='PLAY')

        # Create object names to delete.
        layout.label(text="Object names of MMAPs")
        col = layout.column()
        col.prop(scene, "mmaps_mirror_name", text="Mirror name")
        col.prop(scene, "mmaps_glass_name", text="Glass name")
        col.prop(scene, "mmaps_parent_name", text="MMAPs name")
        # Add button to call 'invoke()' in MMAP_OT_MMAPsClearer
        row = layout.row()
        row.operator(clear_op_cls.bl_idname, text='Clear', icon='REMOVE')