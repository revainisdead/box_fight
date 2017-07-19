import pygame as pg

from .. import const, setup

from .. components import camera
from .. engine import calc


class MapDef:
    """ Map Definition """
    def __init__(self) -> None:
        self.surface = pg.Surface((setup.screen_size.get_width(), setup.screen_size.get_height())).convert()
        self.verts = (-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1)
        self.faces = (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
        self.colors = (255, 0, 0), (255, 128, 0), (255, 255, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0)


    def render(self, dt) -> None:
        """ Draw current shapes onto surface """
        self.surface.fill(const.BLACK)

        vert_list = []
        screen_points = []
        for x, y, z in self.verts:
            # Translate all verts through camera
            x -= camera.CAM.pos[0]
            y -= camera.CAM.pos[1]
            z -= camera.CAM.pos[2]

            # Rotate on the y axis first, then on the x axis.
            x, z = calc.rotate2d((x, z), camera.CAM.rot[1])
            y, z = calc.rotate2d((y, z), camera.CAM.rot[0])
            vert_list += [(x, y, z)]

            # Handle sensitivity of mouse point
            f = (setup.screen_size.get_width()/2)/z

            x, y = x*f, y*f
            screen_points += [(int(setup.screen_size.get_width()/2 + int(x)), int(setup.screen_size.get_height()/2 + int(y)))]

        face_list = []
        face_color = []
        depth = []
        for f in range(len(self.faces)):
            face = self.faces[f]

            on_screen = False
            for ea in face:
                x, y = screen_points[ea]
                if vert_list[ea][2] > 0 and x>0 and x<setup.screen_size.get_width() and y>0 and y<setup.screen_size.get_height():
                    on_screen = True
                    break

            if on_screen:
                points = [screen_points[ea] for ea in face]
                face_list += [points]
                face_color += [self.colors[f]]

                # Depth formula.
                depth += [sum(sum(vert_list[j][i] for j in face)**2 for i in range(3))]


        # Create order to iterate over face list for drawing based on the depth formula
        order = sorted(range(len(face_list)), key=lambda i: depth[i], reverse=True)

        for i in order:
            try:
                pg.draw.polygon(self.surface, face_color[i], face_list[i])
            except Exception as e:
                print("exception drawing polygon: {}".format(e))


    def update(self, dt) -> pg.Surface:
        """ Render and then return updated surface """
        self.update_surf()
        self.render(dt)
        return self.surface


    def update_surf(self) -> None:
        if setup.screen_size.changed():
            self.surface = pg.Surface((setup.screen_size.get_width(), setup.screen_size.get_height())).convert()

