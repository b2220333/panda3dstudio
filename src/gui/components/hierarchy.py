from ..base import *
from ..button import Button, ButtonGroup
from ..toggle import ToggleButtonGroup
from ..combobox import ComboBox
from ..field import InputField
from ..checkbox import CheckBox
from ..colorctrl import ColorPickerCtrl
from ..panel import *


class HierarchyPanel(Panel):

    def __init__(self, parent, focus_receiver=None):

        Panel.__init__(self, parent, "Hierarchy", focus_receiver)

        self._parent = parent
        self._width = parent.get_width()

        self._comboboxes = {}
        self._checkboxes = {}
        self._color_pickers = {}
        self._fields = {}
        self._btns = {}
        self._radio_btns = {}

##        self._map_type = "color"

        panel_sizer = self.GetSizer()
        panel_sizer.Add(wx.Size(self._width, 0))
        parent.GetSizer().Add(self)

        bitmap_paths = Button.get_bitmap_paths("panel_button")

        # ********************** Object linking section ************************

        link_section = section = self.add_section("linking", "Object linking")
        sizer = section.get_client_sizer()
##        sizer.Add(wx.Size(0, 10))

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(btn_sizer)
        sizer_args = (0, wx.ALL, 2)

        label = "Link"
        bitmaps = PanelButton.create_button_bitmaps("*%s" % label, bitmap_paths)
        btn = PanelButton(self, section, btn_sizer, bitmaps, label, "Link objects",
                          self.__toggle_linking_mode, sizer_args, focus_receiver=focus_receiver)
        self._btns["link"] = btn

        btn_sizer.Add(wx.Size(5, 0))

        label = "Unlink"
        bitmaps = PanelButton.create_button_bitmaps("*%s" % label, bitmap_paths)
        btn = PanelButton(self, section, btn_sizer, bitmaps, label, "Unlink selected objects",
                          self.__unlink_objects, sizer_args, focus_receiver=focus_receiver)
        self._btns["unlink"] = btn

        btn_sizer.Add(wx.Size(5, 0))

        label = "Show"
        bitmaps = PanelButton.create_button_bitmaps("*%s" % label, bitmap_paths)
        btn = PanelButton(self, section, btn_sizer, bitmaps, label, "Show links between objects",
                          self.__toggle_link_visibility, sizer_args, focus_receiver=focus_receiver)
        self._btns["show_links"] = btn
