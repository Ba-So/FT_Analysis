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
        """print data
        takes lists of np.arrays"""
        # Obviusly this is the dumbest implementation, if supposed to be used
        # for more than this one thing...
        if data is None:
            data = self.data
        if len(np.shape(data)) > 1:
            # multiple 2D plots  3D structure
            plt.gca().set_color_cycle(None)
            marker      = iter.cycle(('o','v','^','<','>','s','8','p'))
            ax          = plt.gca()
            for i,j in enumerate(data[0,]):
                # multiple 1D plots 2D structure
                if np.shape(data[i])[0] == 1:
                    color    = next(ax._get_lines.prop_cycler)['color']
                    self.kwargs['marker'] = marker.next()
                    self.kwargs['color']  = color
                    self.fig = self.onedim_plot(data[i, 0])
                # multiple 2D plots in 3D structure
                elif np.shape(data[i])[0] == 2:
                    color    = next(ax._get_lines.prop_cycler)['color']
                    self.kwargs['marker'] = marker.next()
                    self.kwargs['color']  = color
                    self.fig = self.twodim_plot(data[i, 0], data[i, 1])
            # else I must assume 3D plot info. case not implemented.
                else:
                    pass
            # 4D data structures and above not implemented.
            self.fig    = plt.gca()
        elif len(shape(data)) == 1:
            color    = next(ax._get_lines.prop_cycler)['color']
            self.kwargs['marker'] = marker.next()
            self.kwargs['color']  = color
            self.fig = self.onedim_plot(data[i][0])
            self.fig    = plt.gca()

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

       self.fit_curve   = []
       self.fit_slope   = []
       self.fit_offs    = []

       if self.data is None:
           print 'data None'
           pass

       if len(self.data) >= 1:
           for i in range(len(self.data)):
               if self.data[i].ndim == 2:
                   curve, fit_slope, fit_offs = dm.lin_reg(self.data[i])
                   self.fit_curve.append(curve)
                   self.fit_slope.append(fit_slope)
                   self.fit_offs.append(fit_offs)
               elif self.data.ndim == 1:
                   print 'Data Set is 1D array, require 2D array'
                   # I know this is dumb.
               else:
                   print 'data set has to many dimensions, not compatible'
       else:
           print 'data empty'


    def plot_linreg(self):
        """adds a linear regression to a plot"""
        self.linear_fit()
        self.plot()
        self.kwargs['linestyle'] = '-'
        self.kwargs['ms']        = '0.0'
        self.plot(self.fit_curve)
        self.kwargs['linestyle'] = 'none'
        self.kwargs['ms']        = '1.5'

