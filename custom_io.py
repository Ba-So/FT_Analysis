import numpy as np
import pandas as pd
import os
import sys
from scipy import io as scio
import xarray as xr

def read_netcdfs(files, dim, kwargs=None, func=None):
  """
        reads data from .nc files:
        path: Path to file
        qty : qty to be read
        """
  def process_one_path(path):
    # use a context manager, to ensure file gets closed after read
    with xr.open_dataset(path) as ds:
      #transform_func should do some sort of selection
      # or aggregation
      if func is not None:
        ds = func(ds, kwargs)
      # Load all data from the transformed dataset, to ensure we
      # use it after closing each original file
      ds.load()
      return ds

#  paths   = sorted(glob(files))
  paths = files
  datasets = [process_one_path(p) for p in paths]
  combined = datasets[0]
  if len(datasets) > 1:
    combined = xr.concat(datasets, dim)
  return combined

def extract_variables(ds, variables):

  def take_one_variable(var, ds):
    return ds[var]

  #variables = ['U', 'V']
  data = {}
  for var in variables:
      data[var] = take_one_variable(var, ds)

  ds_o = xr.Dataset(data)

  # for convienience.
 # ds_o = ds_o.rename({
 #         'cell2' : 'ncells',
 #         'vlon' : 'clon',
 #         'vlat' : 'clat'
 #         })

  return ds_o

def read_file(file_name):
    """reads contents of a file line by line

        first line is assumed to contain variable names
        lines below are values in columns
    """

    data   = pd.read_csv(file_name, sep=',', header=0)
    data_dict = data.to_dict('list')

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

