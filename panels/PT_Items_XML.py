
import bpy
import re
from bpy.types import (
    Panel,
    Operator,
)

from ..properties.Functions import ERROR_ENUM_ID, is_convert_panel_active
from ..utils.Functions import *
from ..utils.Constants import * 



class TM_PT_Items_ItemXML(Panel):
    # region bl_
    locals().update( PANEL_CLASS_COMMON_DEFAULT_PROPS )
    bl_label = ""
    bl_idname = "TM_PT_Items_Export_ItemXML"
    bl_parent_id = "TM_PT_Items_Export"
    # endregion
    
    @classmethod
    def poll(cls, context):
        return not is_convert_panel_active()

    def draw_header(self, context):
        layout = self.layout
        tm_props = get_global_props()
        row = layout.row()
        row.enabled = tm_props.CB_xml_genItemXML
        row.label(text="Item XML")
    
    def draw_header_preset(self, context):
        layout = self.layout
        tm_props = get_global_props()
        row = layout.row(align=True)

        col = row.column(align=True)
        col.enabled = tm_props.CB_xml_genItemXML
        col.prop(tm_props, "CB_xml_overwriteItemXML",   text="", icon=ICON_UPDATE)
        col = row.column(align=True)
        col.prop(tm_props, "CB_xml_genItemXML",         text="", icon=ICON_CHECKED,)
        row=layout.row()
    
    def draw(self, context):

        layout = self.layout
        tm_props        = get_global_props()
        tm_props_pivots = get_pivot_props()
        
        if tm_props.CB_showConvertPanel \
        or tm_props.CB_xml_genItemXML is False:
            return
        
        
        display_type     = tm_props.LI_xml_simpleOrAdvanced
        display_simple   = display_type.upper() == "SIMPLE"
        display_advanced = display_type.upper() == "ADVANCED"
        display_template = display_type.upper() == "TEMPLATE"
        
        layout.label(text="Placement Parameters:")

        row = layout.row(align=True)
        row.prop(tm_props, "LI_xml_simpleOrAdvanced", expand=True)

        if is_game_maniaplanet():
            row = layout.row()
            row.prop(tm_props, "LI_materialCollection", text="Envi")

        if display_simple:
            main_col = layout.column(align=True)
            
            x_row = main_col.row(align=True)
            x_row.label(text="Grid "+CHAR_HORIZONTAL, )
            x_row.prop(tm_props, "LI_xml_simpleGridXY", expand=True)
            
            z_row = main_col.row(align=True)
            z_row.label(text="Grid "+CHAR_VERTICAL)
            z_row.prop(tm_props, "LI_xml_simpleGridZ", expand=True)

            gridXYis0 = tm_props.LI_xml_simpleGridXY == "0"
            gridZis0  = tm_props.LI_xml_simpleGridZ  == "0"
            row = main_col.row(align=True)
            row_ghost = row.column(align=True).row(align=True)
            row.prop(tm_props, "CB_xml_ghostMode",   icon=ICON_GHOSTMODE)
            row_autorot = row.column(align=True).row(align=True)
            row_autorot.enabled = gridXYis0 and gridZis0
            row_autorot.prop(tm_props, "CB_xml_autoRot", icon=ICON_AUTO_ROTATION)

            row = layout.row()
            row.operator("view3d.tm_save_item_placement_template", text="Save as Template", icon=ICON_SAVE)


        elif display_advanced: # advanced
            sync = tm_props.CB_xml_syncGridLevi
            boxCol = layout.column(align=True)
            row = boxCol.row()
            row.prop(tm_props, "CB_xml_syncGridLevi", text="Sync Grid & Levitation", icon=ICON_SYNC)
            
            if sync:
                boxRow = boxCol.row(align=True)
                boxRow.enabled = True if sync else False
                boxRow.prop(tm_props, "NU_xml_gridAndLeviX", text=CHAR_HORIZONTAL+" Place")
                boxRow.prop(tm_props, "NU_xml_gridAndLeviY", text=CHAR_VERTICAL+" Place")
                boxRow = boxCol.row(align=True)
                boxRow.enabled = True if sync else False
                boxRow.prop(tm_props, "NU_xml_gridAndLeviOffsetX", text=CHAR_HORIZONTAL+" Offset")
                boxRow.prop(tm_props, "NU_xml_gridAndLeviOffsetY", text=CHAR_VERTICAL+" Offset")
            
            boxCol = layout.column(align=True)
            boxRow = boxCol.row(align=True)
            boxRow.enabled = False if sync else True
            boxRow.label(text="Grid")
            boxRow.prop(tm_props, "NU_xml_gridX", text=CHAR_HORIZONTAL)
            boxRow.prop(tm_props, "NU_xml_gridY", text=CHAR_VERTICAL)
            boxRow = boxCol.row(align=True)
            boxRow.enabled = False if sync else True
            boxRow.label(text="Offset")
            boxRow.prop(tm_props, "NU_xml_gridXoffset", text=CHAR_HORIZONTAL)
            boxRow.prop(tm_props, "NU_xml_gridYoffset", text=CHAR_VERTICAL)
            
            boxCol = layout.column(align=True)
            boxRow = boxCol.row(align=True)
            boxRow.enabled = False if sync else True
            boxRow.label(text="Levitation")
            boxRow.prop(tm_props, "NU_xml_leviX", text=CHAR_HORIZONTAL)
            boxRow.prop(tm_props, "NU_xml_leviY", text=CHAR_VERTICAL)
            boxRow = boxCol.row(align=True)
            boxRow.enabled = False if sync else True
            boxRow.label(text="Offset")
            boxRow.prop(tm_props, "NU_xml_leviXoffset", text=CHAR_HORIZONTAL)
            boxRow.prop(tm_props, "NU_xml_leviYoffset", text=CHAR_VERTICAL)
            
            boxCol = layout.column(align=True)
            boxRow = boxCol.row(align=True)
            boxRow.prop(tm_props, "CB_xml_ghostMode",   icon=ICON_GHOSTMODE)
            boxRow.prop(tm_props, "CB_xml_autoRot",     icon=ICON_AUTO_ROTATION)
            boxRow = boxCol.row(align=True)
            boxRow.prop(tm_props, "CB_xml_oneAxisRot",  icon=ICON_ONE_AXIS_ROTATION)
            boxRow.prop(tm_props, "CB_xml_notOnItem",   icon=ICON_NOT_ON_ITEM)
            
            pivot_col = layout.column(align=True)
            row=pivot_col.row(align=True)
            row.prop(tm_props, "CB_xml_pivots", text="Pivots (Placement Variants)", icon=ICON_PIVOTS)
            
            if tm_props.CB_xml_pivots is True:
                row = pivot_col.row(align=True)
                row.operator("view3d.tm_addpivot", text="Add", icon=ICON_ADD)
                row.prop(tm_props, "CB_xml_pivotSwitch",    text="Switch", expand=True, icon=ICON_SWITCH)
                row.prop(tm_props, "NU_xml_pivotSnapDis",   text="Snap Distance")
                
                
                if len(tm_props_pivots):
                    pivot_box = layout.box()
                    for i, pivot in enumerate(tm_props_pivots):
                        row = pivot_box.row(align=True)
                        row.prop(tm_props_pivots[i], "NU_pivotX", text=CHAR_BOTTOM_LEFT )
                        row.prop(tm_props_pivots[i], "NU_pivotY", text=CHAR_BOTTOM_RIGHT )
                        row.prop(tm_props_pivots[i], "NU_pivotZ", text=CHAR_TOP )
                        row.operator("view3d.tm_removepivot", text="", icon=ICON_REMOVE).pivot_index = i

            row = layout.row()
            row.operator("view3d.tm_save_item_placement_template", text="Save as Template", icon=ICON_SAVE)

        elif display_template:
            selected_template_name = tm_props.LI_xml_item_template_globally
            col = layout.column(align=True)
            row = col.row(align=True)
            row.prop(tm_props, "LI_xml_item_template_globally")
            row.operator("view3d.tm_remove_item_placement_template", text=f"", icon=ICON_REMOVE).template_name = selected_template_name
            row.prop(tm_props, "CB_xml_ignore_assigned_templates", text=f"", icon=ICON_RECURSIVE)
            
            # if selected_template_name != ERROR_ENUM_ID:
            #     row = col.row()
            #     row.prop(tm_props, "CB_xml_ignore_assigned_templates", text=f"Force on all collections", toggle=True, icon=ICON_EDIT)
            #     row = layout.row()
            

            
        layout.separator(factor=UI_SPACER_FACTOR)


