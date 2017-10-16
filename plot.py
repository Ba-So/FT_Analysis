from matplotlib import pyplot as plt
import itertools as iter
import numpy as np

def plot_xy(data,name, fancy):
    # supposed to plot a flexible amlount of data.
    # use list comprehension
    # pltting info in array of arrays:
    marker      = iter.cycle(('o','v','^','<','>','s','8','p'))
    ax          = plt.gca()
    for i in range(len(data)):
        color   = next(ax._get_lines.prop_cycler)['color']
        plt.plot(data[i][0], data[i][1], ls='', mec='none', ms=2, marker=marker.next(),
                color=color, label= r'$t = {} \tau_c$'.format((i+1)))
        if len(data[i])>2:
            plt.plot(data[i][0], data[i][2], color=color,
                    )
    plt.legend()
    plt.title(fancy['title'], fontsize=20)
    plt.xlabel(fancy['xlabel'], fontsize=18)
    plt.ylabel(fancy['ylabel'], fontsize=18)
    plt.savefig(name)
    plt.show()

def plot_xy_ft(data,name, fancy):
    # supposed to plot a flexible amlount of data.
    # use list comprehension
    # pltting info in array of arrays:
    marker      = iter.cycle(('o','v','^','<','>','s','8','p'))
    ax          = plt.gca()
    for i in range(0, len(data), 2):
        color   = next(ax._get_lines.prop_cycler)['color']
        plt.plot(data[i][0], data[i][1], ls='-', mec='none', ms=2, marker=marker.next(),
                color=color, label= r'gauss-fit $ t = {} \tau_c$'.format((i/2+1)))
        plt.plot(data[(i+1)][0], data[(i+1)][1], ls='', mec='none', ms=2, marker=marker.next(),
                color=color, label= r'$t = {} \tau_c$'.format((i/2+1)))
        if len(data[i])>2:
            plt.plot(data[i][0], data[i][2], color=color,
                    )
    plt.legend(loc= 'lower right')
    plt.title(fancy['title'], fontsize=20)
    plt.xlabel(fancy['xlabel'], fontsize=18)
    plt.ylabel(fancy['ylabel'], fontsize=18)
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


def plot_x_avg(data,name, fancy, markat = []):
    # supposed to plot a flexible amlount of data.
    # use list comprehension
    # pltting info in array of arrays:
    marker      = iter.cycle(('o','v','^','<','>','s','8','p'))
    ax          = plt.gca()
    mark_mask   = create_mask(len(data), markat)
    for i in range(len(data)):
        disc    = 0
        color   = next(ax._get_lines.prop_cycler)['color']
        plt.plot(data[i], ls='', mec='none', ms=2, marker=marker.next(),
                color=color, linewidth=1.0)
        if mark_mask[i]:
            plt.axvline(x = markat[i],
                    label = r'discarded days: {}'.format(markat[i]/720))
            disc    = markat[i]
        data_avg=np.mean(data[i][disc::])
        avg_arr =[data_avg for k in range(len(data[i][disc::]))]
        color   = next(ax._get_lines.prop_cycler)['color']
        plt.plot(avg_arr, ls='--', mec='none', ms=2, color=color,
                linewidth=1.0, label= r'avg : {}'.format(data_avg))
        
    plt.legend(loc = 'lower right')
    plt.title(fancy['title'], fontsize=20)
    plt.xlabel(fancy['xlabel'], fontsize=18)
    plt.ylabel(fancy['ylabel'], fontsize=18)
    plt.savefig(name)
    plt.show()

def create_mask(n, array):
    """Creates a masked true False array"""
    mask = np.array([False for i in range(n)])
    count = 0
    for val in array:
        if val != 0:
            mask[count] = True
        count += 1
    return mask

