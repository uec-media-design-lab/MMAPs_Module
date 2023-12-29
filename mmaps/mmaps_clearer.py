import bpy

from . import mmaps, mmaps_launcher


class MMAP_OT_MMAPsClearer(bpy.types.Operator):
    bl_idname = "object.clear_mmaps"
    bl_label = "MMAPs Clear"
    bl_description = "Clear the MMAPs in scene."

    @classmethod
    def __clear(cls, context):
        """
        Remove all objects that consist the MMAPs with the name specified in Panel.
        """

        scene = context.scene

        mmaps_mirror_name = scene.mmaps_mirror_name
        mmaps_glass_name = scene.mmaps_glass_name
        mmaps_parent_name = scene.mmaps_parent_name
        mmaps.clearMMAPs(
            mirror_name=mmaps_mirror_name,
            glass_name=mmaps_glass_name,
            parent_name=mmaps_parent_name,
        )

    # This function is called when "Clear" button is pressed.
    def invoke(self, context, event):
        op_cls = mmaps_launcher.MMAP_OT_MMAPsLancher
        if context.area.type == "VIEW_3D":
            if op_cls.is_exist(context):
                self.__clear(context)
            else:
                print("MMAPs is not existed.")
            return {"FINISHED"}
        else:
            return {"CANCELLED"}


class MMAP_OT_CustomMMAPClearer(bpy.types.Operator):
    bl_idname = "object.clear_custom_mmap"
    bl_label = "Custom MMAP Clear"
    bl_description = "Clear the custom MMAP in scene."

    @classmethod
    def __clear(cls, context):
        """
        Remove all objects that consist the custom MMAP with the name specified in Panel.
        """

        scene = context.scene

        mmaps_mirror_name = scene.mmaps_mirror_name
        mmaps_glass_name = scene.mmaps_glass_name
        mmaps_parent_name = scene.mmaps_parent_name
        mmaps.clearCustomMMAP()

    # This function is called when "Clear" button is pressed.
    def invoke(self, context, event):
        op_cls = mmaps_launcher.MMAP_OT_CustomMMAPLauncher
        if context.area.type == "VIEW_3D":
            if op_cls.is_exist(context):
                self.__clear(context)
            else:
                print("Custom MMAP is not existed.")
            return {"FINISHED"}
        else:
            return {"CANCELLED"}