class TM_PT_Items_MeshXML(Panel):
    # region bl_
    locals().update( PANEL_CLASS_COMMON_DEFAULT_PROPS )
    bl_label = ""
    bl_idname = "TM_PT_Items_Export_MeshXML"
    bl_parent_id = "TM_PT_Items_Export"
    # endregion
    
    @classmethod
    def poll(cls, context):
        return not is_convert_panel_active()

    def draw_header(self, context):
        layout = self.layout
        tm_props = get_global_props()
        row = layout.row()
        row.enabled = tm_props.CB_xml_genMeshXML
        row.label(text="Mesh XML")
    
    def draw_header_preset(self, context):
        layout = self.layout
        tm_props = get_global_props()
        row = layout.row(align=True)

        col = row.column(align=True)
        col.enabled = tm_props.CB_xml_genMeshXML
        col.prop(tm_props, "CB_xml_overwriteMeshXML",   text="", icon=ICON_UPDATE)
        col = row.column(align=True)
        col.prop(tm_props, "CB_xml_genMeshXML",         text="", icon=ICON_CHECKED,)
        row=layout.row()

    
    def draw(self, context):
        layout = self.layout
        tm_props        = get_global_props()
        
        
        if tm_props.CB_showConvertPanel:
            return
    
        if tm_props.CB_xml_genItemXML is False:
            return
        

        layout.label(text="Overwrite all objects/lights settings:")

        #--- object scale
        row = layout.row(align=True)
        col = row.column(align=True)
        col.enabled = True
        col.prop(tm_props, "CB_xml_scale", toggle=True, icon=ICON_SCALE, text="Object scale")
        col = row.column(align=True)
        col.enabled = False if not tm_props.CB_xml_scale else True
        # col.scale_x = .75
        col.prop(tm_props, "NU_xml_scale", text="")

        
        #--- light power
        col_light = layout.column(align=True)
        row = col_light.row(align=True)
        col = row.column(align=True)
        col.enabled = True
        col.prop(tm_props, "CB_xml_lightPower", icon=ICON_LIGHT_POWER, text="Light power")
        col = row.column(align=True)
        col.enabled = False if not tm_props.CB_xml_lightPower else True
        col.prop(tm_props, "NU_xml_lightPower", text="")


        #--- light color
        row = col_light.row(align=True)
        col = row.column(align=True)
        col.enabled = True
        col.prop(tm_props, "CB_xml_lightGlobColor", icon=ICON_LIGHT_COLOR, text="Light color")
        col = row.column(align=True)
        col.enabled = False if not tm_props.CB_xml_lightGlobColor else True
        col.prop(tm_props, "NU_xml_lightGlobColor", text="")
        
        
        #--- light distance
        row = col_light.row(align=True)
        col = row.column(align=True)
        col.enabled = True
        col.prop(tm_props, "CB_xml_lightGlobDistance", icon=ICON_LIGHT_RADIUS, text="Light radius")
        col = row.column(align=True)
        col.enabled = False if not tm_props.CB_xml_lightGlobDistance else True
        col.prop(tm_props, "NU_xml_lightGlobDistance", text="")
        
        

        layout.separator(factor=UI_SPACER_FACTOR)


