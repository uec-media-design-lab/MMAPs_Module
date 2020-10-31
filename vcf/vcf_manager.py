import bpy 
from . import vcf_launcher 
from . import vcf_clearer

class VCF_PT_VCFManager(bpy.types.Panel):
    bl_label = 'VCF'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VCF'
    bl_context = 'objectmode'

    def draw(self, context):
        scene = context.scene 
        launch_op_cls = vcf_launcher.VCF_OT_VCFLauncher
        clear_op_cls = vcf_clearer.VCF_OT_VCFClearer

        layout = self.layout
        layout.use_property_split = True 
        layout.use_property_decorate = False 

        # Create properties of MMAPs.  
        layout.label(text="VCF parameters")
        col = layout.column()
        col.prop(scene, "vcf_size", text="MMAPs size")
        col.prop(scene, "vcf1_size", text="Display size")
        col.prop(scene, "vcf_slit_spacing", text="Slit spacing")
        col.prop(scene, "view_angle", text="View angle")
        col.prop(scene, "mbta", text="Mbta")
        #col.prop(scene, "glass_ior", text="IOR (glass)")
        row = layout.row()
        row.operator(launch_op_cls.bl_idname, text='Launch', icon='PLAY')

        # Create object names to delete.
        layout.label(text="Object names of VCF")
        col = layout.column()
        col.prop(scene, "vcf_louver_name", text="Louver name")
        col.prop(scene, "vcf_glass_name", text="Glass name")
        col.prop(scene, "vcf_parent_name", text="VCF name")
        row = layout.row()
        row.operator(clear_op_cls.bl_idname, text='Clear', icon='REMOVE')