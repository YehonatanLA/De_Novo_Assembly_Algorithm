from sympy.abc import a, b, x
from sympy import *
import matplotlib.pyplot as plt
from scipy.misc import derivative
import numpy as np
from sympy.physics.continuum_mechanics.beam import numpy
from sympy import diff, Symbol
from sympy.parsing.sympy_parser import parse_expr


def read_function():
    f = open("function2.txt", "r")
    temp = f.read().strip()
    f.close()
    return temp


def main():
    # points = []
    # for k in range(200, 10000, 200):
    #     f = open(f"inputs2/input{k}.txt", "r")
    #     read_num = f.readline().strip()
    #     no_covers = f.readline().strip()
    #     success_percent = float(f.readline().strip())
    #     success_percent = int(success_percent * 1000)
    #     success_percent_full_covers = f.readline().strip()
    #     points.append((k, success_percent))

    # print(points)
    # y = interpolate(points, x)
    # print(y)
    # print(interpolate([(1, 1), (2, 4), (3, 9)], x))
    func = read_function()
    x_axis = []
    y_axis = []

    my_symbols = {'x': Symbol('x')}
    my_func = parse_expr(func, my_symbols)
    der = diff(my_func, my_symbols['x'])
    close_zero = 0

    for k in range(200, 10000, 200):
        x_axis.append(k)
        if abs(der.subs({x: k}) / float(1000)) < 1:
            close_zero += 1
        y_axis.append(der.subs({x: k}) / float(1000))

    print(len(y_axis))
    print(close_zero)
    print(len(y_axis) - close_zero)
    print(y_axis)
    plt.plot(x_axis, y_axis)
    plt.xlabel('read amounts')
    plt.ylabel('derivative')
    plt.show()

    # print(my_func.subs({x:400}))
    # graph(der)
    # diff(my_func, *3 * [my_symbols['x']])


if __name__ == "__main__":
    main()
