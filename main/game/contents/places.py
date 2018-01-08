class Coordinates(object):
    """Stores coordinates of an object relative to its container"""

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def set_x(self, x):
        self.x = x

    def set_z(self, z):
        self.z = z

    def set_y(self, y):
        self.y = y


class Dimensions(object):
    """Stores absolute dimensions of an object"""

    def __init__(self, x=1, z=1, y=1):
        self.x = x
        self.z = z
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_z(self, z):
        self.z = z

    def set_y(self, y):
        self.y = y


class SpatialObject(object):
    """Stores a name, dimensions, and coordinates for an object"""

    def __init__(self, object=None, name=None, dimensions=None,
                 coordinates=None):
        self.name = name  # TODO: Generate names
        self.objects = []

        if dimensions is list:
            self.dimensions = Dimensions(dimensions[0], dimensions[1],
                                         dimensions[2])
        else:
            self.dimensions = dimensions
        if coordinates is list:
            self.coordinates = Coordinates(coordinates[0], coordinates[1],
                                           coordinates[2])
        else:
            self.coordinates = coordinates

    def add_object(self, object):
        self.objects.append(object)

    def set_objects(self, objects):
        self.objects = objects

    def set_x_coordinate(self, x):
        self.coordinates.x = x

    def set_z_coordinate(self, z):
        self.coordinates.x = z

    def set_y_coordinate(self, y):
        self.coordinates.x = y

    def set_x_dimension(self, x):
        self.dimensions.x = x

    def set_z_dimension(self, z):
        self.dimensions.x = z

    def set_y_dimension(self, y):
        self.dimensions.x = y
