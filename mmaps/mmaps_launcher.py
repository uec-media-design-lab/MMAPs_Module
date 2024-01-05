import bpy

from . import mmaps, myutil


class MMAP_OT_MMAPsLancher(bpy.types.Operator):
    bl_idname = "object.launch_mmaps"
    bl_label = "MMAPs Launch"
    bl_description = "Launch the MMAPs in scene."

    @classmethod
    def __launch(cls, context):
        """
        Create MMAPs object include mirrors and glass with specified parameters.
        """
        scene = context.scene
        print("Start creating the MMAPs...")

        digit_func = myutil.getRoundDigit

        size = round(scene.mmaps_size, digit_func(scene.mmaps_size))
        spacing = round(scene.mmaps_slit_spacing, digit_func(scene.mmaps_slit_spacing))
        height_scale = round(scene.mmaps_slit_heightscale, 2)
        mmaps_detailing = int(scene.mmaps_detailing)
        ior = round(scene.mmaps_glass_ior, 2)
        mmaps.createMMAPs(
            size=size,
            spacing=spacing,
            detailing=mmaps_detailing,
            height_scale=height_scale,
            ior=ior,
        )

    @classmethod
    def is_exist(cls, context):
        """
        Check if mmaps is existed
        """
        scene = context.scene
        mmaps_parent_name = scene.mmaps_parent_name
        return bpy.data.objects.get(mmaps_parent_name) is not None

    # This function is called when "Launch" button is pressed.
    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":
            if self.is_exist(context):
                print(
                    "MMAPs is already existed. Please be sure to clear MMAPs before creating it."
                )
            else:
                self.__launch(context)
            return {"FINISHED"}
        else:
            return {"CANCELLED"}


class MMAP_OT_CustomMMAPLauncher(bpy.types.Operator):
    bl_idname = "object.launch_custom_mmap"
    bl_label = "Custom MMAP Launch"
    bl_description = "Launch the custom MMAP in scene."

    @classmethod
    def __launch(cls, context):
        """
        Create custom MMAP object include mirrors and glass with specified parameters.
        """
        scene = context.scene
        print("Start creating the custom MMAP...")

        digit_func = myutil.getRoundDigit

        size = round(scene.custom_mmap_size, digit_func(scene.custom_mmap_size))
        spacing = round(
            scene.custom_mmap_spacing, digit_func(scene.custom_mmap_spacing)
        )

        height1 = round(scene.custom_mmap_height_scale_layer1, 2)
        height2 = round(scene.custom_mmap_height_scale_layer2, 2)

        degree1 = scene.custom_mmap_degree_layer1
        degree2 = scene.custom_mmap_degree_layer2

        ior1 = round(scene.custom_mmap_ior_layer1, 2)
        ior2 = round(scene.custom_mmap_ior_layer2, 2)

        layer1 = mmaps.LayerProperty(height1, ior1, degree1)
        layer2 = mmaps.LayerProperty(height2, ior2, degree2)

        detailing = scene.custom_mmap_detailing
        mmaps.createCustomMMAP(
            size=size,
            spacing=spacing,
            detailing=detailing,
            layer1=layer1,
            layer2=layer2,
            isGlass=True,
        )

    @classmethod
    def is_exist(cls, context):
        """
        Check if mmaps is existed
        """
        scene = context.scene
        parent_name = scene.custom_mmap_parent_name
        return bpy.data.objects.get(parent_name) is not None

    # This function is called when "Launch" button is pressed.
    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":
            if self.is_exist(context):
                print(
                    "MMAPs is already existed. Please be sure to clear MMAPs before creating it."
                )
            else:
                self.__launch(context)
            return {"FINISHED"}
        else:
            return {"CANCELLED"}
