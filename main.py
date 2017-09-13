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

def analyse_data(data, dtime, num_bins, avg, avg_step=2):

    pdf_out     = dm.compute_pdf(data, avg, num_bins, avg_step)    
    ft_out      = dm.ft_analysis(pdf_out, dtime, avg)
    if ft_out != None:
        lin_reg     = dm.lin_reg(ft_out)
        ft_out      = np.concatenate((ft_out, [lin_reg]))
        return ft_out, pdf_out
    else:
        return None, pdf_out

def ft_analyse(data, avg, num_bins, out_path, max=2):
    th          = np.array([avg * i for i in range(1,max)])
    for ths in th:
        helper, helper2  = analyse_data(data, 120, num_bins, ths)
        if helper != None:
            data_lst.append(helper)
            data_lst2.append(helper2)
        else:
            data_lst2.append(helper2)

    plt.plot_x(data, out_path)
    plt.plot_xy(data_lst, out_path + '_ft')    
    plt.plot_xy(data_lst2, out_path+'_pdf')    

def relate_e(data, out_path):
    # to get a hold of the relations of energies to one another
    pass


if __name__== '__main__':
    idir        = '/home/kastor+pollux/kd031/icon-hex/experiments/'
    pname       = 'HS_FT_2000_days/'
    file_name   = 'total_ddtkin_0001.dat'
    file_name2  = 'total_ddtkin_0035.dat'
   # odir        = '/home/kd031/iconana/output/'
   # run_this2(idir, pname, fname, odir)
   # fname    = 'den_data.mat'
   # fpath    = '/home/kd031/iconana/source/'
   # file_name   = 'den_data.mat'
   # file_path   = '/home/kd031/iconana/source/'
    print 'loading data set'
    file_path   = idir + pname
    data        = io.read_files([file_path + file_name, file_path + file_name2])    
    for key in data.iterkeys():
        print key

    out_path    = '/home/kd031/iconana/output/'
    num_bins    = 100
    avg         = [150, 225, 300, 450, 600]
    avg_step    = 0
    data_lst    = []
    data_lst2   = []
    ds          = 720
    disc        = 230*720
    plt.plot_x([data['epothsf']], idir+pname + 'compare')
   # avg         = dm.decorrelation_time(data['epothsf'][disc::], 120)
   # if avg != None:
   #     print "The decorrelation time is: {} hours".format(avg*120/(3600))
   # plt.plot_xy_alt(data['epothsf'], idir + pname + 'epothsf')

   # ft_analyse(data['epothsf'][disc::], avg, num_bins, idir+pname +'epothsf', 4)
   # disc        = 300*720
   # ft_analyse(data['epothsf'][disc::], avg, num_bins, idir+pname +'epothsf', 4)
   # disc        = 400*720
   # ft_analyse(data['epothsf'][disc::], avg, num_bins, idir+pname +'epothsf', 4)
