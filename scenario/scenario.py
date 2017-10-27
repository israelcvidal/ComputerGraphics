class Scenario(object):
    def __init__(self, objects=[], light_sources=[], po=None, look_at=None, avup=None):
        """

        :param objects: list of all objects on the scenario
        :param light_sources: list of all light sources on the scenario
        :param po: observer(camera) location on world coordination
        :param look_at: loot at point
        :param avup: view up point
        """
        self.objects = objects
        self.light_sources = light_sources
        self.po = po
        self.look_at = look_at
        self.avup = avup

    def ray_casting(self, window_width, window_height, window_distance, pixels_width, pixels_height):
        """

        :param window_width: width of window to open on the plane
        :param window_height: height of window to open on the plane
        :param window_distance: distance of the plane where the window will be opened at
        :param pixels_width: number of pixels we will have on width direction
        :param pixels_height: number of pixels we will have on height direction
        :return: matrix rgb to be rendered
        """
        pass

    def render(self):
        pass

    def transform_to_camera(self):
        # transform all objects to camera
        pass

    def transform_to_world(self):
        # transform all objects to world
        pass


class LightSource(object):
    pass


class PunctualLightSource(LightSource):
    pass


class SpotLightSource(LightSource):
    pass


class InfinityLightSource(LightSource):
    pass
