from .base import *


class Text(Widget):

    def __init__(self, parent, font, color, text):

        self._type = "widget"
        self._widget_type = "text"
        self._parent = parent
        self._font = font
        self._color = color
        self._text = text
        self._node = parent.get_node().attach_new_node("text_widget")
        self._image_offset = (0, 0)

        self._image = img = self.__create_image(text)
        self._size = self._min_size = (img.get_x_size(), img.get_y_size())
        self._sizer = None
        self._sizer_item = None
        self._stretch_dir = ""
        self._mouse_region = None
        self._is_hidden = False

    def destroy(self):

        if self._node:
            self._node.remove_node()
            self._node = None

        self._parent = None
        self._sizer = None
        self._sizer_item = None

    def post_process_image(self, image):
        """ Override in derived class """

        return image

    def __create_image(self, text):

        font = self._font
        color = self._color
        lines = text.split("\n")
        line_count = len(lines)

        if line_count == 1:
            return self.post_process_image(font.create_image(text, color))

        line_imgs = []
        line_spacing = font.get_line_spacing()
        width = 0

        for line in lines:
            line_img = font.create_image(line, color)
            line_imgs.append(line_img)
            width = max(width, line_img.get_x_size())

        img = PNMImage(width, line_spacing * (line_count - 1) + font.get_height(), 4)

        for i, line_img in enumerate(line_imgs):
            img.copy_sub_image(line_img, 0, i * line_spacing, 0, 0)

        return self.post_process_image(img)

    def set_text(self, text, force=False):

        if not text or (not force and self._text == text):
            return False

        self._text = text

        self._image = img = self.__create_image(text)
        self._size = self._min_size = (img.get_x_size(), img.get_y_size())

        return True

    def get_text(self):

        return self._text

    def set_font(self, font, update=True):

        self._font = font

        if update:
            self._image = img = self.__create_image(self._text)
            self._size = self._min_size = (img.get_x_size(), img.get_y_size())

    def get_font(self):

        return self._font

    def set_color(self, color, update=True):

        self._color = color

        if update:
            self._image = img = self.__create_image(self._text)
            self._size = self._min_size = (img.get_x_size(), img.get_y_size())

    def get_color(self):

        return self._color

    def set_size(self, size, includes_borders=True, is_min=False):

        self._size = size

        if is_min:
            self._min_size = size

        return size

    def get_outer_borders(self):

        return (0, 0, 0, 0)

    def update_images(self, recurse=True, size=None): pass

    def get_image(self, state=None, composed=True):

        return PNMImage(self._image)

    def enable(self, enable=True): pass


class Label(Widget):

    def __init__(self, parent, font, text_color, back_color, edge_color, text,
                 text_borders=None, edge_borders=None, stretch_dir=""):

        self._type = "widget"
        self._widget_type = "label"
        self._parent = parent
        self._font = font
        self._text_color = text_color
        self._back_color = back_color
        self._edge_color = edge_color
        self._text = text
        self._node = parent.get_node().attach_new_node("label_widget")
        self._size = self._min_size = (0, 0)
        self._image_offset = (0, 0)
        self._text_borders = text_borders if text_borders else (0, 0, 0, 0)
        self._edge_borders = edge_borders if edge_borders else (0, 0, 0, 0)

        self._image = img = self.__create_image(text)
        self._size = self._min_size = (img.get_x_size(), img.get_y_size())
        self._sizer = None
        self._sizer_item = None
        self._stretch_dir = stretch_dir

        self._mouse_region = None
        self._is_hidden = False

    def destroy(self):

        if self._node:
            self._node.remove_node()
            self._node = None

        self._parent = None
        self._sizer = None
        self._sizer_item = None

    def post_process_image(self, image):
        """ Override in derived class """

        return image

    def __create_image(self, text):

        font = self._font
        text_color = self._text_color
        back_color = self._back_color
        edge_color = self._edge_color
        lines = text.split("\n")
        line_count = len(lines)

        if line_count == 1:

            img = font.create_image(text, text_color)

        else:

            line_imgs = []
            line_spacing = font.get_line_spacing()
            width = 0

            for line in lines:
                line_img = font.create_image(line, text_color)
                line_imgs.append(line_img)
                width = max(width, line_img.get_x_size())

            img = PNMImage(width, line_spacing * (line_count - 1) + font.get_height(), 4)

            for i, line_img in enumerate(line_imgs):
                img.copy_sub_image(line_img, 0, i * line_spacing, 0, 0)

        l_e, r_e, b_e, t_e = self._edge_borders
        l_t, r_t, b_t, t_t = self._text_borders
        w, h = self._size
        w_text = img.get_x_size()
        h_text = img.get_y_size()
        w = max(w, w_text + l_e + r_e + l_t + r_t)
        h = max(h, h_text + b_e + t_e + b_t + t_t)
        image = PNMImage(w, h, 4)
        r, g, b, a = edge_color
        image.fill(r, g, b)
        image.alpha_fill(a)
        w -= l_e + r_e
        h -= b_e + t_e
        inner_image = PNMImage(w, h, 4)
        r, g, b, a = back_color
        inner_image.fill(r, g, b)
        inner_image.alpha_fill(a)
        x = (w - w_text) // 2
        y = (h - h_text) // 2
        inner_image.blend_sub_image(img, x, y, 0, 0)
        image.copy_sub_image(inner_image, l_e, t_e, 0, 0)

        return self.post_process_image(image)

    def set_text(self, text, force=False):

        if not text or (not force and self._text == text):
            return False

        self._text = text

        self._image = img = self.__create_image(text)
        self._size = self._min_size = (img.get_x_size(), img.get_y_size())

        return True

    def get_text(self):

        return self._text

    def set_font(self, font):

        self._font = font

    def get_font(self):

        return self._font

    def set_text_color(self, color):

        self._text_color = color

    def get_text_color(self):

        return self._text_color

    def set_back_color(self, color):

        self._back_color = color

    def get_back_color(self):

        return self._back_color

    def set_edge_color(self, color):

        self._edge_color = color

    def get_edge_color(self):

        return self._edge_color

    def set_size(self, size, includes_borders=True, is_min=False):

        self._size = size

        if is_min:
            self._min_size = size

        return size

    def get_outer_borders(self):

        return (0, 0, 0, 0)

    def update_images(self, recurse=True, size=None):

        self._image = self.__create_image(self._text)

    def get_image(self, state=None, composed=True):

        return PNMImage(self._image)

    def enable(self, enable=True): pass
