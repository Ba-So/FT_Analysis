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
    # data        = io.read_files(file_name)

    quarks = {
        'variables' : ['t_fric']
    }
    data = {}
    func = lambda ds, quarks: io.extract_variables(ds, **quarks)
    data_s      = io.read_netcdfs(file_name, 'time', quarks, func)
    data_s = data_s['t_fric'].values
    print data_s[1,1,3:10]
    data['t_fric'] = np.reshape(data_s, np.prod(data_s.shape))
    print data['t_fric'][3:10]

    for key in data.iterkeys():
        print key

    num_bins    = 300
    avg_step    = 0
    data_lst    = []
    data_lst2   = []
    num_step_day   = 720
    disc_days       = 0
    disc        = disc_days * num_step_day
    dtime       = 120

    #----------------
    name        = 'turbulent_friction'
    print '#--------------------'
    print '# processing {}'.format(name)

    ddtsint = dc.FRData(name,r'\sigma', r'\lbrack \frac{J}{K \cdot s} \rbrack', data['t_fric'], dtime, disc)
    print ddtsint.data.shape
    ddtsint.pdf = ddtsint.compute_pdf(None)
    ddtsint.tau_c = 3
    ddtsint.fr = ddtsint.compute_fr(ddtsint.pdf)
    # ddtsint.compute_multiple(2)
    ddtsint.plot_pdf()
    ddtsint.plot_fr()
    ddtsint.plot()
    print type(ddtsint.data)

    #----------------
  #  name        = 'ddt_s_hsf'
  #  print '#--------------------'
  #  print '# processing {}'.format(name)#

  #  ddtshsf = dc.FRData(name,r'\sigma', r'\lbrack \frac{J}{K \cdot s} \rbrack', data[name], dtime, disc)
  #  ddtshsf.compute_multiple(2)
  #  ddtshsf.plot_pdf()
 #   ddtshsf.plot_fr()

    #----------------
  #  name        = 'ddt_einn_hsf'
  #  print '#--------------------'
  #  print '# processing {}'.format(name)

  #  ddteihsf= dc.FRData(name,r'\sigma', r'\lbrack \frac{J}{K \cdot s} \rbrack', data[name], dtime, disc)
  #  ddteihsf.compute_multiple(2)
  #  ddteihsf.plot_pdf()
  #  ddteihsf.plot_fr()

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
    for file in sorted(glob.glob(file_path+'HS_FT_6000_days*refined*.nc')):
       file_name.append(file)
       print('appended: {}').format(file)

    out_path    = '/home/kd031/projects/now/output/'
    # denny_test()
    analyse_and_plot(file_path, file_name, out_path)
    count_time(t1)
