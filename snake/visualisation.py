import cairo
import os
import imageio


def image(number, map1):
    height = len(map1)
    weight = len(map1[0])
    size_x = 400
    size_y = 400
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, size_x, size_y)
    cr = cairo.Context(ims)
    x = 0
    y = 0

    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(14)
    cr.rectangle(0, 0, size_y, size_x)
    for i in range(height):
        for j in range(weight):
            cr.set_line_width(1)
            if map1[i][j] == '▖':
                cr.set_source_rgb(0, 0, 0)
            elif map1[i][j] == '◎':
                cr.set_source_rgb(255, 211, 0)
            elif map1[i][j] == '🐸':
                cr.set_source_rgb(0, 255, 0)
            elif map1[i][j] == '◻':
                cr.set_source_rgb(0, 0.5, 0)
            else:
                cr.set_source_rgb(255, 255, 255)

            cr.rectangle(x, y, size_y / height, size_x / weight)
            cr.fill()
            cr.stroke()
            if x != size_x - size_x / weight:
                x += size_x / weight
            else:
                x = 0
                y += size_y / height

    ims.write_to_png(f"C:/Users/Пользователь/Desktop/"
                     f"snake_folder/images/image{number}.png")
    video()


def video():
    pics = []
    file = os.listdir(path="C:/Users/Пользователь/"
                           "Desktop/snake_folder/images")
    with imageio.get_writer("C:/Users/Пользователь/Desktop/"
                            "snake_folder/video.gif", mode='I') as writer:
        for length in range(len(file)):
            pics.append(f"C:/Users/Пользователь/Desktop/"
                        f"snake_folder/images/image{length+1}.png")
        for filename in pics:
            images = imageio.imread(filename)
            writer.append_data(images)
