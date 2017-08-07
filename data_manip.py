from __future__ import division
import numpy as np
import custom_io as io

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
    return (cumsum[N:] - cumsum[:-N]) / N

def stepwise_mean(x, N, jump):
    """for jumping values like Denny did"""
    data    = running_mean(x, N)
    out     = []
    for i in range(0, len(data), jump):
        out.append(data[i])
    return out

def define_bins(data, num_bins):
    """defines bins for estimation of PDF"""#
        
    bins      = np.zeros(((num_bins+1), 3))
    if not (isinstance(data, np.ndarray) or isinstance(data, list)):
        print 'input data is not an np.array or list'
        return bins
    else:
        # define bins such, that they are symmetric around zero
        dat_max   = np.amax(data)
        dat_min   = np.amin(data)
        dat_step  = (dat_max-dat_min) / num_bins   
        if dat_min < 0:
            num_l     = -int((dat_min+dat_step) // dat_step)
            if (dat_min+dat_step)%dat_step <0:
                num_l += 1 
            # lower bound of bin
            bins[(num_l), 1] = -dat_step 
            # upper bound of bin
            bins[(num_l+1), 1] = 0
            # center of bin, for plotting
            bins[(num_l+1), 0] = -dat_step/2 
            for i in range((num_l), -1, -1):
                for j in range(2):
                    bins[i, j] = bins[i + 1, j] - dat_step
        else: 
            print "data not a candidate for FT"
            num_l     = 1 
            # lower bound of bin
            bins[0, 1] = 0
            # upper bound of bin
            bins[0, 2] = dat_step 
            # center of bin, for plotting
            bins[0, 0] = dat_step/2 
        for i in range (num_l, (num_bins+1)):
            for j in range(2):
                bins[i, j] = bins[(i - 1), j] + dat_step
        return bins  

def compute_pdf(data, avg, num_bins=30, avg_step=0):
    """creates probability distribution using numpy.historgram"""
    bins = define_bins(data, num_bins)
    if avg_step==0:
        points      = running_mean(data,avg)
    elif avg_step > 0:
        points  = stepwise_mean(data, avg, avg_step)
    else:
        print 'invalid avg_step {}'.format(avg_step)
        return None
    test        = np.histogram(points, bins[:, 1], density = True)[0]
    out         = np.array([np.array(bins[1:,0]),np.array( test)])
    return out

def quot_pos_neg(bins): 
    quot = np.array((0,0)) 
    bin     = []
    val     = []
    for i in range(len(bins[0,:])):
        # compare bin centers
        if bins[0,i] < 0:
            for j in reversed(range(len(bins[0,:]-i))):
                if bins[0,j] == -bins[0,i]:
                    # - construct new array with bin center, and ratio
                    if bins[1,i] != 0:
                        bin.append(-bins[0,i])
                        val.append((bins[1,j] / bins[1,i]))
                        break
        else:
            break
    bin = np.flipud(np.array(bin))
    val = np.flipud(np.array(val))
    return np.array([bin,val])

def ft_analysis(pdf, dtime, avg):
    """computes the FT for input PDF"""
    # 1/t
    avgt    = 1/ (dtime * avg)
    quot    = quot_pos_neg(pdf)
    ft      = []
    # turn ratio into ft-like logarithmic distribution.
    if quot.ndim > 1:
        for i in range(len(quot[1])):
            if quot[1,i] != 0:
                ft.append(np.array([quot[0,i],avgt * np.log(quot[1,i])]))
            else:
                continue

    return np.array(ft)

def interpolate(dict, name, npts = 30):
    """Routine to interpolate values of ft's and pdf's onto one common x"""
    xmin, xmax = findminmax_dict(dict, name, 0)
    xstep = (xmax - xmin) / npts
    xvals = [xmin +(i*xstep) for i in range(0, ( npts+1))]
    yvals = []
    names = []
    out   = {}
    interp= 0
    jarr  = 0
    if -1 != name.find('pdf'):
        jarr = 3
    else:
        jarr = 1

    for key, values in dict.iteritems():
        if -1 != key.find(name):
            names.append(key)
            interp = np.interp(xvals, values[:, 0], values[:, jarr])
            yvals.append(interp)

    out['xval'] = xvals
    for i in range(len(names)):
        out[names[i]] = yvals[i]
    return out
    

            



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












    
    


