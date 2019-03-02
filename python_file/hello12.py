"""请利用@property给一个Screen对象加上width和height属性，以及一个只读属性resolution."""

# -*- coding: utf-8 -*-


class Screen(object):
    """."""

    @property
    def width(self):
        """."""
        return self._width or 0

    @width.setter
    def width(self, width):
        """."""
        if not isinstance(width, int) or width < 0:
            return ValueError('width must be an integer not less than 0!')
        else:
            self._width = width

    @property
    def height(self):
        """."""
        return self._height or 0

    @height.setter
    def height(self, height):
        """."""
        if not isinstance(height, int) or height < 0:
            return ValueError('height must be an integer not less than 0!')
        else:
            self._height = height

    @property
    def resolution(self):
        """."""
        if isinstance(self._width, int) and isinstance(self._height, int):
            return self._width * self._height
        else:
            return 0


# 测试:
s = Screen()
s.width = 1024
s.height = 768
print('width =', s.width)
print('height =', s.height)
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')
