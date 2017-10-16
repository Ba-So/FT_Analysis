from __future__ import division
import numpy as np
import custom_io as io
from scipy import stats as st
from scipy.optimize import curve_fit, minimize
import matplotlib.pyplot as plt
import math as math

def gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

def gauss_fit(x, y):

    n           = sum(y)
    mean        = sum(x*y)/n
    sigma       = np.sqrt(sum(y* (x - mean)**2) / n)
    popt,pcov  = curve_fit(gauss, x, y, p0=[max(y), mean, sigma])
    fit_val     = []
    fit_val     = np.array([gauss(i, *popt) for i in x])
    return fit_val


def mean(values):
    """computes the mean of an array of values"""
#   if ever there are problems with this routine...
#    return(np.mean(values))
#   Ansatz das selbst zu schreiben
    if not (isinstance(values, np.ndarray) or isinstance(values, list)):
        if isinstance(values, int) or isinstance(values, float):
            return values 
        else:
            print 'input data is not numerical!'
            return None
    else: 
        mean = 0.0
        for value in values:
            mean += value
        mean = mean / len(values)
        return mean

def compute_means(data, keys):
    """computes mean value of values specified by keys
    
       input: data type:dict, keys type:list
       output: en_list type:dict, only those entries specified by keys
       """
#    en_list = {'pote':, 'pote_mean':, 'kine':, 'kine_mean',: 'inne':,
#            'inne_mean':, 'etot':, 'etot_mean':}
    en_list = {}
    for key in data:
        if key in keys:
            help            = np.array(data[key])
            en_list[key]    = help

    for key in data:
        if key in keys:
            str     = key + '_mean'
            en_list[(key + '_mean')]    =  mean(en_list[key])
    
    return en_list 

def compute_etot(data):
    """computes total energy"""

    en_list = data
    keys = ['kine','inne','pote']
    if not all(key in keys for key in data):
        print 'Data missing for computation of total Energy!'
        print 'returning initial input'
        return data
    else:
        en_list['etot']       = 0.0
        for key in keys:
            en_list['etot'] += en_list[key]

        en_list['etot_mean']  = mean(en_list['etot'])

    return en_list

def make_relative(data, keys):
    new_data = {}
    for key, values in data.iteritems():
        if key in keys:
            new_values = []
            first_value = values[0]
            for value in values:
                new_values.append(value - first_value)
            new_data[key] = new_values
        else:
            new_data[key] = values
    return new_data

def running_mean(x, N):
    """efficent running mean computation"""
    cumsum  = np.cumsum(np.insert(x,0,0))
    help    = (cumsum[N:] - cumsum[:-N]) / N
    return help[:-N or none]

def stepwise_mean(x, N, jump):
    """for jumping values like Denny did"""
    data    = running_mean(x, N)
    out     = []
    for i in range(0, len(data), jump):
        out.append(data[i])
    return out

