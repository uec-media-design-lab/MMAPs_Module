import bpy 
from . import myutil 
from . import vcf

class VCF_OT_VCFLauncher(bpy.types.Operator):
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
        vcf.createVCF(size=mmaps_size, spacing=spacing, view_angle = view_angle,max_beam_transmission_angle = mbta)
        vcf.createVCF(size=display_size, spacing=spacing, view_angle = view_angle,max_beam_transmission_angle = mbta)
        
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