##
##        sizer.Add(wx.Size(0, 2))
##
##        sizer_args = (0, wx.ALIGN_CENTER_HORIZONTAL)
##        label = "Clear"
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths)
##        btn = PanelButton(self, section, sizer, bitmaps, label, "Remove all materials from library",
##                          self.__clear_library, sizer_args, focus_receiver=focus_receiver)
##
##        # ************************* Material section **************************
##
##        section = self.add_section("material", "Material")
##        sizer = section.get_client_sizer()
##
##        combobox = EditablePanelComboBox(self, section, sizer, "Selected material",
##                                         164, focus_receiver=focus_receiver)
##        combobox.set_editable(False)
##        self._comboboxes["material"] = combobox
##
##        self._selected_mat_id = None
##        self._selected_layer_id = None
##
##        field = combobox.get_input_field()
##        val_id = "name"
##        field.add_value(val_id, "string", handler=self.__handle_value)
##        field.set_input_parser(val_id, self.__parse_name)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        sizer.Add(wx.Size(0, 2))
##        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
##        sizer.Add(btn_sizer, 0, wx.ALL, 2)
##        sizer_args = (0, wx.RIGHT, 15)
##
##        icon_path = os.path.join(GFX_PATH, "icon_marker.png")
##        bitmaps = PanelButton.create_button_bitmaps(icon_path, bitmap_paths)
##        btn = PanelButton(self, section, btn_sizer, bitmaps, "", "Edit selected material name",
##                          self.__toggle_material_name_editable, sizer_args, focus_receiver=focus_receiver)
##        self._edit_mat_name_btn = btn
##
##        icon_path = os.path.join(GFX_PATH, "icon_plus_equal.png")
##        bitmaps = PanelButton.create_button_bitmaps(icon_path, bitmap_paths)
##        btn = PanelButton(self, section, btn_sizer, bitmaps, "", "Add copy of selected material",
##                          self.__copy_material, sizer_args, focus_receiver=focus_receiver)
##
##        icon_path = os.path.join(GFX_PATH, "icon_plus.png")
##        bitmaps = PanelButton.create_button_bitmaps(icon_path, bitmap_paths)
##        btn = PanelButton(self, section, btn_sizer, bitmaps, "", "Add new material",
##                          self.__create_material, sizer_args, focus_receiver=focus_receiver)
##
##        icon_path = os.path.join(GFX_PATH, "icon_minus.png")
##        bitmaps = PanelButton.create_button_bitmaps(icon_path, bitmap_paths)
##        btn = PanelButton(self, section, btn_sizer, bitmaps, "", "Remove selected material",
##                          self.__remove_material, sizer_args=(), focus_receiver=focus_receiver)
##
##        sizer.Add(wx.Size(0, 2))
##        group = section.add_group("Extract from objects")
##        grp_sizer = group.get_client_sizer()
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##
##        label = "Selection"
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths)
##        btn = PanelButton(self, group, subsizer, bitmaps, label, "Extract materials from selected objects",
##                          self.__extract_material, focus_receiver=focus_receiver)
##
##        subsizer.Add(wx.Size(15, 0))
##        label = "Pick..."
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths)
##        btn = PanelButton(self, group, subsizer, bitmaps, label, "Extract material from single object",
##                          lambda: None, focus_receiver=focus_receiver)
##
##        sizer.Add(wx.Size(0, 2))
##        group = section.add_group("Apply to objects")
##        grp_sizer = group.get_client_sizer()
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##
##        label = "Selection"
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths)
##        btn = PanelButton(self, group, subsizer, bitmaps, label, "Apply sel. material to sel. objects",
##                          self.__apply_material, focus_receiver=focus_receiver)
##
##        subsizer.Add(wx.Size(15, 0))
##        label = "Pick..."
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths)
##        btn = PanelButton(self, group, subsizer, bitmaps, label, "Apply sel. material to single object",
##                          lambda: None, focus_receiver=focus_receiver)
##
##        sizer_args = (0, wx.ALIGN_CENTER_HORIZONTAL)
##
##        sizer.Add(wx.Size(0, 2))
##        group = section.add_group("Owner selection")
##        grp_sizer = group.get_client_sizer()
##        label = "(De)select owners"
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths)
##        btn = PanelButton(self, group, grp_sizer, bitmaps, label, "Select all objects having the sel. material",
##                          self.__select_material_owners, sizer_args, focus_receiver=focus_receiver)
##        grp_sizer.Add(wx.Size(0, 5))
##
##        group.add_text("Current selection:", grp_sizer)
##        grp_sizer.Add(wx.Size(0, 3))
##
##        radio_btns = PanelRadioButtonGroup(self, group, "", grp_sizer)
##        btn_ids = ("replace", "add_to", "remove_from")
##        texts = ("replace with owners", "add owners", "remove owners")
##        get_command = lambda sel_mode: lambda: Mgr.update_app(
##            "material_owner_sel_mode", sel_mode)
##
##        for btn_id, text in zip(btn_ids, texts):
##            radio_btns.add_button(btn_id, text)
##            command = get_command(btn_id)
##            radio_btns.set_button_command(btn_id, command)
##
##        radio_btns.set_selected_button("replace")
##        self._radio_btns["owner_sel"] = radio_btns
##
##        # *********************** Basic props section *************************
##
##        prop_section = section = self.add_section(
##            "basic_props", "Basic properties")
##        sizer = section.get_client_sizer()
##
##        subsizer = wx.FlexGridSizer(rows=0, cols=3, hgap=5)
##        sizer.Add(subsizer)
##        sizer_args = (0, wx.ALIGN_CENTER_VERTICAL)
##
##        prop_ids = ("diffuse", "ambient", "emissive", "specular")
##        self._base_prop_ids = prop_ids + ("shininess",)
##
##        for prop_id in prop_ids:
##            checkbox = PanelCheckBox(self, section, subsizer, self.__get_color_toggler(prop_id),
##                                     sizer_args=sizer_args)
##            self._checkboxes[prop_id] = checkbox
##            section.add_text("%s color:" %
##                             prop_id.title(), subsizer, sizer_args)
##            handler = self.__get_color_handler(prop_id)
##            color_picker = PanelColorPickerCtrl(
##                self, section, subsizer, handler)
##            self._color_pickers[prop_id] = color_picker
##
##        subsizer.Add(wx.Size(0, 0))
##        section.add_text("Shininess:", subsizer, sizer_args)
##        field = PanelInputField(self, section, subsizer,
##                                60, sizer_args=sizer_args)
##        val_id = "shininess"
##        field.add_value(val_id, "float", handler=self.__handle_value)
##        field.show_value(val_id)
##        field.set_input_parser(val_id, self.__parse_shininess)
##        self._fields[val_id] = field
##
##        val_id = "alpha"
##        checkbox = PanelCheckBox(
##            self, section, subsizer, self.__get_color_toggler(val_id))
##        self._checkboxes[val_id] = checkbox
##        section.add_text("\nTransparency/\nOpacity:\n", subsizer)
##        field = PanelInputField(self, section, subsizer,
##                                60, sizer_args=(0, wx.ALIGN_BOTTOM))
##        field.add_value(val_id, "float", handler=self.__handle_value)
##        field.show_value(val_id)
##        field.set_input_parser(val_id, self.__parse_alpha)
##        self._fields[val_id] = field
##
##        # ************************* Texmaps section ***************************
##
##        map_section = section = self.add_section("texmaps", "Texture maps")
##        sizer = section.get_client_sizer()
##        subsizer = wx.BoxSizer()
##        sizer.Add(subsizer)
##
##        val_id = "tex_map"
##        checkbox = PanelCheckBox(self, section, subsizer, self.__toggle_tex_map,
##                                 sizer_args=sizer_args)
##        self._checkboxes[val_id] = checkbox
##        subsizer.Add(wx.Size(5, 0))
##        combobox = PanelComboBox(self, section, subsizer, "Selected texture map",
##                                 134, sizer_args=sizer_args, focus_receiver=focus_receiver)
##        self._comboboxes["map_type"] = combobox
##
##        def get_command(map_type):
##
##            def set_map_type():
##
##                self._map_type = map_type
##                mat_id = self._selected_mat_id
##                Mgr.update_remotely("material_prop", mat_id,
##                                    "tex_map_select", map_type)
##
##            return set_map_type
##
##        for map_type in ("color", "normal", "height", "normal+height", "gloss",
##                         "color+gloss", "glow", "color+glow"):
##            combobox.add_item(map_type, map_type.title(),
##                              get_command(map_type))
##
##        sizer.Add(wx.Size(0, 5))
##
##        group = section.add_group("Texture files")
##        grp_sizer = group.get_client_sizer()
##
##        subsizer = wx.FlexGridSizer(rows=0, cols=2, hgap=4)
##        grp_sizer.Add(subsizer)
##        label = "Main"
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths, 40)
##        btn = PanelButton(self, group, subsizer, bitmaps, label,
##                          "Load main texture for selected map", self.__load_texture_map_main,
##                          sizer_args, focus_receiver=focus_receiver)
##        field = PanelInputField(self, group, subsizer,
##                                100, sizer_args=sizer_args)
##        val_id = "tex_map_file_main"
##        field.add_value(val_id, "string", handler=self.__set_texture_map_main)
##        field.show_value(val_id)
##        field.set_input_init(val_id, self.__init_main_filename_input)
##        field.set_input_parser(val_id, self.__check_texture_filename)
##        field.set_value_parser(val_id, self.__parse_texture_filename)
##        self._fields[val_id] = field
##        label = "Alpha"
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths, 40)
##        btn = PanelButton(self, group, subsizer, bitmaps, label,
##                          "Load alpha texture for selected map", self.__load_texture_map_alpha,
##                          sizer_args, focus_receiver=focus_receiver)
##        field = PanelInputField(self, group, subsizer,
##                                100, sizer_args=sizer_args)
##        val_id = "tex_map_file_alpha"
##        field.add_value(val_id, "string", handler=self.__set_texture_map_alpha)
##        field.show_value(val_id)
##        field.set_input_init(val_id, self.__init_alpha_filename_input)
##        field.set_input_parser(val_id, self.__check_texture_filename)
##        field.set_value_parser(val_id, self.__parse_texture_filename)
##        self._fields[val_id] = field
##
##        sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        sizer.Add(subsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
##        section.add_text("Border color:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        color_picker = PanelColorPickerCtrl(
##            self, section, subsizer, self.__handle_border_color)
##        self._color_pickers["tex_map_border_color"] = color_picker
##
##        sizer.Add(wx.Size(0, 5))
##
##        group = section.add_group("Wrapping")
##        grp_sizer = group.get_client_sizer()
##
##        mode_ids = ("repeat", "clamp", "border_color", "mirror", "mirror_once")
##        mode_names = ("Repeat", "Clamp", "Border color",
##                      "Mirror", "Mirror once")
##        get_command = lambda axis, mode_id: lambda: Mgr.update_remotely("material_prop",
##                                                                        self._selected_mat_id, "tex_map_wrap_%s" % axis, mode_id)
##
##        subsizer = wx.FlexGridSizer(rows=0, cols=2, hgap=4, vgap=4)
##        grp_sizer.Add(subsizer)
##
##        for axis in ("u", "v"):
##
##            group.add_text("%s:" % axis.title(), subsizer, sizer_args)
##            combobox = PanelComboBox(self, group, subsizer, "%s wrap mode" % axis.title(),
##                                     130, sizer_args=sizer_args, focus_receiver=focus_receiver)
##
##            for mode_id, mode_name in zip(mode_ids, mode_names):
##                combobox.add_item(mode_id, mode_name,
##                                  get_command(axis, mode_id))
##
##            self._comboboxes["tex_map_wrap_%s" % axis] = combobox
##
##        grp_sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##
##        val_id = "tex_map_wrap_lock"
##        checkbox = PanelCheckBox(self, group, subsizer, self.__toggle_wrap_lock,
##                                 sizer_args=sizer_args)
##        self._checkboxes[val_id] = checkbox
##        subsizer.Add(wx.Size(4, 0))
##        group.add_text("Lock U and V modes", subsizer, sizer_args)
##
##        sizer.Add(wx.Size(0, 5))
##
##        group = section.add_group("Filtering")
##        grp_sizer = group.get_client_sizer()
##
##        get_command = lambda minmag, type_id: lambda: Mgr.update_remotely("material_prop",
##                                                                          self._selected_mat_id, "tex_map_filter_%s" % minmag, type_id)
##
##        subsizer = wx.FlexGridSizer(rows=0, cols=2, hgap=4, vgap=4)
##        grp_sizer.Add(subsizer)
##        group.add_text("-:", subsizer, sizer_args)
##        combobox = PanelComboBox(self, group, subsizer, "Minification filter",
##                                 130, sizer_args=sizer_args, focus_receiver=focus_receiver)
##
##        type_ids = ("linear", "nearest", "nearest_mipmap_nearest", "nearest_mipmap_linear",
##                    "linear_mipmap_nearest", "linear_mipmap_linear", "shadow")
##        type_names = ("Linear", "Nearest", "Nearest mipmap nearest", "Nearest mipmap linear",
##                      "Linear mipmap nearest", "Linear mipmap linear", "Shadow")
##
##        for type_id, type_name in zip(type_ids, type_names):
##            combobox.add_item(type_id, type_name, get_command("min", type_id))
##
##        self._comboboxes["tex_map_filter_min"] = combobox
##
##        group.add_text("+:", subsizer, sizer_args)
##        combobox = PanelComboBox(self, group, subsizer, "Magnification filter",
##                                 130, sizer_args=sizer_args, focus_receiver=focus_receiver)
##
##        type_ids = ("linear", "nearest")
##        type_names = ("Linear", "Nearest")
##
##        for type_id, type_name in zip(type_ids, type_names):
##            combobox.add_item(type_id, type_name, get_command("mag", type_id))
##
##        self._comboboxes["tex_map_filter_mag"] = combobox
##
##        grp_sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##        group.add_text("Anisotropic level:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                40, sizer_args=sizer_args)
##        val_id = "tex_map_anisotropic_degree"
##        field.add_value(val_id, "int", handler=self.__handle_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        # *************************** Texmap transform section ****************
##
##        map_xform_section = section = self.add_section(
##            "texmap_xform", "Tex. map transform")
##        sizer = section.get_client_sizer()
##
##        group = section.add_group("Offset")
##        grp_sizer = group.get_client_sizer()
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##        group.add_text("U:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                54, sizer_args=sizer_args)
##        val_id = "tex_map_offset_u"
##        field.add_value(val_id, "float", handler=self.__handle_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##        subsizer.Add(wx.Size(8, 0))
##        group.add_text("V:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                54, sizer_args=sizer_args)
##        val_id = "tex_map_offset_v"
##        field.add_value(val_id, "float", handler=self.__handle_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        sizer.Add(subsizer)
##        section.add_text("Rotation:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, section, subsizer,
##                                90, sizer_args=sizer_args)
##        val_id = "tex_map_rotate"
##        field.add_value(val_id, "float", handler=self.__handle_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        sizer.Add(wx.Size(0, 5))
##
##        group = section.add_group("Scale")
##        grp_sizer = group.get_client_sizer()
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##        group.add_text("U:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                54, sizer_args=sizer_args)
##        val_id = "tex_map_scale_u"
##        field.add_value(val_id, "float", handler=self.__handle_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##        subsizer.Add(wx.Size(8, 0))
##        group.add_text("V:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                54, sizer_args=sizer_args)
##        val_id = "tex_map_scale_v"
##        field.add_value(val_id, "float", handler=self.__handle_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        # *************************** Layer section ***************************
##
##        layer_section = section = self.add_section("layers", "Layers")
##        sizer = section.get_client_sizer()
##
##        subsizer = wx.BoxSizer()
##        sizer_args = (0, wx.ALIGN_CENTER_VERTICAL)
##        sizer.Add(subsizer)
##        val_id = "layers"
##        checkbox = PanelCheckBox(self, section, subsizer, self.__toggle_layers,
##                                 sizer_args=sizer_args)
##        self._checkboxes[val_id] = checkbox
##        subsizer.Add(wx.Size(5, 0))
##        section.add_text(
##            "Use layers\n(overrides single color map)", subsizer, sizer_args)
##        sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        sizer.Add(subsizer)
##
##        val_id = "layer_on"
##        checkbox = PanelCheckBox(self, section, subsizer, self.__toggle_layer,
##                                 sizer_args=sizer_args)
##        self._checkboxes[val_id] = checkbox
##        subsizer.Add(wx.Size(5, 0))
##        combobox = EditablePanelComboBox(self, section, subsizer, "Selected layer",
##                                         134, sizer_args=sizer_args,
##                                         focus_receiver=focus_receiver)
##        combobox.set_editable(False)
##        self._comboboxes["layer"] = combobox
##
##        field = combobox.get_input_field()
##        val_id = "layer_name"
##        field.add_value(val_id, "string", handler=self.__handle_layer_value)
##        field.set_input_parser(val_id, self.__parse_name)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        sizer.Add(wx.Size(0, 2))
##        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
##        sizer.Add(btn_sizer, 0, wx.ALL, 2)
##        sizer_args = (0, wx.RIGHT, 15)
##
##        icon_path = os.path.join(GFX_PATH, "icon_marker.png")
##        bitmaps = PanelButton.create_button_bitmaps(icon_path, bitmap_paths)
##        btn = PanelButton(self, section, btn_sizer, bitmaps, "", "Edit selected layer name",
##                          self.__toggle_layer_name_editable, sizer_args, focus_receiver=focus_receiver)
##        self._edit_layer_name_btn = btn
##
##        icon_path = os.path.join(GFX_PATH, "icon_plus_equal.png")
##        bitmaps = PanelButton.create_button_bitmaps(icon_path, bitmap_paths)
##        btn = PanelButton(self, section, btn_sizer, bitmaps, "", "Add copy of selected layer",
##                          self.__copy_layer, sizer_args, focus_receiver=focus_receiver)
##
##        icon_path = os.path.join(GFX_PATH, "icon_plus.png")
##        bitmaps = PanelButton.create_button_bitmaps(icon_path, bitmap_paths)
##        btn = PanelButton(self, section, btn_sizer, bitmaps, "", "Add new layer",
##                          self.__create_layer, sizer_args, focus_receiver=focus_receiver)
##
##        icon_path = os.path.join(GFX_PATH, "icon_minus.png")
##        bitmaps = PanelButton.create_button_bitmaps(icon_path, bitmap_paths)
##        btn = PanelButton(self, section, btn_sizer, bitmaps, "", "Remove selected layer",
##                          self.__remove_layer, sizer_args=(), focus_receiver=focus_receiver)
##
##        sizer.Add(wx.Size(0, 5))
##
##        sizer_args = (0, wx.ALIGN_CENTER_VERTICAL)
##
##        subsizer = wx.BoxSizer()
##        sizer.Add(subsizer)
##        section.add_text("Sort:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, section, subsizer,
##                                40, sizer_args=sizer_args)
##        val_id = "layer_sort"
##        field.add_value(val_id, "int", handler=self.__handle_layer_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##        subsizer.Add(wx.Size(10, 0))
##        section.add_text("Priority:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, section, subsizer,
##                                40, sizer_args=sizer_args)
##        val_id = "layer_priority"
##        field.add_value(val_id, "int", handler=self.__handle_layer_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        # *************************** Layer color section *********************
##
##        layer_color_section = section = self.add_section(
##            "layer_color", "Layer color")
##        sizer = section.get_client_sizer()
##
##        group = section.add_group("Flat color")
##        grp_sizer = group.get_client_sizer()
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##        group.add_text("RGB:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        color_picker = PanelColorPickerCtrl(
##            self, group, subsizer, self.__handle_layer_rgb)
##        self._color_pickers["layer_rgb"] = color_picker
##        subsizer.Add(wx.Size(4, 0))
##        group.add_text("Alpha:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                45, sizer_args=sizer_args)
##        val_id = "layer_alpha"
##        field.set_input_parser(val_id, self.__parse_alpha)
##        field.add_value(val_id, "float", handler=self.__handle_layer_alpha)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        group = section.add_group("Color scale")
##        grp_sizer = group.get_client_sizer()
##        subsizer = wx.FlexGridSizer(rows=2, cols=2, hgap=4, vgap=4)
##        grp_sizer.Add(subsizer)
##
##        for channels, label in (("rgb", "RGB"), ("alpha", "Alpha")):
##
##            group.add_text("%s:" % label, subsizer, sizer_args)
##            subsizer2 = wx.BoxSizer()
##            subsizer.Add(subsizer2)
##
##            radio_btns = PanelRadioButtonGroup(
##                self, group, "", subsizer2, size=(3, 1))
##            btn_ids = (1, 2, 4)
##            get_command = lambda channels, scale: lambda: Mgr.update_remotely("tex_layer_prop",
##                                                                              self._selected_mat_id, self._selected_layer_id, "%s_scale" % channels, scale)
##
##            for btn_id in btn_ids:
##                radio_btns.add_button(btn_id, str(btn_id))
##                radio_btns.set_button_command(
##                    btn_id, get_command(channels, btn_id))
##
##            self._radio_btns["layer_%s_scale" % channels] = radio_btns
##
##        # *************************** Layer texture section *******************
##
##        layer_tex_section = section = self.add_section(
##            "layer_tex", "Layer texture")
##        sizer = section.get_client_sizer()
##
##        group = section.add_group("Texture files")
##        grp_sizer = group.get_client_sizer()
##
##        subsizer = wx.FlexGridSizer(rows=0, cols=2, hgap=4)
##        grp_sizer.Add(subsizer)
##        label = "Main"
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths, 40)
##        btn = PanelButton(self, group, subsizer, bitmaps, label,
##                          "Load main texture for selected layer", self.__load_layer_main,
##                          sizer_args, focus_receiver=focus_receiver)
##        field = PanelInputField(self, group, subsizer,
##                                100, sizer_args=sizer_args)
##        val_id = "layer_file_main"
##        field.add_value(val_id, "string", handler=self.__set_layer_main)
##        field.show_value(val_id)
##        field.set_input_init(val_id, self.__init_layer_main_filename_input)
##        field.set_input_parser(val_id, self.__check_texture_filename)
##        field.set_value_parser(val_id, self.__parse_texture_filename)
##        self._fields[val_id] = field
##        label = "Alpha"
##        bitmaps = PanelButton.create_button_bitmaps(
##            "*%s" % label, bitmap_paths, 40)
##        btn = PanelButton(self, group, subsizer, bitmaps, label,
##                          "Load alpha texture for selected layer", self.__load_layer_alpha,
##                          sizer_args, focus_receiver=focus_receiver)
##        field = PanelInputField(self, group, subsizer,
##                                100, sizer_args=sizer_args)
##        val_id = "layer_file_alpha"
##        field.add_value(val_id, "string", handler=self.__set_layer_alpha)
##        field.show_value(val_id)
##        field.set_input_init(val_id, self.__init_layer_alpha_filename_input)
##        field.set_input_parser(val_id, self.__check_texture_filename)
##        field.set_value_parser(val_id, self.__parse_texture_filename)
##        self._fields[val_id] = field
##
##        sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        sizer.Add(subsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
##        section.add_text("Border color:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        color_picker = PanelColorPickerCtrl(
##            self, section, subsizer, self.__handle_layer_border_color)
##        self._color_pickers["layer_border_color"] = color_picker
##
##        sizer.Add(wx.Size(0, 5))
##
##        group = section.add_group("Wrapping")
##        grp_sizer = group.get_client_sizer()
##
##        mode_ids = ("repeat", "clamp", "border_color", "mirror", "mirror_once")
##        mode_names = ("Repeat", "Clamp", "Border color",
##                      "Mirror", "Mirror once")
##        get_command = lambda axis, mode_id: lambda: Mgr.update_remotely("tex_layer_prop",
##                                                                        self._selected_mat_id, self._selected_layer_id, "wrap_%s" % axis, mode_id)
##
##        subsizer = wx.FlexGridSizer(rows=0, cols=2, hgap=4, vgap=4)
##        grp_sizer.Add(subsizer)
##
##        for axis in ("u", "v"):
##
##            group.add_text("%s:" % axis.title(), subsizer, sizer_args)
##            combobox = PanelComboBox(self, group, subsizer, "%s wrap mode" % axis.title(),
##                                     130, sizer_args=sizer_args, focus_receiver=focus_receiver)
##
##            for mode_id, mode_name in zip(mode_ids, mode_names):
##                combobox.add_item(mode_id, mode_name,
##                                  get_command(axis, mode_id))
##
##            self._comboboxes["layer_wrap_%s" % axis] = combobox
##
##        grp_sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##
##        val_id = "layer_wrap_lock"
##        checkbox = PanelCheckBox(self, group, subsizer, self.__toggle_layer_wrap_lock,
##                                 sizer_args=sizer_args)
##        self._checkboxes[val_id] = checkbox
##        subsizer.Add(wx.Size(4, 0))
##        group.add_text("Lock U and V modes", subsizer, sizer_args)
##
##        sizer.Add(wx.Size(0, 5))
##
##        group = section.add_group("Filtering")
##        grp_sizer = group.get_client_sizer()
##
##        get_command = lambda minmag, type_id: lambda: Mgr.update_remotely("tex_layer_prop",
##                                                                          self._selected_mat_id, self._selected_layer_id, "filter_%s" % minmag, type_id)
##
##        subsizer = wx.FlexGridSizer(rows=0, cols=2, hgap=4, vgap=4)
##        grp_sizer.Add(subsizer)
##        group.add_text("-:", subsizer, sizer_args)
##        combobox = PanelComboBox(self, group, subsizer, "Minification filter",
##                                 130, sizer_args=sizer_args, focus_receiver=focus_receiver)
##
##        type_ids = ("linear", "nearest", "nearest_mipmap_nearest", "nearest_mipmap_linear",
##                    "linear_mipmap_nearest", "linear_mipmap_linear", "shadow")
##        type_names = ("Linear", "Nearest", "Nearest mipmap nearest", "Nearest mipmap linear",
##                      "Linear mipmap nearest", "Linear mipmap linear", "Shadow")
##
##        for type_id, type_name in zip(type_ids, type_names):
##            combobox.add_item(type_id, type_name, get_command("min", type_id))
##
##        self._comboboxes["layer_filter_min"] = combobox
##
##        group.add_text("+:", subsizer, sizer_args)
##        combobox = PanelComboBox(self, group, subsizer, "Magnification filter",
##                                 130, sizer_args=sizer_args, focus_receiver=focus_receiver)
##
##        type_ids = ("linear", "nearest")
##        type_names = ("Linear", "Nearest")
##
##        for type_id, type_name in zip(type_ids, type_names):
##            combobox.add_item(type_id, type_name, get_command("mag", type_id))
##
##        self._comboboxes["layer_filter_mag"] = combobox
##
##        grp_sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##        group.add_text("Anisotropic level:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                40, sizer_args=sizer_args)
##        val_id = "layer_anisotropic_degree"
##        field.add_value(val_id, "int", handler=self.__handle_layer_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        sizer.Add(subsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
##        section.add_text("UV set:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, section, subsizer,
##                                40, sizer_args=sizer_args)
##        val_id = "layer_uv_set"
##        field.add_value(val_id, "int", handler=self.__handle_layer_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        # *************************** Layer transform section *****************
##
##        layer_xform_section = section = self.add_section(
##            "layer_xform", "Layer transform")
##        sizer = section.get_client_sizer()
##
##        group = section.add_group("Offset")
##        grp_sizer = group.get_client_sizer()
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##        group.add_text("U:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                54, sizer_args=sizer_args)
##        val_id = "layer_offset_u"
##        field.add_value(val_id, "float", handler=self.__handle_layer_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##        subsizer.Add(wx.Size(8, 0))
##        group.add_text("V:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                54, sizer_args=sizer_args)
##        val_id = "layer_offset_v"
##        field.add_value(val_id, "float", handler=self.__handle_layer_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        sizer.Add(subsizer)
##        section.add_text("Rotation:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, section, subsizer,
##                                90, sizer_args=sizer_args)
##        val_id = "layer_rotate"
##        field.add_value(val_id, "float", handler=self.__handle_layer_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        sizer.Add(wx.Size(0, 5))
##
##        group = section.add_group("Scale")
##        grp_sizer = group.get_client_sizer()
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##        group.add_text("U:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                54, sizer_args=sizer_args)
##        val_id = "layer_scale_u"
##        field.add_value(val_id, "float", handler=self.__handle_layer_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##        subsizer.Add(wx.Size(8, 0))
##        group.add_text("V:", subsizer, sizer_args)
##        subsizer.Add(wx.Size(4, 0))
##        field = PanelInputField(self, group, subsizer,
##                                54, sizer_args=sizer_args)
##        val_id = "layer_scale_v"
##        field.add_value(val_id, "float", handler=self.__handle_layer_value)
##        field.show_value(val_id)
##        self._fields[val_id] = field
##
##        # ************************* Layer blending section ********************
##
##        blend_section = section = self.add_section(
##            "layer_blending", "Layer blending")
##        sizer = section.get_client_sizer()
##
##        group = section.add_group("Basic blending")
##        grp_sizer = group.get_client_sizer()
##        combobox = PanelComboBox(self, group, grp_sizer, "Blend mode", 140)
##        self._comboboxes["layer_blend_mode"] = combobox
##
##        mode_ids = ("modulate", "combine", "blend", "replace", "decal", "add",
##                    "blend_color_scale", "selector")
##        mode_names = ("Modulate", "Combine", "Blend", "Replace", "Decal", "Add",
##                      "Blend color scale", "Selector")
##        get_command = lambda mode_id: lambda: Mgr.update_remotely("tex_layer_prop",
##                                                                  self._selected_mat_id, self._selected_layer_id, "blend_mode", mode_id)
##
##        for mode_id, mode_name in zip(mode_ids, mode_names):
##            combobox.add_item(mode_id, mode_name, get_command(mode_id))
##
##        group = section.add_group("Advanced combining")
##        grp_sizer = group.get_client_sizer()
##        group.add_text(
##            "Using any combine mode\noverrides basic blend mode", grp_sizer)
##        grp_sizer.Add(wx.Size(0, 5))
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##        sizer_args = (0, wx.ALIGN_CENTER_VERTICAL)
##        val_id = "layer_combine_channels_use"
##        checkbox = PanelCheckBox(self, group, subsizer, self.__toggle_layer_combine_channels,
##                                 sizer_args=sizer_args)
##        self._checkboxes[val_id] = checkbox
##        subsizer.Add(wx.Size(5, 0))
##
##        combobox = PanelComboBox(self, group, subsizer, "Channels", 100,
##                                 sizer_args=sizer_args)
##        self._comboboxes["layer_combine_channels"] = combobox
##        get_command = lambda channels: lambda: Mgr.update_remotely("tex_layer_prop",
##                                                                   self._selected_mat_id, self._selected_layer_id,
##                                                                   "combine_channels", channels)
##
##        for item_id, item_label in (("rgb", "RGB"), ("alpha", "Alpha")):
##            combobox.add_item(item_id, item_label, get_command(item_id))
##
##        grp_sizer.Add(wx.Size(0, 10))
##
##        combobox = PanelComboBox(self, group, grp_sizer, "Combine mode", 140)
##        self._comboboxes["layer_combine_mode"] = combobox
##        get_command = lambda mode_id: lambda: Mgr.update_remotely("tex_layer_prop",
##                                                                  self._selected_mat_id, self._selected_layer_id, "combine_mode", mode_id)
##
##        mode_ids = ("modulate", "replace", "interpolate", "add", "add_signed",
##                    "subtract", "dot3rgb", "dot3rgba")
##        mode_names = ("Modulate", "Replace", "Interpolate", "Add", "Add signed",
##                      "Subtract", "Dot3 RGB", "Dot3 RGBA")
##        for mode_id, mode_name in zip(mode_ids, mode_names):
##            combobox.add_item(mode_id, mode_name, get_command(mode_id))
##
##        grp_sizer.Add(wx.Size(0, 5))
##
##        subgroup = group.add_group("Sources")
##        subgrp_sizer = subgroup.get_client_sizer()
##
##        combobox = PanelComboBox(
##            self, subgroup, subgrp_sizer, "Source type", 125)
##        self._comboboxes["layer_combine_source_index"] = combobox
##
##        subgrp_sizer.Add(wx.Size(0, 10))
##        combobox = PanelComboBox(self, subgroup, subgrp_sizer, "Source", 125)
##        self._comboboxes["layer_combine_source"] = combobox
##        src_ids = ("texture", "previous_layer", "primary_color", "constant_color",
##                   "const_color_scale", "last_stored_layer")
##        src_names = ("Texture", "Previous layer", "Primary color", "Flat color",
##                     "Color scale", "Last stored layer")
##        get_command = lambda src_id: lambda: Mgr.update_remotely("tex_layer_prop",
##                                                                 self._selected_mat_id, self._selected_layer_id, "combine_source", src_id)
##
##        for src_id, src_name in zip(src_ids, src_names):
##            combobox.add_item(src_id, src_name, get_command(src_id))
##
##        radio_btns = PanelRadioButtonGroup(
##            self, subgroup, "", subgrp_sizer, size=(2, 2))
##        btn_ids = ("rgb", "1-rgb", "alpha", "1-alpha")
##        texts = ("RGB", "1 - RGB", "Alpha", "1 - Alpha")
##        get_command = lambda channels: lambda: Mgr.update_remotely("tex_layer_prop",
##                                                                   self._selected_mat_id, self._selected_layer_id, "combine_source_channels", channels)
##
##        for btn_id, text in zip(btn_ids, texts):
##            radio_btns.add_button(btn_id, text)
##            radio_btns.set_button_command(btn_id, get_command(btn_id))
##
##        radio_btns.set_selected_button("rgb")
##        self._radio_btns["layer_combine_source_channels"] = radio_btns
##
##        grp_sizer.Add(wx.Size(0, 5))
##
##        subsizer = wx.BoxSizer()
##        grp_sizer.Add(subsizer)
##        val_id = "layer_is_stored"
##        checkbox = PanelCheckBox(self, group, subsizer, self.__store_layer,
##                                 sizer_args=sizer_args)
##        self._checkboxes[val_id] = checkbox
##        subsizer.Add(wx.Size(5, 0))
##        group.add_text("Store layer", subsizer, sizer_args)
##
##        # **************************************************************************

        parent.add_panel(self)
        self.update()
        self.finalize()

        def finalize():