def define_bins(data, num_bins):
    """defines bins for estimation of PDF"""
    num_bins  = int(math.log(len(data),2))+1
    print 'num_bins: {}'.format(num_bins)
    print len(data)
    bins      = np.zeros(((num_bins+1), 3))
    if not (isinstance(data, np.ndarray) or isinstance(data, list)):
        print 'input data is not an np.array or list'
        return bins
    else:
        # define bins such, that they are symmetric around zero
        dat_max   = np.amax(data)
        dat_min   = np.amin(data)
        dat_step  = abs((dat_max-dat_min) / num_bins)   
        if dat_min < 0:
            if dat_max >= 0:
                num_l     = int(abs(dat_min+dat_step) // dat_step)
                if (dat_min+dat_step)%dat_step <0:
                    num_l += 1 
                #in need of further correction
                # lower bound of bin
                bins[(num_l), 1] = -dat_step 
                # upper bound of bin
                bins[(num_l), 2] = 0
                # center of bin, for plotting
                bins[(num_l), 0] = -dat_step/2 
            elif dat_max <=0:
                num_l     = int(abs(dat_max-dat_min-dat_step) //dat_step) 
                # lower bound of bin
                bins[(num_l), 1] = dat_max-dat_step 
                # upper bound of bin
                bins[(num_l), 2] = dat_max
                # center of bin, for plotting
                bins[(num_l), 0] = dat_max-dat_step/2 
            for i in range((num_l-1), -1, -1):
                for j in range(3):
                    bins[i, j] = bins[i + 1, j] - dat_step
        else: 
            print "Data not a candidate for FT"
            num_l     =  1
            # lower bound of bin
            bins[0, 1] = dat_min 
            # upper bound of bin
            bins[0, 2] = dat_min + dat_step 
            # center of bin, for plotting
            bins[0, 0] = dat_min + dat_step/2 

        for i in range(num_l, (num_bins+1)):
            for j in range(3):
                bins[i, j] = bins[(i - 1), j] + dat_step
        return bins  

def compute_pdf(data, avg, num_bins=30, sgauss=False, avg_step=0):
    """creates probability distribution using numpy.histogram"""
    if avg is None:
        avg=1
    if avg_step==0:
        points      = running_mean(data, avg)
    elif avg_step > 0:
        points      = stepwise_mean(data, avg, avg_step)
    else:
        print 'invalid avg_step {}'.format(avg_step)
        return None
    bins = define_bins(points, num_bins)
    test        = np.histogram(points, bins[:, 1], density = False)[0]
    if sgauss:
        fgauss  = gauss_fit(np.array(bins[1:,0]), np.array(test)) 
        out     = np.array([np.array(bins[1:,0]),np.array(test), np.array(fgauss)])
    else:
        out         = np.array([np.array(bins[1:,0]),np.array( test)])
    del test, avg, points, bins
    return out

def quot_pos_neg(bins): 
    quot = np.array((0,0)) 
    bin     = []
    val     = []
    cutoff  = 1*10**(1)
    for i in range(len(bins[0,:])):
        # compare bin centers
        if bins[0,i] < 0:
            for j in reversed(range(len(bins[0,:]-i))):
                if (np.allclose([bins[0,j]],[ -bins[0,i]], 1e-05, 1e-08,
                    False) & (bins[0,j] <= cutoff)) :
                    # - construct new array with bin center, and ratio
                    if bins[1,i] != 0:
                        bin.append(-bins[0,i])
                        val.append((bins[1,j] / bins[1,i]))
                        break
        else:
            break
    bin = np.flipud(np.array(bin))
    val = np.flipud(np.array(val))
    out = np.array([bin, val])
    del bin, val, bins
    return out 

def ft_analysis(pdf, dtime, avg, sgauss = False):
    """computes the FT for input PDF"""
    # 1/t
    avgt    = 1/ (dtime * avg)
    bins    = []

    if sgauss:
        bins    = np.array([pdf[0,:],pdf[2,:]])
    else:
        bins    = np.array([pdf[0,:],pdf[1,:]])

    quot    = quot_pos_neg(bins)

    ft      = [[],[]]
    # turn ratio into ft-like logarithmic distribution.
    print quot.shape[1]
    if quot.shape[1] > 1:
        for i in range(len(quot[1])):
            if quot[1,i] != 0:
                #ft[1].append(avgt * np.log(quot[1, i]))
                ft[1].append(       np.log(quot[1, i]))
                ft[0].append(quot[0,i])
            else:
                continue
    else:
        print "There is not enough data to conduct a ft analysis"
        return None
    ft      = np.array(ft)
    return ft

def autocorrelation(data):
    """computes the autocorrelation as a function of k, of a data set.
       input: data, as an 1Darray 
       output: correlation values, position in array = k   
       """
    print "autocorr here"
    max         = 1000
    x           = np.reshape(data, len(data))[:max]
    n           = len(x)
    variance    = x.var()
    x           = x - x.mean()
    print "going into np.correlate"
    r           = np.correlate(x[:n], x[:n], mode = 'full')[-n:] 
    #assert np.allclose(r, np.array([x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    result      = r/(variance*(np.arange(n, 0, -1)))
    return result

def autocorrelation_taubenheim(data):
    """computes autocorrelation using taubenheim algorithm
        derelict"""
    print len(data)
    max         = 200000
    x           = np.reshape(data, len(data))  [:max]
    n           = len(x)
    m           = n//20
    mean        = x.mean()
    mean_sq     = mean**2
    c_zero      = ((x*x).mean()-mean_sq)/n
    c           = []
    c           = np.append(c, c_zero)
    for tau in range(1, m-1):
        nr      = n-tau-1
        #xxsum   = np.convolve(x[:(n-tau)],x[tau:])/nr
        xxsum   = np.mean(x[:(n-tau)]*x[tau:])
        mean_sq = x[:(n-tau)].mean()*x[tau:].mean()
        c       = np.append(c, (xxsum-mean_sq)/nr)
       # c       = np.append(c, (x[:(n-tau)]*x[tau:]).mean()-mean_sq)
    return c/c[0]

def decorrelation_time(data, dtime):
    """computes decorrelation time of dataseries"""
    corr_tau    = autocorrelation_taubenheim(data)
    # - find first index at which correlation = 0
    bound       = 10**(-3)
    k           = np.argwhere(corr_tau<bound)       

    if len(k)<1:
        print 'decorr: data set did not reach decorrelation time.'
        #plt.plot(corr_tau)
        #plt.show()
        return None
    else:
        print 'decorr: The decorrelation time is {}'.format(k[0]*dtime/3600)
        #plt.plot(corr_tau)
        #plt.show()
        return k[0]

def optimize_discard(data):
    """uses scipy.optimize.minimize to minimize
       the amount of discarded data points by minimizing 
       the decorrelation time"""
    pass
# fidgety and not yet to be called out!!!
#    return minimize(decorrelation_time, data, method='nelder-mead')


def lin_reg(data):
    x       = data[0]
    y       = data[1]
    a,b     = st.linregress(x,y)[:2]
    print a,b
    return a*x+b

def findminmax_dict(dict, name, pos = 0):
    min = None
    max = None
    minh= 0
    maxh= 0
    for key, value in dict.iteritems():
        if -1 != key.find(name):
            print value
            minh    = np.amin(value[:, pos])
            maxh    = np.amax(value[:, pos])
            if min == None:
                min = minh
            elif minh < min:
                min = minh
            if max == None:
                max = maxh
            elif maxh > max:
                max = maxh

            print min
            print max
    return min, max












    
    


