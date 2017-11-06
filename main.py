import os
import sys
import glob
import numpy as np
import time
import copy
import custom_io as io
import data_manip as dm
import plot as plt
import data_classes as dc


def count_time(t1=0):
    """little helper that counts the time"""
    if t1 == 0:
        t1 = time.time()
        return t1
    elif t1 != 0:
        t2 = time.time()
        print ''
        print 'Wallclock time: {}'.format(t2-t1)
        print ''
    else :
        print 'Something went horribly wrong'
    return

#def denny_test():
######
#    path='/home/kd031/projects/now'
 ###   file='/source/den_data.mat'
 #   odir=path + '/output/'
#
 #   data = io.read_matlab(path + file)
#
 #   num_bins = 100
  #  avg      = 50
   # avg_step = 0
#
 #   print 'number of bins {}, steps averaged over: {}'.format(num_bins, avg)
  #  # - compute timestep width
   # dtime       = data['t'][1]-data['t'][0]
   # for key in data.iterkeys():
   #     print key
#
 #   print 'tau = {}'.format(dtime*avg)
  #  # - compute pdf
   # ft_analyse(data['P'], 3*avg, num_bins, odir, dtime, 5)
   # return

def analyse_and_plot(file_path, file_name, out_path):

    print 'loading data set'
    data        = io.read_files(file_name)    
    for key in data.iterkeys():
        print key

    num_bins    = 300
    avg_step    = 0
    data_lst    = []
    data_lst2   = []
    num_step_day   = 720
    disc_days       = 400
    disc        = disc_days * num_step_day
    dtime       = 120

    #----------------
    name        = 'ddt_s_int'
    print '#--------------------'
    print '# processing {}'.format(name)

    ddtsint = dc.FRData(name,r'\sigma', r'\lbrack \frac{J}{K \cdot s} \rbrack', data[name], dtime, disc)
    ddtsint.compute_multiple(1)
    ddtsint.plot_pdf()
    ddtsint.plot_fr()

    #----------------
    name        = 'ddt_s_hsf'
    print '#--------------------'
    print '# processing {}'.format(name)

    ddtshsf = dc.FRData(name,r'\sigma', r'\lbrack \frac{J}{K \cdot s} \rbrack', data[name], dtime, disc)
    ddtshsf.compute_multiple(1)
    ddtshsf.plot_pdf()
    ddtshsf.plot_fr()

   # fancy = {'label' : '',
    #         'title': r'material entropy production rates $\bar{\sigma}_t$ [J/(s K)]',
     #        'xlabel': 'time steps',
      #       'ylabel': r'$\bar{\sigma}_t$'} 
    #fancy = {'label' : '', 'title': 'material entropy production rates',
     #        'xlabel': r'\bar{\sigma}_t', 'ylabel': r'\bar{\sigma}_t',
      #       't_c': avg} 

if __name__== '__main__':
    t1          = count_time()
    idir        = '/home/kastor+pollux/kd031/icon-hex/experiments/'
    pname       = 'HS_FT_6000_days/'
    file_path   = idir + pname
    file_name   = []
    for file in sorted(glob.glob(file_path+'*.csv')):
        file_name.append(file)

    out_path    = '/home/kd031/projects/now/output/'
    # denny_test()
    ddtsint = analyse_and_plot(file_path, file_name, out_path)
    count_time(t1)
