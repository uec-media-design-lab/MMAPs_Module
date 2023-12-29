import bpy
from . import vcf 
from . import vcf_launcher

class VCF_OT_VCFClearer(bpy.types.Operator):
    bl_idname = "object.clear_vcf"
    bl_label = "VCF Clear"
    bl_description = "Clear the VCF in scene."

    @classmethod
    def __clear(cls, context):
        scene = context.scene

        vcf_louver_name = scene.vcf_louver_name
        vcf_parent_name = scene.vcf_parent_name
        vcf.clearVCF(louver_name=vcf_louver_name, glass_name='Grass', parent_name=vcf_parent_name)

    # This function is called when "Clear" button is pressed.
    def invoke(self, context, event):
        op_cls = vcf_launcher.VCF_OT_VCFLauncher
        if context.area.type == "VIEW_3D":
            if op_cls.is_exist(context):
                self.__clear(context)
            else:
                print("VCF is not existed.")
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
        
class VCF_OT_VCFDISClearer(bpy.types.Operator):
    bl_idname = "object.clear_vcfdis"
    bl_label = "VCFDIS Clear"
    bl_description = "Clear the VCFDIS in scene."

    @classmethod
    def __clear(cls, context):
        scene = context.scene

        vcfdis_louver_name = scene.vcfdis_louver_name
        vcfdis_parent_name = scene.vcfdis_parent_name
        vcf.clearVCF(louver_name=vcfdis_louver_name, glass_name='Grass', parent_name=vcfdis_parent_name)

    # This function is called when "Clear" button is pressed.
    def invoke(self, context, event):
        op_cls = vcf_launcher.VCF_OT_VCFDISLauncher
        if context.area.type == "VIEW_3D":
            if op_cls.is_exist(context):
                self.__clear(context)
            else:
                print("VCF is not existed.")
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
