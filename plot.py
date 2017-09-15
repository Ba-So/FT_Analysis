from matplotlib import pyplot as plt
import itertools as iter
import numpy as np

def plot_xy(data,name):
    # supposed to plot a flexible amlount of data.
    # use list comprehension
    # pltting info in array of arrays:
    marker      = iter.cycle(('o','v','^','<','>','s','8','p'))
    ax          = plt.gca()
    for i in range(len(data)):
        color   = next(ax._get_lines.prop_cycler)['color']
        plt.plot(data[i][0], data[i][1], ls='', mec='none', ms=2, marker=marker.next(),
                color=color)
        if len(data[i])>2:
            plt.plot(data[i][0], data[i][2], color=color)
    plt.savefig(name)
    plt.show()

def plot_x(data,name):
    # supposed to plot a flexible amlount of data.
    # use list comprehension
    # pltting info in array of arrays:
    marker      = iter.cycle(('o','v','^','<','>','s','8','p'))
    ax          = plt.gca()
    for i in range(len(data)):
        color   = next(ax._get_lines.prop_cycler)['color']
        plt.plot(data[i], ls='', mec='none', ms=2, marker=marker.next(),
                color=color, linewidth=1.0)
    plt.savefig(name)
    plt.show()


def plot_x_avg(data,name):
    # supposed to plot a flexible amlount of data.
    # use list comprehension
    # pltting info in array of arrays:
    marker      = iter.cycle(('o','v','^','<','>','s','8','p'))
    ax          = plt.gca()
    
    for i in range(len(data)):
        color   = next(ax._get_lines.prop_cycler)['color']
        plt.plot(data[i], ls='', mec='none', ms=2, marker=marker.next(),
                color=color, linewidth=1.0)
        data_avg=np.mean(data[i])
        avg_arr =[data_avg for k in range(len(data[i]))]
        color   = next(ax._get_lines.prop_cycler)['color']
        plt.plot(avg_arr, ls='--', mec='none', ms=2, color=color,
                linewidth=1.0)
    plt.savefig(name)
    plt.show()
