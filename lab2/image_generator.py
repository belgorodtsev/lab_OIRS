from PIL import Image, ImageDraw
from random import randrange as r
import os

WINDOW_SIZE = 1000


def is_not_cross(rectangle_a, rectangle_b):
    x_a = [rectangle_a[0], rectangle_a[2]]
    x_b = [rectangle_b[0], rectangle_b[2]]
    y_a = [rectangle_a[1], rectangle_a[3]]
    y_b = [rectangle_b[1], rectangle_b[3]]

    if max(x_a) < min(x_b) or max(y_a) < min(y_b) or min(y_a) > max(y_b):
        return True    # не пересекаются
    else:
        return False   # пересекаются


# круг
def generate_array_circle():
    x_0 = r(100, WINDOW_SIZE - 100)
    y_0 = r(100, WINDOW_SIZE - 100)
    delta = r(80, 120)
    return [x_0, y_0, x_0 + delta, y_0 + delta]


# прямоугольник
def generate_array_rectangle():
    array = [r(100, WINDOW_SIZE - 100), r(100, WINDOW_SIZE - 100), r(100, WINDOW_SIZE - 100), r(50, WINDOW_SIZE - 100)]
    delta_x = abs(array[2] - array[0])
    delta_y = abs(array[3] - array[1])
    while delta_x < 50 or delta_y < 50 or delta_x > 300 or delta_y > 300:
        array = [r(100, WINDOW_SIZE - 100), r(100, WINDOW_SIZE - 100), r(100, WINDOW_SIZE - 100), r(100, WINDOW_SIZE - 100)]
        delta_x = abs(array[2] - array[0])
        delta_y = abs(array[3] - array[1])
    return array


# для правильных фигур (треугольник, квадрат, пятиугольник)
def generate_regular_polygon():
    return [r(150, WINDOW_SIZE - 100), r(150, WINDOW_SIZE - 100), r(50, 100)]


# проверка пересечиня с другими фигурами при генерации новой
def check_cross(array_shapes: list, shape: list):
    if not array_shapes:
        return True

    for figure in array_shapes:
        if not is_not_cross(figure, shape):
            return False
    return True


# позвращает координаты прямоугольника от круга
def circle_to_rectangle(array):
    radius = array[2]
    return [array[0] - radius, array[1] - radius, array[0] + radius, array[1] + radius]


# генерация одной фигуры и проверка на пересечение с другими
def generate(n_shape, gen_func, array_shapes, array_figure):
    for _ in range(n_shape):
        shape = gen_func()
        if len(shape) == 3:
            check_shape = circle_to_rectangle(shape)
            if not check_cross(array_shapes, check_shape):
                return False
            array_shapes.append(check_shape)
            array_figure.append(shape)
        else:
            if not check_cross(array_shapes, shape):
                return False
            array_shapes.append(shape)
            array_figure.append(shape)
    return True


# очистка массивов фигур
def clear_array_shapes(array_all_shapes, array_shapes):
    array_all_shapes.clear()
    for array in array_shapes:
        array[1].clear()


# генерация фигур
def generate_shapes(image_draw, n_rectangle=2, n_circle=2, n_triangle=2, n_square=2, n_pentagon=1):
    array_shapes = list()
    array_figures = [(n_rectangle, list(), generate_array_rectangle),
                     (n_circle, list(), generate_array_circle),
                     (n_triangle, list(), generate_regular_polygon),
                     (n_square, list(), generate_regular_polygon),
                     (n_pentagon, list(), generate_regular_polygon)]

    while True:
        clear_array_shapes(array_shapes, array_figures)

        for num, array, gen_func in array_figures:
            flag = generate(num, gen_func, array_shapes, array)
            if not flag:
                break

        if not flag:
            continue

        break

    for i, figures in enumerate(array_figures):
        if i == 0:
            for rectangle in figures[1]:
                image_draw.rectangle(rectangle, fill=(r(50, 255), r(50, 255), r(50, 255)))
        elif i == 1:
            for circle in figures[1]:
                image_draw.ellipse(circle, fill=(r(50, 255), r(50, 255), r(50, 255)))
        else:
            for fig in figures[1]:
                image_draw.regular_polygon(fig, i + 1, rotation=r(360), fill=(r(50, 255), r(50, 255), r(50, 255)))


def generate_random_images(n_images):
    if not os.path.exists("init"):
        os.mkdir("init")
    for i in range(n_images):
        image = Image.new("RGB", (WINDOW_SIZE, WINDOW_SIZE), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        generate_shapes(draw)
        image.save(f"init/{i + 1}.jpg")


if __name__ == "__main__":
    number_images = input("Введите количество изображений:")
    generate_random_images(int(number_images))
