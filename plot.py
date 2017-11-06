from matplotlib import pyplot as plt
import itertools as iter
import numpy as np
import data_manip as dm

class Plot(object):
    """base class for all sorts of plots
       the intended use is: one plot class per data set.
       """

    def __init__(self, data, strings, **kwargs):
        # input data
        self.data   = data
        # dict containing strings for labels etc.
        self.strings= strings
        # kwargs dict containing possible kwargs for plt
        self.kwargs = kwargs
        # figure:
        self.fig    = None
        # plot figure
        self.plot()
    
    def cla(self):
        """close figure"""
        self.fig.cla()

    def plot(self, data = None):
        """print data"""
        if data is None:
            data = self.data

        if data.ndim == 1:
            # simple 1D plot information
            self.onedim_plot(data)
            self.fig    = plt.gca()

        elif data.ndim == 2:
            # assuming 2D plot information
            if len(data) == 2:
                self.twodim_plot(data[0], data[1])
                self.fig    = plt.gca()
            else:
                # obviously there are cases here not taken into account
                pass

        elif data.ndim == 3:
            # multiple 1D plots in 3D structure
            # in consequence only way to have multiple 1D's
            plt.gca().set_color_cycle(None)
            marker      = iter.cycle(('o','v','^','<','>','s','8','p'))
            ax          = plt.gca()
            if len(data[0,:,0]) == 1:
                for i in range(np.shape(data)[0]):
                    color    = next(ax._get_lines.prop_cycler)['color']
                    self.kwargs['marker'] = marker.next()
                    self.kwargs['color']  = color
                    self.fig = self.onedim_plot(data[i][0])
                self.fig    = plt.gca()
            # multiple 2D plots in 3D structure
            elif len(data[0,:,0]) == 2:
                for i in range(np.shape(data)[0]):
                    color    = next(ax._get_lines.prop_cycler)['color']
                    self.kwargs['marker'] = marker.next()
                    self.kwargs['color']  = color
                    self.fig = self.twodim_plot(data[i][0], data[i][1])
                self.fig    = plt.gca()
            # else I must assume 3D plot info. case not implemented.
            else:
                pass
        # 4D data structures and above not implemented.
        else:
            pass
        # mark axes and title
        if not (self.fig is None):
            self.arrange_strings()

    def onedim_plot(self, x):
        "is performing oneD plotting"
        ax  = plt.gca()
        ax.plot(x, **self.kwargs)

    def twodim_plot(self, x, y):
        "is performing 2D plotting"
        ax  = plt.gca()
        ax.plot(x, y, **self.kwargs)

    
    def format_string(self, string):
        return r'$'+string+r'$'

    def arrange_strings(self):
        #plt.rc('text', usetex=True)
        #plt.rc('font', family='serif')
        if 'xlabel' in self.strings:
            plt.xlabel(self.format_string(self.strings['xlabel']), fontsize = 20)
        if 'ylabel' in self.strings:
            plt.ylabel(self.format_string(self.strings['ylabel']), fontsize = 18)
        if 'title' in self.strings:
            plt.suptitle(self.strings['title'], fontsize = 18)

    def show(self):
        if self.fig is not None:
            plt.show(self.fig)

    def save(self):
        if ('opath' in self.strings) & ('oname' in self.strings):
            plt.savefig(self.strings['opath'] + self.strings['oname'])
        else:
            print 'Output Path and File Name not specified.'

class Lin_Reg(Plot):
    """daughter class of Plot, which adds a linear Refression Fit
       to the plot in Question"""
    def __init__(self, data, strings, **kwargs):
        Plot.__init__(self, data, strings, **kwargs)   
        self.fit_curve = None # curve of fit to self.fr
        self.fit_slope = None # slope of fit
        self.fit_offs  = None # offset of fit
        self.plot_linreg()

    def linear_fit (self):
       """computes linear regression to fr"""
       if self.data is None:
           print 'data None'
           pass
       elif self.data.ndim == 1:
           print 'Data Set is 1D array, require 2D array'
           # I know this is dumb.
       elif self.data.ndim == 2:
           self.fit_curve, self.fit_slope, self.fit_offs = dm.lin_reg(self.data)

       elif self.data.ndim == 3:
           self.fit_curve       = []
           self.fit_slope   = []
           self.fit_offs    = []
           for i in range(np.shape(self.data)[0]):
               curve, fit_slope, fit_offs = dm.lin_reg(self.data[i])
               self.fit_curve.append(curve)
               self.fit_slope.append(fit_slope)
               self.fit_offs.append(fit_offs)

           self.fit_curve   = np.array(self.fit_curve) 
           self.fit_slope   = np.array(self.fit_slope) 
           self.fit_offs    = np.array(self.fit_offs)

       else:
           print 'data set has to many dimensions, not compatible' 


    def plot_linreg(self):
        """adds a linear regression to a plot"""
        self.linear_fit()
        self.plot()
        self.kwargs['linestyle'] = '-'
        self.kwargs['ms']        = '0.0'
        self.plot(self.fit_curve)
        self.kwargs['linestyle'] = 'none'
        self.kwargs['ms']        = '1.5'









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

