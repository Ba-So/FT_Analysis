import custom_io as io
import data_manip as dm
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


def test_names_cleanup():
    dir     = '/home/kastor+pollux/kd031/icon-hex/experiments/FT_LONG_HS_JW_90/'
    fname   = 'total_ddtkin_0001.dat'
    file    = open((dir +fname), 'r')
    lines   = file.readlines()
    file.close() 

    names   = io.names_cleanup(lines[0])
    print names

def test_valdic():
    dir     = '/home/kd031/iconana/source/HS1/'
    fname   = 'total_integrals_0001.dat'
    val_dic = io.read_file(dir+fname)
    for key in val_dic:
        print key
        print type(val_dic[key])

def test_compute_e():
    dir     = '/home/kd031/iconana/source/HS1/'
    fname   = 'total_integrals_0001.dat'
    data = io.read_file(dir + fname)
    keys = ['kine', 'pote', 'inne'] 
    en_mean = dm.compute_e(data, keys) 
    for key, value in en_mean.iteritems():
        if -1 == key.find('_mean'):
            print 'len({}): {}, val00: {}'.format(key, len(value), value[1])
        elif not -1 == key.find('_mean'):
            print '{}: {}'.format(key, value)
        else:
            pass

def test_read_file():
    dir     = '/home/kd031/iconana/source/HS1/'
    fname   = 'total_integrals_0001.dat'
    data = io.read_file(dir + fname)
    keys = ['kine', 'pote', 'inne'] 

    for key, value in data.iteritems():
        print 'len({}): {}'.format(key, len(value))

def test_define_bins():
    data        = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    data2       = [-3, -2, -1, 0, 1, 2, 3]
    num_bins    = 10
    num_bins2   = 6
    check_bins  = [[0.5 + i, 0 + i, 1 + i, 0] for i in range(num_bins)]
    chk_bins2   = [[-2.5+i, -3+i,-2+i,0 ] for i in range(num_bins2)]
    bins        = dm.define_bins(data, num_bins)
    bins2       = dm.define_bins(data2, num_bins2)
    if (bins == check_bins).all():
        print 'check'
    else:
        print 'nope, still work to do'
    if (bins2 == chk_bins2).all():
        print 'check'
    else:
        print 'nope, still work to do'
    for i in range(10):
        data3       = [randint(0,20) for i in range(30)]
        num_bins3   = randint(1,30) 
        bins3       = dm.define_bins(data3, num_bins3)
        if (len(bins3) == (num_bins3)):
            print 'check'
        else:
            print bins3
            print num_bins3
            print bins3
            print 'bugger is making to many or to few bins'

    for i in range(10):
        data3       = [randint(-20,20) for i in range(30)]
        num_bins3   = randint(1,30) 
        bins3       = dm.define_bins(data3, num_bins3)
        if (len(bins3) == (num_bins3)):
            print 'check'
        else:
            print bins3
            print num_bins3
            print bins3
            print 'bugger is making to many or to few bins'


def test_PDF():
    data        = [i for i in range(0,31)]
    check_bins  = [[0.5 + i, 0 + i, 1 + i, 1] for i in range(num_bins)]

def test_mean():
    data1       = [2,2,2,2,2,2]
    data2       = 2

    if dm.mean(data1) == 2:
        print "test1 pass"
    if dm.mean(data2) == 2:
        print "test2 pass"
    if dm.mean('huhu') == None:
        print "test3 pass"

def test_compute_avg_t():
    data    = [i for i in range(0, 22)]
    avg     = 2
    check_points = [0.5 + i for i in range(0,20)]
    print check_points
    points  = dm.compute_avg_t(data, avg)
    print points
    if (points == check_points).all():
        print 'yes'
    else:
        print 'nope'

def test_running_mean():
    data    = [i for i in range(0, 22)]
    avg     = 2
    check_points = np.array([0.5 + i for i in range(0,21)])
    print check_points
    points  = dm.running_mean(data, avg)
    print points
    if (points == check_points).all():
        print 'yes'
    else:
        print 'nope'

def test_compute_pdf():
    data        = [randint(-30,30) for i in range(0, 64200)]
    avg         = 1
    num_bins    = 10 
    chk_pdf     = [[0.5 + i, 0 + i, 1 + i, 0] for i in range(num_bins)]

    pdf         = dm.compute_pdf(data, avg)
    print pdf 
    avg = 2
    pdf         = dm.compute_pdf(data, avg)
    print pdf 
    avg = 3
    pdf         = dm.compute_pdf(data, avg)
    print pdf 

def test_quot_pos_neg():
    bins  = [[(i-1)*2+1, (2 * (i-1)),(2*i), 10+i] for i in range(-9, 11)]
    quot  = dm.quot_pos_neg(bins)
    print bins
    print quot 

def test_ft_analysis():
    dtime   = 10
    avg     = 2 
    bins  = [[(i-1)*2+1, (2 * (i-1)),(2*i), 10+i] for i in range(-9, 130)]
    ft = dm.ft_analysis(bins, dtime, avg)
    # no clue as how to check it really...
    print ft

def test_read_matlab():
    file_name   = 'den_data.mat'
    file_path   = '/home/kd031/iconana/source/'
    data        = io.read_matlab(file_path + file_name)    
    print type(data)
    for key in data.iterkeys():
        print key

def test_concat_dicts():
    dicta       = {'a': [1,2,3], 'b': [10,11,12], 'c':[3,6,9]}
    dictb       = {'a': [4,5,6], 'b': [13,14,15]}
    dict_exp    = {'a': [1,2,3,4,5,6], 'b': [10,11,12,13,14,15], 'c':[3,6,9]}
    dict_test   = {}

    dict_test   = io.concat_dicts(dicta, dictb)
    test_is     = False
    print dict_test
    for key in dict_exp.iterkeys():
        if (dict_exp[key] == dict_test[key]).all():
            test_is = True
        else:
            print 'stuff to do'
            break
    if test_is:
        print dict_test
        print 'pass'

def test_gauss_fit():
    x   = np.arange(10)
    y   = np.array([0,1,2,3,4,5,4,3,2,1])
    y2  = dm.gauss_fit(x, y)
    plt.plot(x, y, 'b+:', label='data')
    plt.plot(x, y2, 'r-', label='fit')
    plt.show()

if __name__== '__main__':
    #test_names_cleanup()
   #test_valdic()
   #test_compute_e()
   #test_read_file()
   #test_mean()
   #test_compute_avg_t()
   #test_define_bins()
   #test_running_mean()
   #test_compute_pdf()
   #test_quot_pos_neg()
   #test_ft_analysis()
   #test_read_matlab()
   #test_concat_dicts()
   test_gauss_fit()