##            blend_section.expand(False)
            self.expand(False)
            self.update_parent()

        wx.CallAfter(finalize)

        Mgr.add_app_updater("object_link_viz", self.__update_link_visibility)

    def get_clipping_rect(self):

        panel_rect = self.GetRect()
        width, height = panel_rect.size
        y_orig = self.GetParent().GetPosition()[1] + panel_rect.y
        clipping_rect = wx.Rect(0, -y_orig, *self.GetGrandParent().GetSize())

        return clipping_rect

    def setup(self):

        def enter_linking_mode(prev_state_id, is_active):

            Mgr.do("set_viewport_border_color", (255, 128, 255))
            self._btns["link"].set_active()

        def exit_linking_mode(next_state_id, is_active):

            if not is_active:
                self._btns["link"].set_active(False)

        add_state = Mgr.add_state
        add_state("object_linking_mode", -10, enter_linking_mode, exit_linking_mode)

    def __toggle_linking_mode(self):

        if self._btns["link"].is_active():
            Mgr.exit_state("object_linking_mode")
        else:
            Mgr.enter_state("object_linking_mode")

    def __unlink_objects(self):

        Mgr.update_remotely("object_unlinking")

    def __toggle_link_visibility(self):

        btn = self._btns["show_links"]

        if btn.is_active():
            btn.set_active(False)
        else:
            btn.set_active()

        Mgr.update_app("object_link_viz", btn.is_active())

    def __update_link_visibility(self, show):

        self._btns["show_links"].set_active(show)

