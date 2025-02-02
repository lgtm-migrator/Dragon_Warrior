from src.config import TILE_SIZE


class Camera:
    def __init__(self, hero_position, current_map, screen):
        self.current_map = current_map
        self.x = None
        self.y = None
        self.screen = screen
        self.set_camera_position(hero_position)

    def set_camera_position(self, hero_position: tuple):
        """
        Sets the camera position.
        :type hero_position: tuple
        :param hero_position: Position of the hero, in (column, row) format.
        """
        column, row = hero_position
        if self.screen:
            self.x = (-column + (self.screen.get_width() / TILE_SIZE / 2)) * TILE_SIZE
            self.y = (-row + (self.screen.get_height() / TILE_SIZE // 2)) * TILE_SIZE
        else:
            self.x = (-column + 8) * TILE_SIZE
            self.y = (-row + 7) * TILE_SIZE

    def get_pos(self) -> tuple:
        """
        Gets the position of a particular rectangle.
        """
        return self.x, self.y

    def set_pos(self, coord):
        """
        Sets the position of a particular rectangle.
        """
        self.x = coord[0]
        self.y = coord[1]
        # TODO: Investigate Python getters/setters (prop and props live templates?)

    # TODO: Migrate game move method here.
