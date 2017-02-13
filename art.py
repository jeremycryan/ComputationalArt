""" TODO: Put your header comment here """

import random
from PIL import Image
import math

def prod(f, a, b):
    return evaluate_random_function(f[1][0], a, b) * evaluate_random_function(f[1][1], a, b)

def avg(f, a, b):
    return (evaluate_random_function(f[1][0], a, b) + evaluate_random_function(f[1][1], a, b))/2

def cos_pi(f, a, b):
    return math.cos(math.pi*evaluate_random_function(f[1], a, b))

def sin_pi(f, a, b):
    return math.sin(math.pi*evaluate_random_function(f[1], a, b))

def power_2(f, a, b):
    return evaluate_random_function(f[1], a, b)**2

def square_root(f, a, b):
    return abs(evaluate_random_function(f[1], a, b))**(1/2)

def x(a, b):
    return a

def y(a, b):
    return b


def build_random_function(min_depth, max_depth):
    function_dict = {1 : "prod",
                    2 : "avg",
                    3 : "cos_pi",
                    4 : "sin_pi",
                    5 : "power_2",
                    6 : "square_root",
                    7 : "x",
                    8 : "y"}
    if random.randint(min_depth, max_depth) <= 0:
        # print("Ends by random termination")
        recstr = [function_dict[random.randint(7, 8)]]
        return recstr
    recstr = [function_dict[random.randint(1, 6)]]
    # print("Recurse.")
    if "_" not in str(recstr):
        recstr.append([build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth - 1)])
    else:
        recstr.append(build_random_function(min_depth - 1, max_depth - 1))
    return recstr


def evaluate_random_function(f, a, b):
    fdict = {"prod" : prod, "avg" : avg, "cos_pi" : cos_pi, "sin_pi" : sin_pi, "power_2" : power_2, "square_root" : square_root, "x" : x, "y" : y}
    paradict = {"prod" : (f, a, b), "avg" : (f, a, b), "cos_pi" : (f, a, b), "sin_pi" : (f, a, b), "power_2" : (f, a, b), "square_root" : (f, a, b), "x" : (a, b), "y" : (a, b)}
    return fdict[f[0]](*paradict[f[0]])


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
        input_range = input_interval_end - input_interval_start
        output_range = output_interval_end - output_interval_start
        propival = (val - input_interval_start) / input_range
        outputval = (propival * output_range) + output_interval_start
        return outputval


def color_map(val):
    return remap_interval(val, -1, 1, 0, 255)


def test_image(filename, x_size=350, y_size=350):
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    red_function = build_random_function(6, 9)
    green_function = build_random_function(6, 9)
    blue_function = build_random_function(6, 9)
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    int(color_map(evaluate_random_function(red_function, x, y))),
                    int(color_map(evaluate_random_function(green_function, x, y))),
                    int(color_map(evaluate_random_function(blue_function, x, y)))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
