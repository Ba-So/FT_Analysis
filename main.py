import os
import sys
import numpy as np
import time
import copy
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

def denny_test():

    path='/home/kd031/projects/now'
    file='/source/den_data.mat'
    odir=path + '/output/'

    data = io.read_matlab(path + file)

    num_bins = 100
    avg      = 50
    avg_step = 0

    print 'number of bins {}, steps averaged over: {}'.format(num_bins, avg)
    # - compute timestep width
    dtime       = data['t'][1]-data['t'][0]
    for key in data.iterkeys():
        print key

    print 'tau = {}'.format(dtime*avg)
    # - compute pdf
    ft_analyse(data['P'], 3*avg, num_bins, odir, dtime, 5)
    return

def analyse_data(data, dtime, num_bins, avg, sgauss, avg_step=0):

    true_data   = []
    pdf_out     = dm.compute_pdf(data, avg, num_bins, sgauss, avg_step)    
    ft_out      = dm.ft_analysis(pdf_out, dtime, avg, sgauss)
    if not(ft_out is None):
        lin_reg     = dm.lin_reg(ft_out)
        ft_out      = np.concatenate((ft_out, [lin_reg]))
        return ft_out, pdf_out
    else:
        return None, pdf_out

def ft_analyse(data, avg, num_bins, out_path, dtime, fancy, sgauss, max=2):
    data_lst    = []
    data_lst2   = []
    th          = np.array([avg * i for i in range(1,max)])
    xlab        = fancy['xlabel']
    fancy['label'] = ['data', 'fit']
    fancypdf    = copy.deepcopy(fancy)
    fancypdf['xlabel']= r'${}$'.format(xlab)
    fancypdf['ylabel']= r'PDF(${}$)'.format(xlab)
    fancypdf['title'] = r'propability distribution function of ${}$'.format(xlab)
    fancyft    = copy.deepcopy(fancy)
    fancyft['xlabel']= r'${}$'.format(xlab)
    fancyft['ylabel']= r'$ln\left(\frac{ PDF(-' + r'{}'.format(xlab) \
                     + r')}{PDF(' + r'{}'.format(xlab) + r')}\right)$'
    fancyft['title'] = 'Fluctuation Relation for ${}$'.format(fancy['xlabel'])

    for ths in th:
        print 'tau={}'.format(ths)
        helper, helper2 = analyse_data(data, dtime, num_bins, ths, sgauss)
        if not(helper is None):
            data_lst.append(helper)
            data_lst2.append(helper2)
            if sgauss:
                helper, helper2 = analyse_data(data, dtime, num_bins, ths, False)
                data_lst.append(helper)
        else:
            data_lst2.append(helper2)
            plt.plot_xy(data_lst2, out_path+'_pdf', fancypdf)    
            if not(data_lst == []):
                plt.plot_xy(data_lst, out_path + '_ft', fancyft)    
            return
    plt.plot_xy(data_lst2, out_path+'_pdf', fancypdf)    
    plt.plot_xy(data_lst, out_path + '_ft', fancyft)    
    #plt.plot_x(data, out_path)

def relate_e(data, out_path):
    # to get a hold of the relations of energies to one another
    pass

def analyse_and_plot(file_path, file_name, out_path):

    print 'loading data set'
    for i in range(len(file_name)):
        file_name[i] = file_path + file_name[i]
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
    sgauss      = False

    #plt.plot_x_avg([data['epothsf'][disc::]], idir+pname + 'compare')
    name        = 'ddteinnhsf'
    print '#--------------------'
    print '# analysing {}'.format(name)

    #plt.plot_x_avg([data[name]], out_path + name + 'full')
    #avg         = dm.decorrelation_time(data[name][disc::], dtime)
    #if not(avg is None):
    #    ft_analyse(data[name][disc::], avg, num_bins, out_path
    #            +name + '_ft_{}'.format(disc_days), dtime, sgauss, 4)
    #plt.plot_x_avg([data[name][disc::]], out_path + name)

    #----------------
    name        = 'ddtsint'
    print '#--------------------'
    print '# analysing {}'.format(name)

    fancy = {'label' : '',
             'title': r'material entropy production rates $\bar{\sigma}_t$ [J/(s K)]',
             'xlabel': 'time steps',
             'ylabel': r'$\bar{\sigma}_t$'} 
    avg         = dm.decorrelation_time(data[name][disc::], dtime)
    #plt.plot_x_avg([data[name]], out_path + name + 'full', fancy, [disc])
    if not(avg is None):
       fancy = {'label' : '', 'title': 'material entropy production rates',
                'xlabel': r'\bar{\sigma}_t', 'ylabel': r'\bar{\sigma}_t',
                't_c': avg} 
       ft_analyse(data[name][disc::], avg, num_bins, out_path
               +name + '_ft_{}'.format(disc_days), dtime, fancy, sgauss, 4)

   # plt.plot_x_avg([data[name][disc::]], idir + pname + name, fancy)

    #------------------
    name        = 'ddtshsf'
    print '#--------------------'
    print '# analysing {}'.format(name)
    #plt.plot_x_avg([data[name]], idir + pname + name + 'full')
    #avg         = dm.decorrelation_time(data[name][disc::], dtime)
    #if not(avg is None):
    #    ft_analyse(data[name][disc::], avg, num_bins, idir+pname
    #            +name +'_ft_{}'.format(disc_days), dtime, sgauss, 4)
    #plt.plot_x_avg([data[name][disc::]], idir + pname + name)

    #------------------

if __name__== '__main__':
    idir        = '/home/kastor+pollux/kd031/icon-hex/experiments/'
    pname       = 'HS_FT_6000_days/'
    file_name   = ['total_integrals_0001.dat'
                   ,'total_integrals_0035.dat'
                   ,'total_integrals_0069.dat'
                   ,'total_integrals_0103.dat'
                   ,'total_integrals_0137.dat'
                   ,'total_integrals_0171.dat'
               ]
   # odir        = '/home/kd031/iconana/output/'
   # run_this2(idir, pname, fname, odir)
   # fname    = 'den_data.mat'
   # fpath    = '/home/kd031/iconana/source/'
   # file_name   = 'den_data.mat'
   # file_path   = '/home/kd031/iconana/source/'

    file_path   = idir + pname
    out_path    = '/home/kd031/projects/now/output/'
    # denny_test()
    analyse_and_plot(file_path, file_name, out_path)
