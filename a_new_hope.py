import data_manip as dm

class DataSet():
    """base class for analysis of data from various sources"""

    def __init__(self, name, unit, data, disc = None, tau_c = None, avg = 1):
        self.name      = name
        self.unit      = unit
        self.data      = data
        self.disc      = disc 
        self.tau_c     = tau_c
        self.avg       = avg
        self.pdf       = None
        self.gauss_pdf = None
        self.gauss_ft  = None
        self.fr        = None
        # initial computations. 
        self.optimize_discard()
        self.discard()
        self.compute_decorrelation_time()
        self.compute_pdf()
        self.compute_fr()
    
    # Classes ATTRIBUTES:

    # Classes METHODS:
    def optimize_discard(self):
        """optimizes the discard of data by optimizing decorrelation times"""
        if self.disc is not None:
            print 'discard specifiedi as {} data points'.format(self.disc)
            pass
        pass
        # not yet active
        self.disc, self.tau_c   = dm.optimize_discard(self.data)
    
    def discard(self):
        """throws discarded data points"""
        self.data   = self.data[self.disc::]

    def compute_decorrelation_time(self):
        """compute decorrelation time,
           kicks in when disc is given but tau_c is not
           """
        if self.tau_c is not None:
            print 'decorrelation time is {}h'.format(self.tau_c)
            pass
        pass
        # not yet active, changes in dm first
        self.tau_c  = decorrelation_time(data) 

    def compute_pdf(self):
        """compute pdf from contained data"""
        if self.pdf is not None:
            print 'pdf already computed'
            pass
        pass

    def fit_gaussian(self):
        """fit gaussian to PDF and compute FR from fit"""
        if self.gausss_pdf is not None:
            print 'Gaussian Fit already performed'
            pass
        pass

    def compute_fr (self):
        """compute fr from contained data"""
        if self.fr is not None:
            print 'FR already computed'
            pass
        pass
    
    def print_pdf(self):
        """print self.pdf"""
        if self.pdf is None:
            print 'PDF not yet computed'
            pass
        pass
    
    def print_fr(self):
        """print fr"""
        if self.fr is None:
            print 'FR not yet computed'
            pass
        pass
    
    # initialization computations. Assuming pdf's and fr's are always wanted?

# working with inheritance?

#class DataPDF( DataSet ):
#    pass

#class DataFR( DataSet ):
    
#    def __init__():
#        self.pdf    = DataPDF()  ???



