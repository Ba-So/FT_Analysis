from matplotlib import pyplot as plt
import itertools as iter
import numpy as np

class Plot(object):

    def __init__(self, data):
        self.fig    = None
        self.data   = data
        self.kwargs = {}
        self.plot()

    def plot(self, data = None):
        """print data"""
        if data is None:
            data = self.data

        if data.ndim == 1:
            # simple 1D plot information
            self.onedim_plot(data)
            self.fig    = plt.gcf()

        elif data.ndim == 2:
            # assuming 2D plot information
            if len(data) == 2:
                self.twodim_plot(data[0], data[1])
                self.fig    = plt.gcf()
            else:
                # obviously there are cases here not taken into account
                pass

        elif data.ndim == 3:
            # multiple 1D plots in 3D structure
            # in consequence only way to have multiple 1D's
            marker              = iter.cycle(('o','v','^','<','>','s','8','p'))
            ax                  = plt.gca()
            if len(data[0,:,0]) == 1:
                for i in range(np.shape(data)[0]):
                    color    = next(ax._get_lines.prop_cycler)['color']
                    self.kwargs['marker'] = marker.next()
                    self.kwargs['color']  = color
                    self.onedim_plot(data[i][0])
            # multiple 2D plots in 3D structure
                self.fig    = plt.gcf()
            elif len(data[0,:,0]) == 2:
                for i in range(np.shape(data)[0]):
                    color    = next(ax._get_lines.prop_cycler)['color']
                    self.kwargs['marker'] = marker.next()
                    self.kwargs['color']  = color
                    self.twodim_plot(data[i][0], data[i][1])
            # else I must assume 3D plot info. case not implemented.
                self.fig    = plt.gcf()
            else:
                pass
        # 4D data structures and above not implemented.
        else:
            pass
        # mark axes and title
        
    def onedim_plot(self, x):
        "is performing oneD plotting"
        ax  = plt.gca()
        ax.plot(x, **self.kwargs)

    def twodim_plot(self, x, y):
        "is performing 2D plotting"
        ax  = plt.gca()
        ax.plot(x, y, **self.kwargs)
    
    def show(self):
        if self.fig is not None:
            plt.show(self.fig)

if __name__== '__main__':
    data    = np.array([[[k+j for k in range(10)]
                              for j in range(2)] 
                              for i in range(3) ])
    plot    = Plot(data)
    plot.show()

