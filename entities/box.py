from pygame import Rect


class Box:

    def __init__(self, x: float, y: float, width: float, height: float):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.x = value

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.x = value - self.width

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value):
        self.y = value

    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, value):
        self.y = value - self.height

    @property
    def center(self):
        return self.x + self.width / 2, self.y + self.height / 2

    @center.setter
    def center(self, value):
        self.x = value[0] - self.width / 2
        self.y = value[1] - self.height / 2

    @property
    def center_x(self):
        return self.x + self.width / 2

    @center_x.setter
    def center_x(self, value):
        self.x = value - self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    @center_y.setter
    def center_y(self, value):
        self.y = value - self.height / 2

    @property
    def topleft(self):
        return self.x, self.y

    @topleft.setter
    def topleft(self, value):
        self.x, self.y = value

    @property
    def topright(self):
        return self.right, self.y

    @topright.setter
    def topright(self, value):
        self.x = value[0] - self.width
        self.y = value[1]

    @property
    def bottomleft(self):
        return self.x, self.bottom

    @bottomleft.setter
    def bottomleft(self, value):
        self.x, self.y = value[0], value[1] - self.height

    @property
    def bottomright(self):
        return self.right, self.bottom

    @bottomright.setter
    def bottomright(self, value):
        self.x = value[0] - self.width
        self.y = value[1] - self.height

    @property
    def midleft(self):
        return self.x, self.center_y

    @midleft.setter
    def midleft(self, value):
        self.x, self.y = value[0], value[1] - self.height / 2

    @property
    def midright(self):
        return self.right, self.center_y

    @midright.setter
    def midright(self, value):
        self.x, self.y = value[0] - self.width, value[1] - self.height / 2

    @property
    def midtop(self):
        return self.center_x, self.y

    @midtop.setter
    def midtop(self, value):
        self.x, self.y = value[0] - self.width / 2, value[1]

    @property
    def midbottom(self):
        return self.center_x, self.bottom

    @midbottom.setter
    def midbottom(self, value):
        self.x, self.y = value[0] - self.width / 2, value[1] - self.height

    @property
    def size(self):
        return self.width, self.height

    @size.setter
    def size(self, value):
        self.width, self.height = value

    @property
    def rect(self) -> Rect:
        return Rect(self.x, self.y, self.width, self.height)

    @rect.setter
    def rect(self, value: Rect):
        self.x, self.y, self.width, self.height = value

    def __repr__(self):
        return "Box({}, {}, {}, {})".format(self.x, self.y, self.width, self.height)
