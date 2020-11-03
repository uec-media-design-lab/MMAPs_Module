bl_info = {
    "name": "VCF Launcher",
    "author": "Ayami Hoshi",
    "version": (2, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "This addon is to create VCF in scene.",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# Load modules
if "bpy" in locals():
    import imp 
    imp.reload(vcf)
    imp.reload(myutil)
    imp.reload(vcf_launcher)
    imp.reload(vcf_clearer)
    imp.reload(vcf_manager)
else:
    from . import vcf
    from . import myutil 
    from . import vcf_launcher
    from . import vcf_clearer
    from . import vcf_manager

import bpy 
from bpy.props import *

classes = [
    vcf_launcher.VCF_OT_VCFLauncher,
    vcf_launcher.VCF_OT_VCFDISLauncher,
    vcf_clearer.VCF_OT_VCFClearer,
    vcf_clearer.VCF_OT_VCFDISClearer,
    vcf_manager.VCF_PT_VCFManager
]

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

    scene.vcfdis_slit_spacing = FloatProperty(
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

    scene.view_angle_dis = FloatProperty(
        name="view_angle.",
        min = 1,
        default=60
    )

    scene.mbta_dis = FloatProperty(
        name="mbta.",
        min = 0,
        default=25
    )

    scene.vcf_louver_name = StringProperty(
        name="The name of louver object.",
        default="Louver"
    )
    scene.vcf_parent_name = StringProperty(
        name="The name of VCF",
        default="MMAPsVCF"
    )
    
    scene.vcfdis_louver_name = StringProperty(
        name="The name of louver object.",
        default="Louver"
    )
    scene.vcfdis_parent_name = StringProperty(
        name="The name of VCFDIS",
        default="DisplayVCF"
    )

def clear_props():
    scene = bpy.types.Scene 
    del scene.vcf_size
    del scene.vcf1_size
    del scene.vcf_slit_spacing
    del scene.vcfdis_slit_spacing
    del scene.view_angle
    del scene.mbta
    del scene.view_angle_dis
    del scene.mbta_dis
    del scene.vcf_louver_name
    del scene.vcf_parent_name
    del scene.vcfdis_louver_name
    del scene.vcfdis_parent_name

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