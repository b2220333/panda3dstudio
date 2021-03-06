from ..base import *
from ..button import *
from ..panel import *


class HierarchyPanel(Panel):

    def __init__(self, stack):

        Panel.__init__(self, stack, "hierarchy", "Hierarchy")

        self._checkboxes = {}
        self._btns = {}
        self._toggle_btns = ToggleButtonGroup()
        toggle = (self.__set_xform_target_type, lambda: None)
        self._toggle_btns.set_default_toggle("all", toggle)

        # ********************** Object linking section ************************

        section = self.add_section("linking", "Object linking")

        subsizer = Sizer("horizontal")
        section.add(subsizer)

        checkbox = PanelCheckBox(section, self.__toggle_link_visibility)
        checkbox.check(False)
        self._checkboxes["show_links"] = checkbox
        borders = (0, 5, 0, 0)
        subsizer.add(checkbox, alignment="center_v", borders=borders)
        subsizer.add(PanelText(section, "Show links"), alignment="center_v")

        group = section.add_group("Link")
        subsizer = Sizer("horizontal")
        group.add(subsizer, alignment="center_v", expand=True)

        subsizer.add((0, 0), proportion=1.)

        text = "Selection"
        tooltip_text = "Link selected objects to target object"
        command = lambda: self.__toggle_linking_mode("sel_linking_mode")
        btn = PanelButton(group, text, "", tooltip_text, command)
        self._btns["sel_linking_mode"] = btn
        subsizer.add(btn, alignment="center_v")

        subsizer.add((0, 0), proportion=1.)

        text = "Pick..."
        tooltip_text = "Link single object to target object"
        command = lambda: self.__toggle_linking_mode("obj_linking_mode")
        btn = PanelButton(group, text, "", tooltip_text, command)
        self._btns["obj_linking_mode"] = btn
        subsizer.add(btn, alignment="center_v")

        subsizer.add((0, 0), proportion=1.)

        group = section.add_group("Unlink")
        subsizer = Sizer("horizontal")
        group.add(subsizer, alignment="center_v", expand=True)

        subsizer.add((0, 0), proportion=1.)

        text = "Selection"
        tooltip_text = "Unlink selected objects"
        command = self.__unlink_selection
        btn = PanelButton(group, text, "", tooltip_text, command)
        subsizer.add(btn, alignment="center_v")

        subsizer.add((0, 0), proportion=1.)

        text = "Pick..."
        tooltip_text = "Unlink single object"
        command = lambda: self.__toggle_linking_mode("obj_unlinking_mode")
        btn = PanelButton(group, text, "", tooltip_text, command)
        self._btns["obj_unlinking_mode"] = btn
        subsizer.add(btn, alignment="center_v")

        subsizer.add((0, 0), proportion=1.)

        subsizer = Sizer("horizontal")
        borders = (0, 0, 0, 10)
        section.add(subsizer, borders=borders)

        checkbox = PanelCheckBox(section, self.__toggle_group_member_linking)
        checkbox.check()
        self._checkboxes["group_member_linking_allowed"] = checkbox
        borders = (0, 5, 0, 0)
        subsizer.add(checkbox, alignment="center_v", borders=borders)
        text = "Affect group membership:"
        subsizer.add(PanelText(section, text), alignment="center_v")

        subsizer = Sizer("horizontal")
        borders = (20, 0, 0, 0)
        section.add(subsizer, borders=borders)

        checkbox = PanelCheckBox(section, self.__toggle_open_group_member_linking)
        checkbox.check()
        self._checkboxes["group_member_linking_open_groups_only"] = checkbox
        borders = (0, 5, 0, 0)
        subsizer.add(checkbox, alignment="center_v", borders=borders)
        text = "affect open groups only"
        subsizer.add(PanelText(section, text), alignment="center_v")

        subsizer = Sizer("horizontal")
        borders = (20, 0, 0, 0)
        section.add(subsizer, borders=borders)

        checkbox = PanelCheckBox(section, self.__toggle_group_member_unlink_only)
        checkbox.check()
        self._checkboxes["group_member_linking_unlink_only"] = checkbox
        borders = (0, 5, 0, 0)
        subsizer.add(checkbox, alignment="center_v", borders=borders)
        text = "unlink only"
        subsizer.add(PanelText(section, text), alignment="center_v")

        # ************************ Transforms section **************************

        disabler = lambda: GlobalData["active_obj_level"] != "top"

        section = self.add_section("transforms", "Transforms")

        sizer = GridSizer(rows=0, columns=2, gap_h=5, gap_v=5)
        section.add(sizer, expand=True)

        text = "Geom only"
        tooltip_text = "Transform geometry only"
        btn = PanelButton(section, text, "", tooltip_text)
        btn.add_disabler("subobj_lvl", disabler)
        toggle = (lambda: self.__set_xform_target_type("geom"), lambda: None)
        self._toggle_btns.add_button(btn, "geom", toggle)
        sizer.add(btn, proportion_h=1.)

        text = "Reset geom"
        tooltip_text = "Reset geometry to original transform"
        command = lambda: Mgr.update_app("geom_reset")
        btn = PanelButton(section, text, "", tooltip_text, command)
        btn.add_disabler("subobj_lvl", disabler)
        self._btns["reset_geom"] = btn
        sizer.add(btn, proportion_h=1.)

        text = "Pivot only"
        tooltip_text = "Transform pivot only"
        btn = PanelButton(section, text, "", tooltip_text)
        btn.add_disabler("subobj_lvl", disabler)
        toggle = (lambda: self.__set_xform_target_type("pivot"), lambda: None)
        self._toggle_btns.add_button(btn, "pivot", toggle)
        sizer.add(btn, proportion_h=1.)

        text = "Reset pivot"
        tooltip_text = "Reset pivot to original transform"
        command = lambda: Mgr.update_app("pivot_reset")
        btn = PanelButton(section, text, "", tooltip_text, command)
        btn.add_disabler("subobj_lvl", disabler)
        self._btns["reset_pivot"] = btn
        sizer.add(btn, proportion_h=1.)

        text = "Links only"
        tooltip_text = "Transform hierarchy links only"
        btn = PanelButton(section, text, "", tooltip_text)
        btn.add_disabler("subobj_lvl", disabler)
        toggle = (lambda: self.__set_xform_target_type("links"), lambda: None)
        self._toggle_btns.add_button(btn, "links", toggle)
        sizer.add(btn, proportion_h=1.)

        text = "No children"
        tooltip_text = "Don't transform child objects"
        btn = PanelButton(section, text, "", tooltip_text)
        btn.add_disabler("subobj_lvl", disabler)
        toggle = (lambda: self.__set_xform_target_type("no_children"), lambda: None)
        self._toggle_btns.add_button(btn, "no_children", toggle)
        sizer.add(btn, proportion_h=1.)

        # **********************************************************************

        def disable_xform_targets():

            self._toggle_btns.enable(False)
            self._btns["reset_geom"].enable(False)
            self._btns["reset_pivot"].enable(False)

        def enable_xform_targets():

            self._toggle_btns.enable()
            self._btns["reset_geom"].enable()
            self._btns["reset_pivot"].enable()

        Mgr.accept("disable_transform_targets", disable_xform_targets)
        Mgr.accept("enable_transform_targets", enable_xform_targets)
        Mgr.add_app_updater("object_link_viz", self.__update_link_visibility)
        Mgr.add_app_updater("group_options", self.__update_group_member_linking)
        Mgr.add_app_updater("transform_target_type", self.__update_xform_target_type)

    def __update_group_member_linking(self):

        for option, value in GlobalData["group_options"]["member_linking"].items():
            self._checkboxes["group_member_linking_{}".format(option)].check(value)

    def setup(self):

        def enter_linking_mode(prev_state_id, is_active):

            Mgr.do("set_viewport_border_color", "viewport_frame_link_objects")
            self._btns[GlobalData["object_linking_mode"]].set_active()

        def exit_linking_mode(next_state_id, is_active):

            if not is_active:
                self._btns[GlobalData["object_linking_mode"]].set_active(False)

        add_state = Mgr.add_state
        add_state("object_linking_mode", -10, enter_linking_mode, exit_linking_mode)

        self.get_section("transforms").expand(False)
        self.expand(False)

    def __toggle_linking_mode(self, linking_mode):

        current_linking_mode = GlobalData["object_linking_mode"]

        if current_linking_mode and current_linking_mode != linking_mode:
            Mgr.exit_state("object_linking_mode")

        if self._btns[linking_mode].is_active():
            Mgr.exit_state("object_linking_mode")
            GlobalData["object_linking_mode"] = ""
        else:
            GlobalData["object_linking_mode"] = linking_mode
            Mgr.enter_state("object_linking_mode")

    def __unlink_selection(self):

        Mgr.update_remotely("selection_unlinking")

    def __toggle_link_visibility(self, links_shown):

        GlobalData["object_links_shown"] = links_shown
        Mgr.update_remotely("object_link_viz")

    def __update_link_visibility(self):

        links_shown = GlobalData["object_links_shown"]
        self._checkboxes["show_links"].check(links_shown)

    def __toggle_group_member_linking(self, allowed):

        GlobalData["group_options"]["member_linking"]["allowed"] = allowed

    def __toggle_open_group_member_linking(self, open_groups_only):

        GlobalData["group_options"]["member_linking"]["open_groups_only"] = open_groups_only

    def __toggle_group_member_unlink_only(self, unlink_only):

        GlobalData["group_options"]["member_linking"]["unlink_only"] = unlink_only

    def __set_xform_target_type(self, target_type="all"):

        GlobalData["transform_target_type"] = target_type
        Mgr.update_app("transform_target_type")

    def __update_xform_target_type(self):

        target_type = GlobalData["transform_target_type"]

        if target_type == "all":
            self._toggle_btns.deactivate()
        else:
            self._toggle_btns.set_active_button(target_type)
