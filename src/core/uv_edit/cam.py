from .base import *


class PickingCamera(BaseObject):

    def __init__(self):

        self._tex = None
        self._img = None
        self._buffer = None
        self._np = None
        self._mask = BitMask32.bit(25)

        self._pixel_color = VBase4()

        UVMgr.expose("picking_mask", lambda: self._mask)
        UVMgr.expose("pixel_under_mouse", lambda: self._pixel_color)
        UVMgr.expose("picking_cam", lambda: self)
        UVMgr.expose("picked_point", self.__get_picked_point)

    def setup(self):

        core = Mgr.get("core")
        self._tex = Texture("uv_picking_texture")
        self._img = PNMImage(1, 1)
        props = FrameBufferProperties()
        props.set_float_color(True)
        props.set_alpha_bits(True)
        self._buffer = core.win.make_texture_buffer("uv_picking_buffer",
                                                    1, 1,
                                                    self._tex,
                                                    to_ram=True,
                                                    fbp=props)

        self._buffer.set_clear_color(VBase4())
        self._buffer.set_sort(-100)
        self._np = core.make_camera(self._buffer)
        self._np.reparent_to(self.cam)
        node = self._np.node()
        lens = OrthographicLens()
        size = self.cam_lens.get_film_size()[0] / 600.
        lens.set_film_size(size)
        node.set_lens(lens)
        node.set_camera_mask(self._mask)

        state_np = NodePath("uv_vertex_color_state")
        state_np.set_texture_off(1)
        state_np.set_material_off(1)
        state_np.set_shader_off(1)
        state_np.set_light_off(1)
        state_np.set_color_off(1)
        state_np.set_color_scale_off(1)
        state_np.set_render_mode_thickness(10, 1)
        state_np.set_transparency(TransparencyAttrib.M_none, 1)
        node.set_initial_state(state_np.get_state())
        node.set_active(False)

        return "uv_picking_camera_ok"

    def set_active(self, is_active=True):

        if is_active:
            Mgr.add_task(self.__check_pixel,
                         "get_uv_pixel_under_mouse", sort=0)
        else:
            Mgr.remove_task("get_uv_pixel_under_mouse")

        self._np.node().set_active(is_active)

    def __check_pixel(self, task):

        if not self.mouse_watcher.has_mouse():
            return task.cont

        film_size = self.cam_lens.get_film_size()[0]
        x, z = self.mouse_watcher.get_mouse() * film_size * .5
        self._np.set_pos(x, 0., z)
        self._tex.store(self._img)
        self._pixel_color = p = self._img.get_xel_a(0, 0)

        return task.cont

    def __get_picked_point(self):

        pos = self._np.get_pos(self.uv_space)
        pos[1] = 0.

        return pos


class UVNavigationBase(BaseObject):

    def __init__(self):

        self._pan_start_pos = Point3()

    def setup(self):

        add_state = Mgr.add_state
        add_state("panning", -100, interface_id="uv_window")
        add_state("zooming", -100, interface_id="uv_window")

        def start_panning():

            Mgr.enter_state("panning", "uv_window")
            self.__init_pan()

        def start_zooming():

            Mgr.enter_state("zooming", "uv_window")
            self.__init_zoom()

        def end_cam_transform():

            Mgr.enter_state("uv_edit_mode", "uv_window")
            Mgr.remove_task("transform_uv_cam")

        bind = Mgr.bind_state
        bind("uv_edit_mode", "edit uvs -> pan",
             "mouse3", start_panning, "uv_window")
        bind("panning", "pan -> edit uvs", "mouse3-up",
             end_cam_transform, "uv_window")
        bind("panning", "pan -> zoom", "mouse1", start_zooming, "uv_window")
        bind("zooming", "zoom -> pan", "mouse1-up", start_panning, "uv_window")
        bind("zooming", "zoom -> edit uvs", "mouse3-up",
             end_cam_transform, "uv_window")
        bind("uv_edit_mode", "zoom in", "wheel_up",
             self.__zoom_step_in, "uv_window")
        bind("uv_edit_mode", "zoom out", "wheel_down",
             self.__zoom_step_out, "uv_window")
        bind("uv_edit_mode", "reset view", "home",
             self._reset_view, "uv_window")

    def _reset_view(self):

        self.cam.set_pos(.5, -10., .5)
        self.cam.set_scale(1.)
        self._grid.update()
        self._transf_gizmo.set_scale(self.cam.get_sx())

    def __init_pan(self):

        Mgr.remove_task("transform_uv_cam")

        if not self.mouse_watcher.has_mouse():
            return

        self.__get_pan_pos(self._pan_start_pos)
        Mgr.add_task(self.__pan, "transform_uv_cam", sort=2)

    def __pan(self, task):

        pan_pos = Point3()

        if not self.__get_pan_pos(pan_pos):
            return task.cont

        self.cam.set_pos(self.cam.get_pos() + (self._pan_start_pos - pan_pos))
        self._grid.update()
        self._transf_gizmo.set_scale(self.cam.get_sx())

        return task.cont

    def __get_pan_pos(self, pos):

        if not self.mouse_watcher.has_mouse():
            return False

        pos.x, unused, pos.z = UVMgr.get("picked_point")

        return True

    def __init_zoom(self):

        Mgr.remove_task("transform_uv_cam")

        if not self.mouse_watcher.has_mouse():
            return

        self._zoom_start = (self.cam.get_sx(),
                            self.mouse_watcher.get_mouse_y())
        Mgr.add_task(self.__zoom, "transform_uv_cam", sort=2)

    def __zoom(self, task):

        if not self.mouse_watcher.has_mouse():
            return task.cont

        mouse_y = self.mouse_watcher.get_mouse_y()
        start_scale, start_y = self._zoom_start

        if mouse_y < start_y:
            # zoom out
            zoom = 1. + start_y - mouse_y
        else:
            # zoom in
            zoom = 1. / (1. + mouse_y - start_y)

        zoom *= start_scale
        zoom = min(1000., max(.001, zoom))
        self.cam.set_scale(zoom, 1., zoom)
        self._grid.update()
        self._transf_gizmo.set_scale(self.cam.get_sx())

        return task.cont

    def __zoom_step_in(self):

        zoom = self.cam.get_sx() * .9
        zoom = max(.001, zoom)
        self.cam.set_scale(zoom, 1., zoom)
        self._grid.update()
        self._transf_gizmo.set_scale(self.cam.get_sx())

    def __zoom_step_out(self):

        zoom = self.cam.get_sx() * 1.1
        zoom = min(1000., zoom)
        self.cam.set_scale(zoom, 1., zoom)
        self._grid.update()
        self._transf_gizmo.set_scale(self.cam.get_sx())