##    def __toggle_material_name_editable(self):
##
##        combobox = self._comboboxes["material"]
##        editable = not combobox.is_editable()
##        combobox.set_editable(editable)
##        self._edit_mat_name_btn.set_active(editable)
##
##    def __toggle_layer_name_editable(self):
##
##        combobox = self._comboboxes["layer"]
##        editable = not combobox.is_editable()
##        combobox.set_editable(editable)
##        self._edit_layer_name_btn.set_active(editable)
##
##    def __extract_material(self):
##
##        Mgr.update_remotely("extracted_material")
##
##    def __create_material(self):
##
##        Mgr.update_remotely("new_material", None)
##
##    def __copy_material(self):
##
##        Mgr.update_remotely("new_material", self._selected_mat_id)
##
##    def __remove_material(self):
##
##        old_id = self._selected_mat_id
##        combobox = self._comboboxes["material"]
##        combobox.remove_item(self._selected_mat_id)
##        mat_id = combobox.get_selected_item()
##
##        Mgr.update_remotely("removed_material", old_id)
##
##        if mat_id:
##            name = combobox.get_item_label(mat_id)
##            self._fields["name"].set_value("name", name)
##            self._selected_mat_id = mat_id
##            self._comboboxes["layer"].clear()
##            Mgr.update_remotely("material_selection", mat_id)
##
##    def __clear_library(self):
##
##        self._selected_mat_id = None
##        self._comboboxes["material"].clear()
##
##        Mgr.update_remotely("cleared_material_lib")
##
##    def __handle_value(self, value_id, value):
##
##        mat_id = self._selected_mat_id
##
##        if value_id in ("shininess", "alpha"):
##            prop_data = {"value": value}
##            Mgr.update_remotely("material_prop", mat_id, value_id, prop_data)
##        else:
##            Mgr.update_remotely("material_prop", mat_id, value_id, value)
##
##    def __handle_layer_value(self, value_id, value):
##
##        mat_id = self._selected_mat_id
##        layer_id = self._selected_layer_id
##        prop_id = value_id.replace("layer_", "", 1)
##
##        Mgr.update_remotely("tex_layer_prop", mat_id, layer_id, prop_id, value)
##
##    def __get_color_handler(self, value_id):
##
##        def handle_color(color):
##
##            color_values = Mgr.convert_to_remote_format(
##                "color", color.Get() + (255,))
##            mat_id = self._selected_mat_id
##            prop_data = {"value": color_values}
##            Mgr.update_remotely("material_prop", mat_id, value_id, prop_data)
##
##        return handle_color
##
##    def __handle_layer_rgb(self, color):
##
##        color_values = Mgr.convert_to_remote_format(
##            "color", color.Get() + (255,))
##        alpha = float(self._fields["layer_alpha"].get_text("layer_alpha"))
##        color_values = color_values[:3] + [alpha]
##        mat_id = self._selected_mat_id
##        layer_id = self._selected_layer_id
##
##        Mgr.update_remotely("tex_layer_prop", mat_id,
##                            layer_id, "color", color_values)
##
##    def __handle_layer_alpha(self, value_id, value):
##
##        color = self._color_pickers["layer_rgb"].get_color()
##        color_values = Mgr.convert_to_remote_format(
##            "color", color.Get() + (255,))
##        color_values = color_values[:3] + [value]
##        mat_id = self._selected_mat_id
##        layer_id = self._selected_layer_id
##
##        Mgr.update_remotely("tex_layer_prop", mat_id,
##                            layer_id, "color", color_values)
##
##    def __handle_border_color(self, color):
##
##        color_values = Mgr.convert_to_remote_format(
##            "color", color.Get() + (255,))
##        mat_id = self._selected_mat_id
##
##        Mgr.update_remotely("material_prop", mat_id,
##                            "tex_map_border_color", color_values)
##
##    def __handle_layer_border_color(self, color):
##
##        color_values = Mgr.convert_to_remote_format(
##            "color", color.Get() + (255,))
##        mat_id = self._selected_mat_id
##        layer_id = self._selected_layer_id
##
##        Mgr.update_remotely("tex_layer_prop", mat_id,
##                            layer_id, "border_color", color_values)
##
##    def __get_color_toggler(self, value_id):
##
##        def toggle_color(on):
##
##            mat_id = self._selected_mat_id
##            prop_data = {"on": on}
##            Mgr.update_remotely("material_prop", mat_id, value_id, prop_data)
##
##        return toggle_color
##
##    def __toggle_tex_map(self, on):
##
##        mat_id = self._selected_mat_id
##        Mgr.update_remotely("material_prop", mat_id, "tex_map_on", on)
##
##    def __toggle_layers(self, on):
##
##        mat_id = self._selected_mat_id
##        Mgr.update_remotely("material_prop", mat_id, "layers_on", on)
##
##    def __toggle_layer(self, on):
##
##        mat_id = self._selected_mat_id
##        layer_id = self._selected_layer_id
##        Mgr.update_remotely("tex_layer_prop", mat_id, layer_id, "on", on)
##
##    def __toggle_wrap_lock(self, on):
##
##        mat_id = self._selected_mat_id
##        Mgr.update_remotely("material_prop", mat_id, "tex_map_wrap_lock", on)
##
##    def __toggle_layer_wrap_lock(self, on):
##
##        mat_id = self._selected_mat_id
##        layer_id = self._selected_layer_id
##        Mgr.update_remotely("tex_layer_prop", mat_id,
##                            layer_id, "wrap_lock", on)
##
##    def __toggle_layer_combine_channels(self, on):
##
##        mat_id = self._selected_mat_id
##        layer_id = self._selected_layer_id
##        prop_id = "combine_channels_use"
##        Mgr.update_remotely("tex_layer_prop", mat_id, layer_id, prop_id, on)
##
##    def __parse_name(self, name):
##
##        parsed_name = name.strip(" *")
##
##        return parsed_name if parsed_name else None
##
##    def __parse_shininess(self, shininess):
##
##        try:
##            return abs(float(eval(shininess)))
##        except:
##            return None
##
##    def __parse_alpha(self, alpha):
##
##        try:
##            return min(1., max(0., abs(float(eval(alpha)))))
##        except:
##            return None
##
##    def __set_material_property(self, mat_id, prop_id, value):
##
##        if prop_id == "name":
##            if self._selected_mat_id == mat_id:
##                self._fields[prop_id].set_value(prop_id, value)
##            self._comboboxes["material"].set_item_label(mat_id, value)
##        elif prop_id == "shininess":
##            self._fields[prop_id].set_value(prop_id, value["value"])
##        elif prop_id == "alpha":
##            self._checkboxes[prop_id].check(value["on"])
##            self._fields[prop_id].set_value(prop_id, value["value"])
##        elif prop_id in self._base_prop_ids:
##            self._checkboxes[prop_id].check(value["on"])
##            self._color_pickers[prop_id].set_color(value["value"])
##        elif prop_id == "layers_on":
##            self._checkboxes["layers"].check(value)
##        elif prop_id == "tex_map_select":
##            self._map_type = value
##            self._comboboxes["map_type"].select_item(value)
##        elif prop_id == "tex_map_on":
##            self._checkboxes["tex_map"].check(value)
##        elif prop_id == "tex_map_file_main":
##            self._tex_map_file_main = value
##            self._fields[prop_id].set_value(prop_id, value)
##        elif prop_id == "tex_map_file_alpha":
##            self._tex_map_file_alpha = value
##            self._fields[prop_id].set_value(prop_id, value)
##        elif prop_id == "tex_map_border_color":
##            self._color_pickers[prop_id].set_color(value)
##        elif prop_id == "tex_map_wrap_u":
##            self._comboboxes[prop_id].select_item(value)
##        elif prop_id == "tex_map_wrap_v":
##            self._comboboxes[prop_id].select_item(value)
##        elif prop_id == "tex_map_wrap_lock":
##            self._checkboxes[prop_id].check(value)
##        elif prop_id == "tex_map_filter_min":
##            self._comboboxes[prop_id].select_item(value)
##        elif prop_id == "tex_map_filter_mag":
##            self._comboboxes[prop_id].select_item(value)
##        elif prop_id == "tex_map_anisotropic_degree":
##            self._fields[prop_id].set_value(prop_id, value)
##        elif prop_id == "tex_map_transform":
##            u, v = value["offset"]
##            rot = value["rotate"][0]
##            su, sv = value["scale"]
##            self._fields["tex_map_offset_u"].set_value("tex_map_offset_u", u)
##            self._fields["tex_map_offset_v"].set_value("tex_map_offset_v", v)
##            self._fields["tex_map_rotate"].set_value("tex_map_rotate", rot)
##            self._fields["tex_map_scale_u"].set_value("tex_map_scale_u", su)
##            self._fields["tex_map_scale_v"].set_value("tex_map_scale_v", sv)
##        elif prop_id in ("tex_map_offset_u", "tex_map_offset_v", "tex_map_rotate",
##                         "tex_map_scale_u", "tex_map_scale_v"):
##            self._fields[prop_id].set_value(prop_id, value)
##        elif prop_id == "layers":
##            get_command = lambda layer_id: lambda: self.__select_layer(
##                layer_id)
##            for layer_id, name in value:
##                self._comboboxes["layer"].add_item(
##                    layer_id, name, get_command(layer_id))
##
##    def __select_material(self, mat_id):
##
##        combobox = self._comboboxes["material"]
##        combobox.select_item(mat_id)
##        name = combobox.get_item_label(mat_id)
##        self._fields["name"].set_value("name", name)
##        self._selected_mat_id = mat_id
##        self._comboboxes["layer"].clear()
##        Mgr.update_remotely("material_selection", mat_id)
##
##    def __update_new_material(self, mat_id, name="", select=True):
##
##        self._comboboxes["material"].add_item(
##            mat_id, name, lambda: self.__select_material(mat_id))
##
##        if select:
##            self.__select_material(mat_id)
##
##    def __apply_material(self):
##
##        Mgr.update_remotely("selected_obj_mat", self._selected_mat_id)
##
##    def __select_material_owners(self):
##
##        Mgr.update_remotely("material_owners", self._selected_mat_id)
##
##    def __check_texture_filename(self, filename):
##
##        return filename if (not filename or os.path.exists(filename)) else None
##
##    def __parse_texture_filename(self, filename):
##
##        return os.path.basename(filename) if filename else "<None>"
##
##    def __load_texture_file(self, map_type):
##
##        file_types = "Bitmap files (*.bmp;*.jpg;*.png)|*.bmp;*.jpg;*.png"
##        tex_filename = wx.FileSelector("Load %s texture map" % map_type,
##                                       "", "", "bitmap", file_types,
##                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
##                                       self)
##
##        return tex_filename
##
##    def __set_texture_map(self):
##
##        rgb_filename = self._tex_map_file_main
##        alpha_filename = self._tex_map_file_alpha
##        map_type = self._map_type
##        rgb_type, alpha_type = (map_type.split("+") + [""])[:2]
##
##        if rgb_filename and alpha_type and not alpha_filename:
##            return
##
##        mat_id = self._selected_mat_id
##        tex_data = {
##            "map_type": map_type,
##            "rgb_filename": rgb_filename,
##            "alpha_filename": alpha_filename
##        }
##        prop_data = {
##            "layer_id": None,
##            "tex_data": tex_data
##        }
##        Mgr.update_remotely("material_prop", mat_id, "texture", prop_data)
##
##    def __load_texture_map_main(self):
##
##        map_type = self._map_type
##        rgb_type, alpha_type = (map_type.split("+") + [""])[:2]
##        rgb_filename = self.__load_texture_file(rgb_type)
##
##        if not rgb_filename:
##            return
##
##        self._fields["tex_map_file_main"].set_value(
##            "tex_map_file_main", rgb_filename)
##        self._tex_map_file_main = rgb_filename
##        self.__set_texture_map()
##
##    def __load_texture_map_alpha(self):
##
##        map_type = self._map_type
##        rgb_type, alpha_type = (map_type.split("+") + [""])[:2]
##        alpha_filename = self.__load_texture_file(
##            alpha_type if alpha_type else "alpha")
##
##        if not alpha_filename:
##            return
##
##        self._fields["tex_map_file_alpha"].set_value(
##            "tex_map_file_alpha", alpha_filename)
##        self._tex_map_file_alpha = alpha_filename
##
##        if self._tex_map_file_main:
##            self.__set_texture_map()
##
##    def __init_main_filename_input(self):
##
##        field = self._fields["tex_map_file_main"]
##
##        if self._tex_map_file_main:
##            field.set_input_text(self._tex_map_file_main)
##        else:
##            field.clear()
##
##    def __init_alpha_filename_input(self):
##
##        field = self._fields["tex_map_file_alpha"]
##
##        if self._tex_map_file_alpha:
##            field.set_input_text(self._tex_map_file_alpha)
##        else:
##            field.clear()
##
##    def __set_texture_map_main(self, value_id, filename):
##
##        self._tex_map_file_main = filename
##        self.__set_texture_map()
##
##    def __set_texture_map_alpha(self, value_id, filename):
##
##        self._tex_map_file_alpha = filename
##
##        if self._tex_map_file_main:
##            self.__set_texture_map()
##
##    def __create_layer(self):
##
##        Mgr.update_remotely("new_tex_layer", self._selected_mat_id, None)
##
##    def __copy_layer(self):
##
##        Mgr.update_remotely(
##            "new_tex_layer", self._selected_mat_id, self._selected_layer_id)
##
##    def __remove_layer(self):
##
##        old_id = self._selected_layer_id
##        combobox = self._comboboxes["layer"]
##        combobox.remove_item(self._selected_layer_id)
##        layer_id = combobox.get_selected_item()
##
##        Mgr.update_remotely("removed_tex_layer", self._selected_mat_id, old_id)
##
##        if layer_id:
##            name = combobox.get_item_label(layer_id)
##            self._fields["layer_name"].set_value("layer_name", name)
##            self._selected_layer_id = layer_id
##            Mgr.update_remotely("tex_layer_selection",
##                                self._selected_mat_id, layer_id)
##
##    def __set_source_types(self, count):
##
##        combobox = self._comboboxes["layer_combine_source_index"]
##        combobox.clear()
##        labels = ("Primary", "Secondary", "Interpolation")
##        get_command = lambda index: lambda: Mgr.update_remotely("tex_layer_prop",
##                                                                self._selected_mat_id, self._selected_layer_id, "combine_source_index", index)
##
##        for i in range(count):
##            combobox.add_item(i, labels[i], get_command(i))
##
##    def __store_layer(self, on):
##
##        mat_id = self._selected_mat_id
##        layer_id = self._selected_layer_id
##        prop_id = "is_stored"
##        Mgr.update_remotely("tex_layer_prop", mat_id, layer_id, prop_id, on)
##
##    def __set_layer_property(self, layer_id, prop_id, value):
##
##        if self._selected_layer_id != layer_id:
##            return
##
##        val_id = "layer_" + prop_id
##
##        if prop_id == "name":
##            self._fields[val_id].set_value(val_id, value)
##            self._comboboxes["layer"].set_item_label(layer_id, value)
##        elif prop_id == "color":
##            self._color_pickers["layer_rgb"].set_color(value)
##            self._fields["layer_alpha"].set_value("layer_alpha", value[3])
##        elif prop_id == "rgb_scale":
##            self._radio_btns[val_id].set_selected_button(value)
##        elif prop_id == "alpha_scale":
##            self._radio_btns[val_id].set_selected_button(value)
##        elif prop_id == "on":
##            self._checkboxes[val_id].check(value)
##        elif prop_id == "file_main":
##            self._layer_file_main = value
##            self._fields[val_id].set_value(val_id, value)
##        elif prop_id == "file_alpha":
##            self._layer_file_alpha = value
##            self._fields[val_id].set_value(val_id, value)
##        elif prop_id == "sort":
##            self._fields[val_id].set_value(val_id, value)
##            self._comboboxes["layer"].set_item_index(layer_id, value)
##        elif prop_id == "priority":
##            self._fields[val_id].set_value(val_id, value)
##        elif prop_id == "border_color":
##            self._color_pickers[val_id].set_color(value)
##        elif prop_id == "wrap_u":
##            self._comboboxes[val_id].select_item(value)
##        elif prop_id == "wrap_v":
##            self._comboboxes[val_id].select_item(value)
##        elif prop_id == "wrap_lock":
##            self._checkboxes[val_id].check(value)
##        elif prop_id == "filter_min":
##            self._comboboxes[val_id].select_item(value)
##        elif prop_id == "filter_mag":
##            self._comboboxes[val_id].select_item(value)
##        elif prop_id == "anisotropic_degree":
##            self._fields[val_id].set_value(val_id, value)
##        elif prop_id == "uv_set":
##            self._fields[val_id].set_value(val_id, value)
##        elif prop_id == "transform":
##            u, v = value["offset"]
##            rot = value["rotate"][0]
##            su, sv = value["scale"]
##            self._fields["layer_offset_u"].set_value("layer_offset_u", u)
##            self._fields["layer_offset_v"].set_value("layer_offset_v", v)
##            self._fields["layer_rotate"].set_value("layer_rotate", rot)
##            self._fields["layer_scale_u"].set_value("layer_scale_u", su)
##            self._fields["layer_scale_v"].set_value("layer_scale_v", sv)
##        elif prop_id in ("offset_u", "offset_v", "rotate", "scale_u", "scale_v"):
##            self._fields[val_id].set_value(val_id, value)
##        elif prop_id == "blend_mode":
##            self._comboboxes[val_id].select_item(value)
##        elif prop_id == "combine_mode":
##            self._comboboxes[val_id].select_item(value)
##        elif prop_id == "combine_channels":
##            self._comboboxes[val_id].select_item(value)
##        elif prop_id == "combine_channels_use":
##            self._checkboxes[val_id].check(value)
##        elif prop_id == "combine_source_count":
##            self.__set_source_types(value)
##        elif prop_id == "combine_source_index":
##            self._comboboxes[val_id].select_item(value)
##        elif prop_id == "combine_source":
##            self._comboboxes[val_id].select_item(value)
##        elif prop_id == "combine_source_channels":
##            self._radio_btns[val_id].set_selected_button(value)
##        elif prop_id == "is_stored":
##            self._checkboxes[val_id].check(value)
##
##    def __select_layer(self, layer_id):
##
##        combobox = self._comboboxes["layer"]
##        combobox.select_item(layer_id)
##        name = combobox.get_item_label(layer_id)
##        self._fields["layer_name"].set_value("layer_name", name)
##        self._selected_layer_id = layer_id
##        Mgr.update_remotely("tex_layer_selection",
##                            self._selected_mat_id, layer_id)
##
##    def __update_new_layer(self, layer_id, name="", select=True):
##
##        self._comboboxes["layer"].add_item(
##            layer_id, name, lambda: self.__select_layer(layer_id))
##
##        if select:
##            self.__select_layer(layer_id)
##
##    def __set_layer(self):
##
##        rgb_filename = self._layer_file_main
##        alpha_filename = self._layer_file_alpha
##
##        mat_id = self._selected_mat_id
##        tex_data = {
##            "map_type": "layer",
##            "rgb_filename": rgb_filename,
##            "alpha_filename": alpha_filename
##        }
##        prop_data = {
##            "layer_id": self._selected_layer_id,
##            "tex_data": tex_data
##        }
##        Mgr.update_remotely("material_prop", mat_id, "texture", prop_data)
##
##    def __load_layer_main(self):
##
##        rgb_filename = self.__load_texture_file("color")
##
##        if not rgb_filename:
##            return
##
##        self._fields["layer_file_main"].set_value(
##            "layer_file_main", rgb_filename)
##        self._layer_file_main = rgb_filename
##        self.__set_layer()
##
##    def __load_layer_alpha(self):
##
##        alpha_filename = self.__load_texture_file("alpha")
##
##        if not alpha_filename:
##            return
##
##        self._fields["layer_file_alpha"].set_value(
##            "layer_file_alpha", alpha_filename)
##        self._layer_file_alpha = alpha_filename
##
##        if self._layer_file_main:
##            self.__set_layer()
##
##    def __init_layer_main_filename_input(self):
##
##        field = self._fields["layer_file_main"]
##
##        if self._layer_file_main:
##            field.set_input_text(self._layer_file_main)
##        else:
##            field.clear()
##
##    def __init_layer_alpha_filename_input(self):
##
##        field = self._fields["layer_file_alpha"]
##
##        if self._layer_file_alpha:
##            field.set_input_text(self._layer_file_alpha)
##        else:
##            field.clear()
##
##    def __set_layer_main(self, value_id, filename):
##
##        self._layer_file_main = filename
##        self.__set_layer()
##
##    def __set_layer_alpha(self, value_id, filename):
##
##        self._layer_file_alpha = filename
##
##        if self._layer_file_main:
##            self.__set_layer()

    def get_width(self):

        return self._width

    def get_client_width(self):

        return self._width - self.get_client_offset() * 2