bl_info = {
    "name": "Shift 2 .meb car mesh",
    "blender": (2, 80, 0),
    "category": "Import",
}

import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

class importMEB(Operator, ImportHelper):
    """Import from Shift 2 mesh format (.meb)"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "import_scene.meb"
    bl_label = "Import Shift 2 (*.meb)"
    bl_options = {'UNDO'}  # Enable undo for the operator.
    
    filename_ext = '.meb'
    filter_glob = StringProperty(
        default="*.meb", 
        options={'HIDDEN'}
    )
    
    importall = BoolProperty(
        name="Import entire folder", 
        description="Import all meshes in this folder", 
        default=False)
    
    rotate = BoolProperty(
        name="Rotate 90 X", 
        description="Rotates 90 degrees around X axis", 
        default=True)
    
    ignore_dmg = BoolProperty(
        name="Ignore damage parts", 
        description="Skip damage parts if in selected folder", 
        default=True)
    
    hide_lodb = BoolProperty(
        name="Hide imported LODB", 
        description="Hide imported LODB parts", 
        default=True)

    hide_lodc = BoolProperty(
        name="Hide imported LODC", 
        description="Hide imported LODC parts", 
        default=True)
    
    
    def draw(self, context):
        layout = self.layout
        sub = layout.row()
        sub.prop(self, "importall")
        sub = layout.row()
        sub.prop(self, "rotate")
        sub = layout.row()
        sub.prop(self, "ignore_dmg")
        sub = layout.row()
        sub.prop(self, "hide_lodb")
        sub = layout.row()
        sub.prop(self, "hide_lodc")
    

    def execute(self, context):        # execute() is called when running the operator.
        from . import import_meb

        import_meb.load(self.filepath, self.importall, self.rotate, self.ignore_dmg, self.hide_lodb, self.hide_lodc)

        return {'FINISHED'}






def menu_func(self, context):
    self.layout.operator(importMEB.bl_idname, text="Shift 2 mesh (.meb)")

def register():
    from bpy.utils import register_class
    register_class(importMEB)
    
    bpy.types.TOPBAR_MT_file_import.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    from bpy.utils import unregister_class
    unregister_class(importMEB)

    bpy.types.TOPBAR_MT_file_import.append(menu_func)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()