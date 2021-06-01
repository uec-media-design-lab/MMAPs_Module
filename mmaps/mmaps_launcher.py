import bpy 
from . import mmaps 
from . import myutil 

class MMAP_OT_MMAPsLancher(bpy.types.Operator):
    bl_idname = "object.launch_mmaps"
    bl_label = "MMAPs Launch"
    bl_description = "Launch the MMAPs in scene."

    @classmethod
    def __launch(cls, context):
        '''
        Create MMAPs object include mirrors and glass with specified parameters. 
        '''
        scene = context.scene
        print("Start creating the MMAPs...")

        digit_func = myutil.getRoundDigit
        
        size = round(scene.mmaps_size, digit_func(scene.mmaps_size))
        spacing = round(scene.mmaps_slit_spacing, digit_func(scene.mmaps_slit_spacing)) 
        height_scale = round(scene.mmaps_slit_heightscale, 2)
        mmaps_detailing = int(scene.mmaps_detailing)
        ior = round(scene.mmaps_glass_ior, 2)
        mmaps.createMMAPs(size=size, spacing=spacing, detailing=mmaps_detailing, height_scale=height_scale, ior=ior)

    @classmethod 
    def is_exist(cls, context):
        '''
        Check if mmaps is existed
        '''
        scene = context.scene
        mmaps_parent_name = scene.mmaps_parent_name
        return bpy.data.objects.get(mmaps_parent_name) is not None

    # This function is called when "Launch" button is pressed.
    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":
            if self.is_exist(context):
                print('MMAPs is already existed. Please be sure to clear MMAPs before creating it.')
            else:
                self.__launch(context)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}