class UVTemplateSaver(BaseObject):

    def __init__(self):

        self._template_mask = BitMask32.bit(26)
        self._size = 512
        self._edge_color = VBase4(1., 1., 1., 1.)
        self._poly_color = VBase4(1., 1., 1., 0.)
        UVMgr.expose("template_mask", lambda: self._template_mask)

        def update_remotely():

            Mgr.update_interface_remotely(
                "uv_window", "uv_template", "size", self._size)
            r, g, b, a = self._edge_color
            Mgr.update_interface_remotely(
                "uv_window", "uv_template", "edge_rgb", (r, g, b))
            Mgr.update_interface_remotely(
                "uv_window", "uv_template", "edge_alpha", a)
            r, g, b, a = self._poly_color
            Mgr.update_interface_remotely(
                "uv_window", "uv_template", "poly_rgb", (r, g, b))
            Mgr.update_interface_remotely(
                "uv_window", "uv_template", "poly_alpha", a)

        UVMgr.accept("remotely_update_template_props", update_remotely)

    def add_interface_updaters(self):

        Mgr.add_interface_updater(
            "uv_window", "uv_template", self.__update_uv_template)

    def __update_uv_template(self, value_id, value=None):

        if value_id == "size":
            self._size = value
        elif value_id == "edge_rgb":
            for i in range(3):
                self._edge_color[i] = value[i]
        elif value_id == "edge_alpha":
            self._edge_color[3] = value
        elif value_id == "poly_rgb":
            for i in range(3):
                self._poly_color[i] = value[i]
        elif value_id == "poly_alpha":
            self._poly_color[3] = value
        elif value_id == "save":
            self.__save_uv_template(value)

        if value_id != "save":
            Mgr.update_interface_remotely(
                "uv_window", "uv_template", value_id, value)

    def __save_uv_template(self, filename):

        res = self._size
        core = Mgr.get("core")
        tex = Texture("uv_template")
        props = FrameBufferProperties()
        props.set_float_color(True)
        props.set_alpha_bits(True)
        tex_buffer = core.win.make_texture_buffer("uv_template_buffer",
                                                  res, res,
                                                  tex,
                                                  to_ram=True,
                                                  fbp=props)

        tex_buffer.set_clear_color(VBase4())
        cam = core.make_camera(tex_buffer)
        cam.reparent_to(self.uv_space)
        cam.set_pos(.5, -10., .5)
        node = cam.node()
        node.set_camera_mask(self._template_mask)
        lens = OrthographicLens()
        lens.set_film_size(1.)
        node.set_lens(lens)
        node.set_tag_state_key("uv_template")

        state_np = NodePath("uv_template_edge_state")
        state_np.set_texture_off()
        state_np.set_material_off()
        state_np.set_shader_off()
        state_np.set_light_off()
        state_np.set_color(self._edge_color)
        state_np.set_transparency(TransparencyAttrib.M_alpha)
        node.set_tag_state("edge", state_np.get_state())

        state_np = NodePath("uv_template_poly_state")
        state_np.set_texture_off()
        state_np.set_material_off()
        state_np.set_shader_off()
        state_np.set_light_off()
        state_np.set_two_sided(True)
        state_np.set_color(self._poly_color)
        state_np.set_transparency(TransparencyAttrib.M_alpha)
        node.set_tag_state("poly", state_np.get_state())

        Mgr.render_frame()
        tex.write(filename)
        cam.remove_node()
        core.graphicsEngine.remove_window(tex_buffer)


MainObjects.add_class(PickingCamera, "uv_window")