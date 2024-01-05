import bpy

from . import mmaps_clearer, mmaps_launcher


class MMAP_PT_MMAPsManager(bpy.types.Panel):
    """
    Panel class to manage MMAPs parameters
    """

    bl_label = "MMAPs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMAPs"
    bl_context = "objectmode"

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
        row.operator(launch_op_cls.bl_idname, text="Launch", icon="PLAY")

        # Create object names to delete.
        layout.label(text="Object names of MMAPs")
        col = layout.column()
        col.prop(scene, "mmaps_mirror_name", text="Mirror name")
        col.prop(scene, "mmaps_glass_name", text="Glass name")
        col.prop(scene, "mmaps_parent_name", text="MMAPs name")
        # Add button to call 'invoke()' in MMAP_OT_MMAPsClearer
        row = layout.row()
        row.operator(clear_op_cls.bl_idname, text="Clear", icon="REMOVE")


class MMAP_PT_CustomMMAPManager(bpy.types.Panel):
    """
    Panel class to manage custom MMAP parameters
    """

    bl_label = "Custom MMAP"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Custom MMAP"
    bl_context = "objectmode"

    def draw(self, context):
        scene = context.scene
        # Operator class to create/clear custom MMAP.
        launch_op_cls = mmaps_launcher.MMAP_OT_CustomMMAPLauncher
        clear_op_cls = mmaps_clearer.MMAP_OT_CustomMMAPClearer

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # Create properties of custom MMAP
        layout.use_property_split = True
        layout.use_property_decorate = False

        # Create properties of MMAPs.
        layout.label(text="Custom MMAP parameters")
        col = layout.column()
        col.prop(scene, "custom_mmap_size", text="Size")
        col.prop(scene, "custom_mmap_spacing", text="Slit spacing")
        # TODO: Add grouping of each layer properties
        col.label(text="Layer 1")
        l1_box = col.box()
        l1_box.prop(scene, "custom_mmap_height_scale_layer1", text="Height scale")
        l1_box.prop(scene, "custom_mmap_degree_layer1", text="Degree")
        l1_box.prop(scene, "custom_mmap_ior_layer1", text="IOR")
        col.label(text="Layer 2")
        l2_box = col.box()
        l2_box.prop(scene, "custom_mmap_height_scale_layer2", text="Height scale")
        l2_box.prop(scene, "custom_mmap_degree_layer2", text="Degree")
        l2_box.prop(scene, "custom_mmap_ior_layer2", text="IOR")
        # Add button to call 'invoke()' in MMAP_OT_CustomMMAPLauncher
        row = layout.row()
        row.operator(launch_op_cls.bl_idname, text="Launch", icon="PLAY")

        # Create object names to delete.
        layout.label(text="Object names of custom MMAP")
        col = layout.column()
        col.prop(scene, "custom_mmap_mirror_name", text="Mirror name")
        col.prop(scene, "custom_mmap_glass_name", text="Glass name")
        col.prop(scene, "custom_mmap_parent_name", text="Custom MMAP name")
        # Add button to call 'invoke()' in MMAP_OT_CustomMMAPClearer
        row = layout.row()
        row.operator(clear_op_cls.bl_idname, text="Clear", icon="REMOVE")
