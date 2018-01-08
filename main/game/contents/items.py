class Volume(object):
    """Store x, z, and y values to determine volume"""

    def __init__(self, x, z, y):
        self.x = x
        self.z = z
        self.y = y

    def get_total_space(self):
        return self.x * self.z * self.y

    def get_volume_array(self):
        return [self.x, self.z, self.y]


class Item(Volume):
    def __init__(self, name, x, z, y):
        Volume.__init__(self, x, z, y)
        self.name = name


class Container(Item):
    """Stores items based on volume"""

    def __init__(self, name, x, z, y):
        Item.__init__(self, name, x, z, y)
        self.items = []

    def get_available_space(self):
        """Returns the available space"""
        used_volume = 0
        for item in self.items:
            used_volume += item.get_total_space()
        return self.get_total_space() - used_volume

    def can_fit(self, item):
        """Checks whether an item can be rotated to fit in the boundaries of the
        container.
        """
        volume_array = sorted(self.get_volume_array())
        for value in sorted(item.get_volume_array()):
            for own_value in volume_array:
                if value < own_value:
                    volume_array.remove(own_value)
                    break
                return False
        return True

    def can_add(self, item):
        """Checks if the item can fit and if there's enough space left"""
        if self.can_fit(
                item) and item.get_total_space() < self.get_available_space():
            return True
        return False

    def add(self, item):
        """Adds an item if possible"""
        if self.can_add(item):
            self.items.append(item)
            return True
        return False
