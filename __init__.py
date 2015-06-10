bl_info = {
    "name": "HDR 2 RGBM",
    "author": "Yusuf Umar",
    "version": (0, 0, 0),
    "blender": (2, 74, 0),
    "location": "Anywhere",
    "description": "Encode (and decode) HDR image into RGBM format",
    "wiki_url": "http://twitter.com/ucupumar",
    "category": "Material",
}

import bpy, math

# function to clamp float
def saturate(num, floats=True):
    if num < 0:
        num = 0
    elif num > (1 if floats else 255):
        num = (1 if floats else 255)
    return num 

class Convert2RGBM(bpy.types.Operator):
    """Nice Useful Tooltip"""
    bl_idname = "image.convert_to_rgbm"
    bl_label = "Convert HDR to RGBM"
    bl_description = "Convert HDR/float image to RGBM format"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sima = context.space_data
        # Image
        ima = sima.image
        ima_name = ima.name

        # Checking if image is float
        if not ima.is_float:
            self.report({'ERROR'}, "Need float/HDR image input.")
            return {'CANCELLED'}  
        
        # Removing .exr or .hdr prefix
        if ima_name[-4:] == '.exr' or ima_name[-4:] == '.hdr':
            ima_name = ima_name[:-4]

        target_ima = bpy.data.images.get(ima_name + '_RGBM')
        if not target_ima:
            target_ima = bpy.data.images.new(
                    name = ima_name + '_RGBM',
                    width = ima.size[0],
                    height = ima.size[1],
                    alpha = True,
                    float_buffer = False
                    )
        
        num_pixels = len(ima.pixels)
        result_pixel = list(ima.pixels)
        
        # Encode to RGBM
        for i in range(0,num_pixels,4):
            for j in range(3):
                result_pixel[i+j] *= 1.0 / 8.0
            result_pixel[i+3] = saturate(max(result_pixel[i], result_pixel[i+1], result_pixel[i+2], 1e-6))
            result_pixel[i+3] = math.ceil(result_pixel[i+3] * 255.0) / 255.0;
            for j in range(3):
                result_pixel[i+j] /= result_pixel[i+3]
        
        target_ima.pixels = result_pixel
        
        sima.image = target_ima

        #print(ima)
        return {'FINISHED'}

class ConvertToRGBMPanel(bpy.types.Panel):
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "TOOLS"
    #bl_context = "objectmode"
    bl_label = "HDR to RGBM"
    bl_category = "RGBM"

    def draw(self, context):
        c = self.layout.column()
        c.operator("image.convert_to_rgbm")

def register():
    bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
