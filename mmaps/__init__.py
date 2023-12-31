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
    "category": "Object",
}

# Load modules
if "bpy" in locals():
    import imp

    imp.reload(mmaps)
    imp.reload(myutil)
    imp.reload(mmaps_launcher)
    imp.reload(mmaps_clearer)
    imp.reload(mmaps_manager)
else:
    from . import mmaps
    from . import myutil
    from . import mmaps_launcher
    from . import mmaps_clearer
    from . import mmaps_manager

import bpy
from bpy.props import *

classes = [
    mmaps_launcher.MMAP_OT_MMAPsLancher,
    mmaps_clearer.MMAP_OT_MMAPsClearer,
    mmaps_manager.MMAP_PT_MMAPsManager,
    mmaps_launcher.MMAP_OT_CustomMMAPLauncher,
    mmaps_clearer.MMAP_OT_CustomMMAPClearer,
    mmaps_manager.MMAP_PT_CustomMMAPManager,
]


def init_props():
    scene = bpy.types.Scene

    scene.mmaps_size = FloatProperty(name="MMAPs size", min=0.1, default=48.8)

    scene.mmaps_slit_spacing = FloatProperty(
        name="Slit spacing of MMAPs", min=0.0001, default=0.05
    )

    scene.mmaps_slit_heightscale = FloatProperty(
        name="Height scale of mirror to slit spacing.", min=0.1, default=2.5
    )

    scene.mmaps_detailing = IntProperty(
        name="The number of detailing of mirror.", min=1, default=10
    )

    scene.mmaps_glass_ior = FloatProperty(
        name="Index of refraction of glass.", min=0.1, default=1.52
    )

    scene.mmaps_mirror_name = StringProperty(
        name="The name of mirror object.", default="Mirror"
    )
    scene.mmaps_glass_name = StringProperty(
        name="The name of glass object.", default="Glass"
    )
    scene.mmaps_parent_name = StringProperty(name="The name of MMAPs", default="MMAPs")

    # Custom MMAP
    scene.custom_mmap_size = FloatProperty(
        name="Custom MMAP size", min=0.1, default=48.8
    )

    scene.custom_mmap_spacing = FloatProperty(
        name="Slit spacing of custom MMAP", min=0.0001, default=0.05
    )

    # Layer 1
    scene.custom_mmap_height_scale_layer1 = FloatProperty(
        name="Height scale of mirror to slit spacing in layer 1", min=0.1, default=2.5
    )
    scene.custom_mmap_degree_layer1 = FloatProperty(
        name="Degree of mirror in layer 1", min=0.0, default=0.0
    )
    scene.custom_mmap_ior_layer1 = FloatProperty(
        name="Index of refraction in layer 1", min=1.0, default=1.52
    )
    # Layer 2
    scene.custom_mmap_height_scale_layer2 = FloatProperty(
        name="Height scale of mirror to slit spacing in layer 2", min=0.1, default=2.5
    )
    scene.custom_mmap_degree_layer2 = FloatProperty(
        name="Degree of mirror in layer 2", min=0.0, default=0.0
    )
    scene.custom_mmap_ior_layer2 = FloatProperty(
        name="Index of refraction in layer 2", min=1.0, default=1.52
    )

    scene.custom_mmap_detailing = IntProperty(
        name="The number of detailing of mirror.", min=1, default=10
    )

    scene.custom_mmap_mirror_name = StringProperty(
        name="The name of mirror object.", default="Mirror_Layer"
    )
    scene.custom_mmap_glass_name = StringProperty(
        name="The name of glass object.", default="Glass_Layer"
    )
    scene.custom_mmap_parent_name = StringProperty(
        name="The name of MMAPs", default="CustomMMAP"
    )


def clear_props():
    scene = bpy.types.Scene
    del scene.mmaps_size
    del scene.mmaps_slit_spacing
    del scene.mmaps_slit_heightscale
    del scene.mmaps_detailing
    del scene.mmaps_glass_ior
    del scene.mmaps_mirror_name
    del scene.mmaps_glass_name
    del scene.mmaps_parent_name


def register():
    init_props()
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    clear_props()


if __name__ == "__main__":
    register()
