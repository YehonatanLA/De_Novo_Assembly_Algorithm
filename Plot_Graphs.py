import matplotlib.pyplot as plt
import numpy as np


def main():
    x_axis = []
    y_axis_full_covers = []
    y_axis = []
    y_axis_no_covers = []
    for k in range(200, 10000, 200):
        f = open(f"inputs/input{k}.txt", "r")
        read_num = f.readline().strip()
        no_covers = f.readline().strip()
        success_percent = f.readline().strip()
        success_percent_full_covers = f.readline().strip()
        x_axis.append(k)
        y_axis_full_covers.append(success_percent_full_covers)
        y_axis.append(success_percent)
        y_axis_no_covers.append(no_covers)

    plt.plot(x_axis, y_axis, label="cover+algorithm success percentage")
    plt.plot(x_axis, y_axis_full_covers, label="only algorithm success percentage")
    plt.xlabel('read amounts')
    plt.ylabel('success percent')
    #  plt.xticks(np.arange(0, len(x_axis) + 1, 1000))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
