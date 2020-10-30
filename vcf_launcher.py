import mmaps 
import vcf
import bpy
import myutil
import math
from bpy.props import *

bl_info = {
    "name": "VCF Launcher",
    "author": "Ayami Hoshi",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "This addon is to create VCF in scene.",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

class VCF_OT_VCFLancher(bpy.types.Operator):
    bl_idname = "object.launch_vcf"
    bl_label = "VCF Launch"
    bl_description = "Launch the VCF in scene."

    @classmethod
    def __launch(cls, context):
        scene = context.scene
        print("Start creating the VCF...")

        digit_func = myutil.getRoundDigit

        mmaps_size = round(scene.vcf_size, digit_func(scene.vcf_size))
        display_size = round(scene.vcf1_size, digit_func(scene.vcf1_size))
        spacing = round(scene.vcf_slit_spacing, digit_func(scene.vcf_slit_spacing)) 
        view_angle = round(scene.view_angle, 2)
        mbta = round(scene.mbta, 2)
        #ior = round(scene.glass_ior, 2)
        #mmaps.createDetailedMMAPs(size=size, spacing=spacing, detailing=detailing, height_scale=height_scale, ior=ior)
        vcf.createVCF(size=mmaps_size, spacing=spacing, view_angle = view_angle,max_beam_transmission_angle = mbta, overwrite=False)
        vcf.createVCF(size=display_size, spacing=spacing, view_angle = view_angle,max_beam_transmission_angle = mbta, overwrite=False)
        
    @classmethod 
    def is_exist(cls, context):
        scene = context.scene
        vcf_parent_name = scene.vcf_parent_name
        return bpy.data.objects.get(vcf_parent_name) is not None

    # This function is called when "Launch" button is pressed.
    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":
            if self.is_exist(context):
                print('VCF is already existed. Please be sure to clear VCF before creating it.')
            else:
                self.__launch(context)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

class VCF_OT_VCFClearer(bpy.types.Operator):
    bl_idname = "object.clear_vcf"
    bl_label = "VCF Clear"
    bl_description = "Clear the VCF in scene."

    @classmethod
    def __clear(cls, context):
        scene = context.scene

        vcf_louver_name = scene.vcf_louver_name
        vcf_glass_name = scene.vcf_glass_name 
        vcf_parent_name = scene.vcf_parent_name
        vcf.clearVCF(louver_name=vcf_louver_name, glass_name=vcf_glass_name, parent_name=vcf_parent_name)

    # This function is called when "Clear" button is pressed.
    def invoke(self, context, event):
        op_cls = VCF_OT_VCFLancher
        if context.area.type == "VIEW_3D":
            if op_cls.is_exist(context):
                self.__clear(context)
            else:
                print("VCF is not existed.")
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

class VCF_PT_VCFManager(bpy.types.Panel):
    bl_label = 'VCF'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VCF'
    bl_context = 'objectmode'

    def draw(self, context):
        scene = context.scene 
        launch_op_cls = VCF_OT_VCFLancher
        clear_op_cls = VCF_OT_VCFClearer

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

def init_props():
    scene = bpy.types.Scene 
    
    scene.vcf_size = FloatProperty(
        name="VCF size",
        min=0.1,
        default=48.8
    )
    
    scene.vcf1_size = FloatProperty(
        name="VCF1 size",
        min=0.1,
        default=17.5
    )

    scene.vcf_slit_spacing = FloatProperty(
        name="Slit spacing of VCF",
        min = 0.0001,
        default = 0.0132
    )

    scene.view_angle = FloatProperty(
        name="view_angle.",
        min = 1,
        default=60
    )

    scene.mbta = FloatProperty(
        name="mbta.",
        min = 0,
        default=25
    )
    
    '''
    scene.glass_ior = FloatProperty(
        name="Index of reflaction of glass.",
        min = 0.1,
        default=1.52
    )
    '''

    scene.vcf_louver_name = StringProperty(
        name="The name of louver object.",
        default="Louver"
    )
    scene.vcf_glass_name = StringProperty(
        name="The name of glass object.",
        default = "Glass"
    )
    scene.vcf_parent_name = StringProperty(
        name="The name of VCF",
        default="VCF"
    )

def clear_props():
    scene = bpy.types.Scene 
    del scene.vcf_size
    del scene.vcf1_size
    del scene.vcf_slit_spacing
    del scene.view_angle
    del scene.mbta
    #del scene.glass_ior
    del scene.vcf_louver_name
    del scene.vcf_glass_name
    del scene.vcf_parent_name

classes = [
    VCF_OT_VCFLancher,
    VCF_OT_VCFClearer,
    VCF_PT_VCFManager,
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