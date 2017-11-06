import data_manip as dm
import numpy as np
import plot as pc
#from scipy.optimize import minimize_scalar

class DataSet(object):
    """base class for data of all kind"""

    def __init__(self, name, symbol, unit, data, dtime, disc):
        self.name      = name # name of quantity for printing
        self.symbol    = symbol # formula symbol for printing
        self.unit      = unit # physical unit of quantity for printing
        self.data      = np.array(data) # data
        self.dtime     = dtime # time step of dataset
        self.disc      = disc # to be discarded number of initial data points
        self.fig       = None # figure object to be passed back and forth
    
    def discard(self):
        """throws discarded data points"""
        if len(self.data) > self.disc:
            self.data   = self.data[self.disc::]
        else:
            print 'invalid Parameter for discard of data points'
            self.disc   = None
    def plot_data(self):
        # mind the $ and r's for latex formatted printing 
        labels['ylabel'] = r'${} / {}$'.format(symbol, unit)
        # lacks universality, but based on use is ok
        labels['xlabel'] = 'timesteps in s'
        labels['title']  = ''
        kwargs           = {'linestyle': 'solid', 'label':'',
                            'marker':'o','lw':'1.0', 'color':'blue'}
        self.fig = pc.Plot(self.data, labels, **kwargs)

class FRData(DataSet):
    """class for FR analysis of data"""

    def __init__(self, name, symbol, unit, data, dtime, disc = None, tau_c =
            None, avg_step = 1):
        super(FRData, self).__init__(name, symbol, unit, data, dtime, disc)
        self.tau_c     = tau_c #correlation time of dataset
        self.avg_step  = avg_step # not yet active, for discrete averaging
        self.pdf       = None # propability distribution function
        self.fr        = None # fluctuation relation
        # initial computations. 
        self.optimize_discard() # not yet functional
        self.discard()
        self.compute_decorrelation_time()
    
    # Classes ATTRIBUTES:

    # Classes METHODS:
    def optimize_discard(self):
        """optimizes the discard of data by optimizing decorrelation times"""
        if self.disc is not None:
            print 'discard specified as {} data points'.format(self.disc)
            pass
        pass
        # not yet active
        # self.disc, self.tau_c   = minimize_scalar (self.discard)
    

    def compute_decorrelation_time(self):
        """compute decorrelation time,
           kicks in when disc is given but tau_c is not
           """
        if self.tau_c is not None:
            print 'decorrelation time is {} h'.format(self.tau_c)
            pass
        pass
        # not yet active, changes in dm first
        self.tau_c  = dm.decorrelation_time(self.data)[0] 

    def compute_pdf(self, tau_c):
        """compute pdf from contained data"""
        return dm.compute_pdf(self.data, tau_c) 

    def compute_fr (self, pdf):
        """compute fr from contained data"""
        if pdf is None:
            print 'PDF not computed, aborting'
            pass
        elif self.tau_c is None:
            print '''no valid decorrelation time, aborting computation of
                   Fluctuation Relation'''
            pass
        else:
            inter = dm.fr_analysis(pdf, self.dtime, self.tau_c)
            
            return inter 

    
    def compute_multiple(self, times):
        """computes pdf's and fr's for multiples of tau_c"""
        if self.tau_c is None:
            print 'invalid or no decorelation time for dataset, aborting'
            pass
        else:
            self.pdf    = []
            self.fr     = []
            for i in range(0, times):
                print 'Durchgang {}'.format(i+1)
                fr_help = None
                inter   = None
                self.pdf.append(self.compute_pdf((i+1)*self.tau_c))
                inter = self.compute_fr(self.pdf[i])
                if inter is not None:
                    fr.append(inter)
            self.pdf    = np.array(self.pdf)
            if self.fr:
                self.fr     = np.array(self.fr)
            else:
                self.fr     = None


    def plot_pdf(self):
        """print self.pdf"""
        if self.pdf is None:
            print 'PDF not yet computed'
            pass
        else:
            labels = {}
            # mind the $ and r's for latex formatted printing 
            labels['ylabel'] = r'PDF(\langle\bar{'+r'{}'.format(self.symbol)+r'_{\tau}}\rangle)'
            # lacks universality, but based on use is ok
            labels['xlabel'] = r'{} / {}'.format(self.symbol, self.unit)
            labels['title']  = (r'probability distribution of values of '
                                +r'${}$'.format(self.symbol))
            kwargs           = {'linestyle': 'none','label':'',
                                'marker':'o', 'ms': 1.5, 'lw':'1.0', 
                                'color':'blue'}
            self.pdf_fig = pc.Plot(self.pdf, labels, **kwargs)
            self.pdf_fig.show()
    
    
    def plot_fr(self):
        """print self.fr"""
        if self.fr is None:
            print 'FR not yet computed'
            pass
        else:
            labels           = {}
            # mind the $ and r's for latex formatted printing 
            labels['ylabel'] =( r'\frac{1}{\tau}ln\left(\frac{P(\langle\bar{'
                             +  r'{}'.format(self.symbol)
                             +  r'_{\tau}}\rangle)}{P(\langle\bar{'
                             +  r'{}'.format(self.symbol) 
                             +  r'_{\tau}}\rangle)}\right)')

            # lacks universality, but based on use is ok
            labels['xlabel'] =(r'\langle\bar{' 
                    + r'{}'.format(self.symbol)
                             + r'_{\tau}}\rangle / '
                             + r'{}'.format(self.unit))
            labels['title']  =(r'fluctuation relation for '
                             + r'${}$'.format(self.symbol))
            kwargs           = {'linestyle': 'none', 'label': '',
                                'marker': 'o','lw': '1.0', 'color': 'blue',
                                'ms': 1.5}
            self.fr_fig = pc.Lin_Reg(self.fr, labels, **kwargs)
            self.fr_fig.show()

    def plot(self):
        self.plot_pdf()
        self.plot_fr()

class GaussData( FRData ):
    """Class that includes Gaussian Analysis
        likely to be superflous.
        But it makes for pretty plots.
        """
     
    def __init__(self, name, unit, data, dtime,
                 disc = None, tau_c = None, avg_step = 1):
        super(GaussData, self).__init__(name, symbol, unit, data, dtime, disc, tau_c, avg_step)
        self.gauss_pdf = None
        self.gauss_fr  = None
        self.fit_gaussian()

    def fit_gaussian(self):
        """fit gaussian to PDF and compute FR from fit"""
        if self.gauss_pdf is not None:
            print 'Gaussian Fit already performed'
            pass
        self.gauss_pdf  = dm.gauss_fit(self.pdf[0][:], self.pdf[1][:])
        self.gauss_fr   = self.compute_fr(self, self.gauss_pdf)
        self.gauss_lin, self.gauss_slope, self.gauss_offs = self.linear_fit(gauss_fr)

class PrintFancy():
    """only responsible for the setting of various print parameters"""
    pass
