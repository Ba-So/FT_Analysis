import os
import sys
import numpy as np
import time
import custom_io as io
import data_manip as dm
import plot as plt


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

# What do I need this to do?
# a Routine that computes the fancy Probability Distributions
# a Routine that prints it all using Ngl
# 
def run_this(dir, project_name, file_name, odir):
    #fancy time counting
    t1 = count_time()

    data = io.read_file((dir + file_name))
    # extracts information from NAME_LIST
    name_list = io.get_name_list(dir)
#    for i in range(1, len(names)):
#        plt.print_xy_ngl(data[i], names[i], odir)
     
#    print name_list
    # get energy budget and mean values
    keys = ['kine', 'inne', 'pote']
    data    = dm.make_relative(data, keys)
    en_mean = dm.compute_e(data, keys)
    # print 'em
    fname   = 'E_Budget'
# - Specify values to be plotted 
    #keys = ['kine', 'inne', 'pote', 'tote', 'kine_mean', 'inne_mean',
    #'pote_mean', 'tote_mean']
    keys = ['etot', 'etot_mean']
    #keys = ['pote', 'pote_mean']
#    plt.print_xy_ngl_dict(en_mean, name_list, odir, fname, keys)    

    Ngl.end() 
    #fancy time counting
    count_time(t1)

def run_this2(dir, pname, fname, odir):
    t1 = count_time()
    # read data from file
    data = io.read_file((dir + pname + fname))
    # extracts information from NAME_LIST
    name_list = io.get_name_list(dir + pname)
    dtime = name_list['dtime']
    keys  = ['advK', 'hadvTheta', 'gradp', 'totalddtekin']
    ft_out= {}
    num_bins = 60
    avg      = 4
    pdf_keys = []
    ft_keys  = []
    for avg in range(4, 20):
        for key in keys:
            pdfname     = '_pdf_{}'.format(avg * dtime)
            ftname      = '_ft_{}'.format(avg * dtime)
            ft_out[key+pdfname] = dm.compute_pdf(data[key], avg, num_bins)
            pdf_keys = np.append(pdf_keys, key+pdfname)
            ft_out[key+ftname] = dm.ft_analysis(ft_out[key+pdfname], dtime, avg) 
            ft_keys  = np.append(ft_keys, key+ftname)

    for key in keys:
        give_pdf    = []
        give_ft     = []
        pdf_dic     = {}
        ft_dic      = {}
        for name in ft_out:

            if ( (-1 != name.find(key) )  and (-1 != name.find('pdf') ) ):
                give_pdf.append(name) 
            elif ( (-1 != name.find(key) ) and (-1 != name.find('ft') ) ):
                give_ft.append(name)

        pdf_dic     = dm.interpolate(ft_out, key+'_pdf')
#        plt.print_xy_ngl_ft(pdf_dic, name_list, odir)

        ft_dic     = dm.interpolate(ft_out, key+'_ft')
#        plt.print_xy_ngl_ft(ft_dic, name_list, odir) 

    del data    

    Ngl.end()
    count_time(t1)

def denny_test(data, out_path, num_bins, avg, avg_step=0):
    print 'number of bins {}, steps averaged over: {}'.format(num_bins, avg)
    # - compute timestep width
    dtime       = data['t'][1]-data['t'][0]
    print 'tau = {}'.format(dtime*avg)
    # - compute pdf
    print 'averaging step width_ {}'.format(avg_step)
    print 'computing histogram (pdf)'
    pdf_out     = dm.compute_pdf(data['P'], avg, num_bins, avg_step)

    # - compute ft from pdf:H
    print 'analysing relation of fluctuations (ft)'
    ft_out      = dm.ft_analysis(pdf_out, dtime, avg)
    lin_reg     = dm.lin_reg(ft_out)
    ft_out      = np.concatenate((ft_out, [lin_reg]))

    # - print
    param       = [num_bins, avg, avg_step]
    return ft_out


if __name__== '__main__':
   # idir  = '/home/kastor+pollux/kd031/icon-hex/experiments/'
   # pname = 'FT_LONG_HS_JW_90/'
   # fname = 'total_ddtkin_0001.dat'
   # odir        = '/home/kd031/iconana/output/'
   # run_this2(idir, pname, fname, odir)
   # fname    = 'den_data.mat'
   # fpath    = '/home/kd031/iconana/source/'
    file_name   = 'den_data.mat'
    file_path   = '/home/kd031/iconana/source/'
    print 'loading data set'
    data        = io.read_matlab(file_path+file_name)    
    out_path    = '/home/kd031/iconana/output/'
    num_bins    = 1000
    avg         = [150, 225, 300, 450, 600]
    avg_step    = 0
    data_lst    = []
    decorr      = dm.decorrelation_time(data['P'], data['t'][1]-data['t'][0])
    print "The decorrelation time is:"
    print decorr
    print "computing: ft's"
 #   for i in avg:
  #      data_lst.append( denny_test(data, out_path, num_bins, i, avg_step))

   # name            = 'den_dat_step_sin_avg'

  #  print 'output: printing ft and linear regression'
  #  plt.plot_xy(data_lst)
    

