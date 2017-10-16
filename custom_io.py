import numpy as np
import os
import sys
from scipy import io as scio

def remove_whites(strings):
    nowhites = []
    for string in strings:
        nowhites.append(string.strip())
    return nowhites

def remove_oddchars(name):
    """removes all non chars or digits from a string"""
   
    chars = list(name)
    out_name = ''
    for char in chars:
        if char.isdigit() or char.isalpha():
            out_name += char
        else:
            pass
    return out_name

def clean_oddchars(names):
    """removes all non chars or digits from array of strings"""
    out_names = []
    for name in names:
        out_names.append(remove_oddchars(name))
    return out_names

def names_cleanup(names):
    """nasty cleanup routine"""
    # - fast alle sind via , getrennt
    c_names = np.array(names.split(','))
    # - nur der erste und zweite Eintrag nicht
    #help = c_names[0].split()
    #print help
    # - rejoin scnd entry
    #help = np.array([help[0], (help[1]+help[2])])
    # - der letzte Eintrag ist versehentlich mit . getrennt
    #help2 = np.array(c_names[len(c_names)-1].strip('.').split('.'))

    #help    = np.concatenate((help, c_names[1:len(c_names)-1], help2[0:2]))
    # - remove all spaces from strings
    names = remove_whites(c_names)
    return clean_oddchars(names)
   
def resort_array(data):
    """Function changes from a column of lines
       to a line of columns.
       """
    # - length of lines. 
    lenx    = len(data[0])
    # - length of columns. 
    leny    = len(data) 
    out     = []
    # - step the lines
    for i in range(lenx):
        out.append([])
        # - step the columns
        for j in range(leny):
            out[i].append(data[j][i])
    
    return out

def read_file(file_name):
    """reads contents of a file line by line
    
        first line is assumed to contain variable names
        lines below are values in columns
    """
    file = open((file_name), 'r')
    lines = file.readlines()
    file.close()
    
    data = []
    names= names_cleanup(lines[0])

    for line in lines[1:]:
        a = line.split() 
        data.append([float(i) for i in a])

    data        = resort_array(data)
    data_dict   = {}
    for i in range(len(names)):
        data_dict[names[i]] = data[i][:]

    return data_dict 
def concat_dicts(dicta, dictb):
    dict_out = {}
    for key in dicta.iterkeys():
        if key in dictb:
            dict_out[key]   = np.ma.concatenate((dicta[key],dictb[key]), 0)
        else:
            dict_out[key]   = np.ma.concatenate((dicta[key], []),0)
    return dict_out

def read_files(file_names):
    """reads contents of a file line by line
    
        first line is assumed to contain variable names
        lines below are values in columns
    """
    data        = []
    data_out    = {}

    for file_name in file_names:
        data.append(read_file(file_name))
        print '{} read and appended'.format(file_name)

    data_out    = data[0] 
    for i in range(1, len(data)):
        data_out    = concat_dicts(data_out, data[i])

    return data_out 

def read_matlab(file):
    """reads content of a matlab data file

        needed new routine different stuff
    """
    data    = scio.loadmat(file)
    
    return data

def find_var(lines):
    """reads variables and their values within lines of
        NAMELIST_ICON.
        """
    # create empty name_list dictionary. 
    name_list = {}
    for line in lines:
        # find lines which contain variables 
        # omit the ones which are commented out
        # and others. it ain't pretty...
        if not  (   len(line.strip()) == 0   or
                    line.strip()[0]   == '!' or
                    line.strip()[0]   == '&' or
                    line.strip()[0]   == '/'
                    ):

            # remove trailing comments
            rem_com         = line.split('!')
            key, var        = remove_whites(rem_com[0].split('='))
            name_list[key]  = var
        else:
            pass
    return name_list 

def convert_boolean(fbool):
    """converts Fortran Booleans to python Booleans"""
    if fbool == '.TRUE.':
        return True
    if fbool == '.FALSE.':
        return False

def get_name_list(fdir):
    """extracts information on variable values in NAMELIST_ICON"""
    fpath   = fdir + 'NAMELIST_ICON'
    file = open((fpath), 'r')
    lines = file.readlines()
    file.close()
    # prepare name_list dictionary
    name_list = find_var(lines) 
    for key, value in name_list.iteritems(): 
        # strings are signified by '' in NAMELIST_ICON
        if value.strip("'").isalpha():
            name_list[key] = str(value.strip("'"))
        # clear
        elif value.isdigit():
            name_list[key] = float(value)
        # Booleans are signified by .bool. in NAMELIST_ICON
        elif value.strip(".").isalpha():
            name_list[key] = convert_boolean(value)
    return name_list

def write_analysis(data, name, odir)
