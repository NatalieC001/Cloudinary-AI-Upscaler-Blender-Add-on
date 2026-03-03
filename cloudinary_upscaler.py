
# Depricated for  the newer more secure Cloudinary_SecureInstaller.py loaded through plugins interface
"""

bl_info = {
    "name": "Cloudinary AI Upscaler",
    "author": "You",
    "version": (0, 5, 1),
    "blender": (3, 0, 0),
    "location": "Image Editor > N-panel > Cloudinary",
    "description": "Upload image to Cloudinary via Drag & Drop or Picker and upscale with AI",
    "category": "Image",
}

import bpy
import os
import subprocess
import sys
import urllib.request

# ---------------------------------------------------------------------------
# Ensure cloudinary is installed
# ---------------------------------------------------------------------------
def ensure_cloudinary_installed():
    try:
        import cloudinary
        return True
    except ImportError:
        python_exe = sys.executable
        try:
            subprocess.check_call([python_exe, "-m", "pip", "install", "cloudinary"])
            import cloudinary  # re-import after install
            return True
        except Exception as e:
            print(f"Failed to install cloudinary: {e}")
            return False

_CLOUDINARY_AVAILABLE = ensure_cloudinary_installed()

if _CLOUDINARY_AVAILABLE:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    from cloudinary.utils import cloudinary_url
else:
    cloudinary = None

# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------
class CloudinarySettings(bpy.types.PropertyGroup):
    cloud_name: bpy.props.StringProperty(name="Cloud Name", default="")
    api_key: bpy.props.StringProperty(name="API Key", default="")
    api_secret: bpy.props.StringProperty(name="API Secret", default="", subtype='PASSWORD')
    show_credentials: bpy.props.BoolProperty(name="Show Credentials", default=False)
   
    output_format: bpy.props.EnumProperty(
        name="Format",
        description="Format to download the upscaled image",
        items=[
            ('png', "PNG", "Download as PNG"),
            ('jpg', "JPG", "Download as JPG"),
        ],
        default='png'
    )
    
    target_width: bpy.props.IntProperty(
        name="Target Width",
        description="Desired output width after upscale (px) - 0 = auto",
        default=2048,
        min=0,
        soft_max=4096
    )
    
    drop_target: bpy.props.StringProperty(
        name="Image Path",
        description="Drag and drop an image file here from your computer",
        default="",
        subtype='FILE_PATH'
    )

# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------
class CLOUDINARY_OT_clear_creds(bpy.types.Operator):
    """Wipe all credentials to start fresh"""
    bl_idname = "image.cloudinary_clear_creds"
    bl_label = "Clear All Fields"
    
    def execute(self, context):
        s = context.scene.cloudinary_tool_settings
        s.cloud_name = ""
        s.api_key = ""
        s.api_secret = ""
        s.drop_target = ""
        return {'FINISHED'}

class CLOUDINARY_OT_test_connection(bpy.types.Operator):
    """Verify if the Cloudinary credentials are correct"""
    bl_idname = "image.cloudinary_test_connection"
    bl_label = "Test Connection"
    
    def execute(self, context):
        s = context.scene.cloudinary_tool_settings
        c_name = s.cloud_name.strip()
        a_key = s.api_key.strip()
        a_secret = s.api_secret.strip()
        
        if not all([c_name, a_key, a_secret]):
            self.report({'ERROR'}, "Missing credentials.")
            return {'CANCELLED'}
        
        try:
            cloudinary.config(cloud_name=c_name, api_key=a_key, api_secret=a_secret, secure=True)
            cloudinary.api.ping()
            self.report({'INFO'}, "Connection Successful!")
        except Exception as e:
            self.report({'ERROR'}, f"Connection Failed: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}

class CLOUDINARY_OT_process_image(bpy.types.Operator):
    """Uploads the specified image path to Cloudinary and upscales it"""
    bl_idname = "image.cloudinary_process_image"
    bl_label = "Upscale This Image"
   
    path_to_upload: bpy.props.StringProperty()
    
    def execute(self, context):
        if not _CLOUDINARY_AVAILABLE or cloudinary is None:
            self.report({'ERROR'}, "Cloudinary library not available. Check console for pip errors.")
            return {'CANCELLED'}
        
        s = context.scene.cloudinary_tool_settings
        c_name = s.cloud_name.strip()
        a_key = s.api_key.strip()
        a_secret = s.api_secret.strip()
        
        if not all([c_name, a_key, a_secret]):
            self.report({'ERROR'}, "Missing or invalid credentials.")
            return {'CANCELLED'}
        
        cloudinary.config(cloud_name=c_name, api_key=a_key, api_secret=a_secret, secure=True)
        
        abs_path = bpy.path.abspath(self.path_to_upload)
        if not os.path.exists(abs_path):
            self.report({'ERROR'}, f"File not found: {abs_path}")
            return {'CANCELLED'}
        
        try:
            self.report({'INFO'}, f"Uploading {os.path.basename(abs_path)}...")
            upload_result = cloudinary.uploader.upload(abs_path)
            public_id = upload_result["public_id"]
            
            # Build transformation chain
            trans = []
            
            # Apply AI super-resolution upscale (adds detail, ~4x enlargement)
            # This is the core "AI upscaler" feature
            trans.append({"effect": "upscale"})
            
            # Respect user setting exactly:
            # - If >0 → enforce final width (scale preserves aspect ratio)
            # - If ==0 → no resize constraint (let upscale run free, avoid conflicts)
            target_w = s.target_width
            if target_w > 0:
                trans.append({"width": target_w, "crop": "scale"})
            
            # Final quality boost
            trans.append({"quality": "auto:best"})
            
            # Generate secure delivery URL
            upscaled_url, _ = cloudinary_url(
                public_id,
                transformation=trans,
                fetch_format=s.output_format,
                secure=True
            )
            
            # Download the file locally
            filename = f"{public_id.replace('/', '_')}_upscaled.{s.output_format}"
            save_path = os.path.join(os.path.dirname(abs_path), filename)
           
            self.report({'INFO'}, f"Downloading upscaled image from: {upscaled_url}")
            urllib.request.urlretrieve(upscaled_url, save_path)
            
            # Load into Blender
            new_img = bpy.data.images.load(save_path, check_existing=True)
           
            # Switch image editor to new image
            for area in context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    area.spaces.active.image = new_img
                    break
            
            bpy.context.window_manager.clipboard = upscaled_url
            self.report({'INFO'}, f"Upscaled image saved to: {save_path}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Cloudinary error: {str(e)}")
            print(f"Full error: {e.__class__.__name__}: {e}")
            return {'CANCELLED'}

# ---------------------------------------------------------------------------
# Panel
# ---------------------------------------------------------------------------
class CLOUDINARY_PT_panel(bpy.types.Panel):
    bl_label = "Cloudinary AI Tools"
    bl_idname = "CLOUDINARY_PT_panel"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Cloudinary"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.cloudinary_tool_settings
        
        # API Credentials Section
        box = layout.box()
        header = box.row(align=True)
        header.label(text="API Credentials", icon='LOCKED' if not settings.show_credentials else 'UNLOCKED')
        header.prop(settings, "show_credentials", text="", icon='HIDE_OFF' if settings.show_credentials else 'HIDE_ON', emboss=False, toggle=True)
        
        if settings.show_credentials:
            box.prop(settings, "cloud_name")
            box.prop(settings, "api_key")
            box.prop(settings, "api_secret")
        else:
            for label, val in [("Cloud Name", settings.cloud_name),
                              ("API Key", settings.api_key),
                              ("API Secret", settings.api_secret)]:
                row = box.row()
                row.label(text=label + ":")
                row.label(text="●●●●●●●●" if val else "(empty)")
        
        row = box.row(align=True)
        row.operator("image.cloudinary_test_connection", icon='WORLD')
        row.operator("image.cloudinary_clear_creds", icon='TRASH', text="")
        
        layout.separator()
        
        # Settings
        layout.prop(settings, "target_width")
        layout.prop(settings, "output_format")
        
        layout.separator()
        
        # Drag and Drop Section
        col = layout.column(align=True)
        col.label(text="Drag & Drop Image Below:", icon='IMAGE_DATA')
        col.prop(settings, "drop_target", text="")
       
        if settings.drop_target:
            filename = os.path.basename(settings.drop_target)
            row = layout.row()
            op = row.operator("image.cloudinary_process_image", text=f"Upscale: {filename}", icon='EXPORT')
            op.path_to_upload = settings.drop_target
        
        layout.separator()
       
        # Active Image Section
        if context.space_data.image:
            img = context.space_data.image
            if img.filepath:
                col = layout.column()
                col.label(text="Or use Active Editor Image:")
                op_active = col.operator("image.cloudinary_process_image", text=f"Upscale {img.name}", icon='IMAGE_EDITOR')
                op_active.path_to_upload = img.filepath

# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------
classes = (
    CloudinarySettings,
    CLOUDINARY_OT_clear_creds,
    CLOUDINARY_OT_test_connection,
    CLOUDINARY_OT_process_image,
    CLOUDINARY_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cloudinary_tool_settings = bpy.props.PointerProperty(type=CloudinarySettings)

def unregister():
    del bpy.types.Scene.cloudinary_tool_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

"""
