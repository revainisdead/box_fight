import pygame as pg

from .. import const, setup

from .. components import camera, shape
from .. engine import calc


class MapDef:
    """ Map Definition """
    def __init__(self) -> None:
        self.surface = pg.Surface((setup.screen_size.get_width(), setup.screen_size.get_height())).convert()
        self.cubes = [shape.Cube((0, 4, 0)), shape.Cube((0, 6, 0)), shape.Cube((0, 8, 0)), shape.Floor()]

        for cube in self.cubes:
            print(cube.verts)


    def render(self, dt) -> None:
        """ Draw current shapes onto surface """
        self.surface.fill(const.BLACK)

        face_list = []
        face_color = []
        depth = []

        for cube in self.cubes:
            vert_list = []
            screen_points = []
            for x, y, z in cube.verts:
                # Translate all verts through camera
                x -= camera.CAM.pos[0]
                y -= camera.CAM.pos[1]
                z -= camera.CAM.pos[2]

                # Rotate on the y axis first, then on the x axis.
                x, z = calc.rotate2d((x, z), camera.CAM.rot[1]*const.RADIAN_MULT)
                y, z = calc.rotate2d((y, z), camera.CAM.rot[0]*const.RADIAN_MULT)
                vert_list += [(x, y, z)]

                # Handle sensitivity of mouse point
                try:
                    f = (setup.screen_size.get_width()/2 - const.FOV_DELTA)/z
                except ZeroDivisionError:
                    print("Point for map is incorrect, got 0 for z: ({}, {}, {})".format(x, y, z))

                x, y = x*f, y*f
                screen_points += [(int(setup.screen_size.get_width()/2 + int(x)), int(setup.screen_size.get_height()/2 + int(y)))]

            for f in range(len(cube.faces)):
                face = cube.faces[f]

                on_screen = False
                for ea in face:
                    x, y = screen_points[ea]
                    if vert_list[ea][2] > 0 and x>0 and x<setup.screen_size.get_width() and y>0 and y<setup.screen_size.get_height():
                        on_screen = True
                        break

                if on_screen:
                    points = [screen_points[ea] for ea in face]
                    face_list += [points]
                    face_color += [cube.colors[f]]

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

