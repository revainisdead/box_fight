import pygame
import math
import sys

from ..components import camera


def rotate2d(pos, rad):
    x, y = pos
    s = math.sin(rad)
    c = math.cos(rad)

    #x = x*cos - y*sin
    #y = y*cos + x*sin
    return x*c - y*s, y*c + x*s


pygame.init()
w, h = 800, 800
cx, cy = w/2, h/2
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

verts = (-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1)
#edges = (0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)
colors = (255, 0, 0), (255, 128, 0), (255, 255, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0)


# Warning: This steals all mouse activity and keyboard input for the game.
#pygame.event.get()
#pygame.mouse.get_rel()
#pygame.mouse.set_visible(0)
#pygame.event.set_grab(1)

while True:
    dt = clock.tick()/1000

    # To make the camera rotate automatically based on time.
    #radian += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Give camera object access to the last event
        cam.events(event)

    screen.fill((0, 0, 0))


    #for x, y, z in verts:
        #x += 5
        #f = 200/z
        #x, y = x*f, y*f
        #pygame.draw.circle(screen, (0, 0, 0), (int(cx+int(x)), int(cy+int(y))), 6)


    """
    for edge in edges:
        points = []
        for x, y, z in (verts[edge[0]], verts[edge[1]]):
            x -= cam.pos[0]
            y -= cam.pos[1]
            z -= cam.pos[2]

            # Rotate on the y axis first, then on the x axis.
            x, z = rotate2d((x, z), cam.rot[1])
            y, z = rotate2d((y, z), cam.rot[0])
            f = (w/2)/z
            x, y = x*f, y*f
            points += [(int(cx+int(x)), int(cy+int(y)))]
        pygame.draw.line(screen, (0,0,0), points[0], points[1], 1)
    """

    vert_list = []
    screen_points = []
    for x, y, z in verts:
        # Translate all verts through camera
        x -= cam.pos[0]
        y -= cam.pos[1]
        z -= cam.pos[2]

        # Rotate on the y axis first, then on the x axis.
        x, z = rotate2d((x, z), cam.rot[1])
        y, z = rotate2d((y, z), cam.rot[0])
        vert_list += [(x, y, z)]

        f = (w/2)/z
        x, y = x*f, y*f
        screen_points += [(int(cx+int(x)), int(cy+int(y)))]


    face_list = []
    face_color = []
    depth = []
    for f in range(len(faces)):
        face = faces[f]

        on_screen = False
        for ea in face:
            x, y = screen_points[ea]
            if vert_list[ea][2] > 0 and x>0 and x<w and y>0 and y<h:
                on_screen = True
                break

        if on_screen:
            points = [screen_points[ea] for ea in face]
            face_list += [points]
            face_color += [colors[f]]

            # Depth formula.
            depth += [sum(sum(vert_list[j][i] for j in face)**2 for i in range(3))]


    # Create order to iterate over face list for drawing based on the depth formula
    order = sorted(range(len(face_list)), key=lambda i: depth[i], reverse=True)

    for i in order:
        try:
            pygame.draw.polygon(screen, face_color[i], face_list[i])
        except Exception as e:
            print("exception drawing polygon: {}".format(e))



    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt, key)


# Vertices (8 on a cube)
#
# Video coords (-z, +z)
#(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1)
#(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
# My attempt (+z, -z) Works!
#(-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1)
#(-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1)


# Edges (12 on a cube)
# (0,1), (1,2), (2,3), (3,0)
# (4,5), (5,6), (6,7), (7,4)
# (0,4), (1,5), (2,6), (3, 7)

# Rotation
# (0, 1): (sin, cos)
# (1, 0): (cos, -sin)
# (0, -1): (-sin, -cos)
# (-1, 0): (-cos, sin)

# "Join the pattern", not sure the maths behind this. Seen it before though.
# [ Counter clockwise ]
# x = y*sin + x*cos
# y = y*cos - x*sin

# Invert sin for clockwise
# x = x*cos - y*sin
# y = y*cos + x*sin


# Faces (6 on a cube)
#
# Vert label, also used for edges
# (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 4), (0, 3, 7, 4), (1, 2, 6, 5)



####
# 1. Create a level with high walls... large polygons. King of the hill, large arena areas, no complicated mazes.
# 2. Create a floor too and add colision detection.
# 3. Create gravity, and add jumping. Make perfect.
# 4. Jump problem: direction looking needs to match direction moving, even while airbourne.
# 5. Create a connection over the network. Steal info from game dict???
