#!/usr/bin/env python3

# encoding: utf-8
'''
 -- A basic checker for agggregated files

@author:     Lara Ferrighi, METNO

@contact:    laraf@met.no
'''

import sys
from collections import OrderedDict
from netCDF4 import Dataset

#check how many files are provided
number_of_files = len(sys.argv)-2

#get aggregation variable
agg_var =  str(sys.argv[-1])

#create a list of datasets from argv
datasets = []
dimensions = []
dimsizes = []
variables = []
vatt = []
for i in range(0, number_of_files,1):
    print(i)
    datasets.append(Dataset(str(sys.argv[1+i])))
    # check dimensions name (e.g. lat, lon, ocean_time)
    dimensions.append(datasets[i].dimensions.keys())
    dimsizes.append(OrderedDict())
    for name,dimension in datasets[i].dimensions.items():
        dimsizes[i][name] = dimension.size
    # check variables (e.g. lon, lat, ocean_time, h, MLD)
    variables.append(datasets[i].variables.keys())
    # check variables attributes. key=name (i.e. pressure) and value=list of attribute name (i.e. units)
    vatt.append(OrderedDict())
    for name, variable in datasets[i].variables.items():
        vatt[i][name] = set(variable.ncattrs())


#print("dst =",datasets)
#print("dim =", dimensions)
#print("dsiz =",dimsizes)
#print("var =",variables)
#print("vat =",vatt)

# check that aggregation dimention exists in all files
for a in dimensions[:]:
    if agg_var not in a:
        print("Fail: aggregation dim {} is not present in all files".format(agg_var))
        break
    else:
        print("Pass: aggregation dim {} found in all files".format(agg_var))

# compare dimensions name
for a in dimensions[:-1]:
    if a != dimensions[-1]:
        print("Fail: not the same dim name {} in all files".format(list(a)))
    else:
        print("Pass: same dim name {} in all files".format(list(a)))

#var = [odict_keys(['image', 'validTime', 'valid100thSecs']), 
#       odict_keys(['image', 'validTime', 'valid100thSecs'])]
# compare variables name
for a in variables[:-1]:
    if a != variables[-1]:
        print("Fail: not the same var name {}".format(list(a)))
    else:
        print("Pass: same var name {} in all files".format(list(a)))

#vat = [OrderedDict([('image', {'units', 'standard_name', 'coverage_content_type', 'long_name'}), 
#                     ('validTime', {'units', 'standard_name', 'coverage_content_type', 'long_name'}), 
#                     ('valid100thSecs', {'units', 'standard_name', 'coverage_content_type', 'long_name'})]), 
#       OrderedDict([('image', {'units', 'standard_name', 'coverage_content_type', 'long_name'}), 
#                     ('validTime', {'units', 'standard_name', 'coverage_content_type', 'long_name'}), 
#                     ('valid100thSecs', {'units', 'standard_name', 'coverage_content_type', 'long_name'})])]
# compare variables attributes
for dic in vatt[:-1]:
    for vkey, vvalues in vatt[-1].items():
        if vvalues != dic[vkey]:
            print("Fail: the var {} does not have the same attributes in all files")
        else:
            print("Pass: var {} has the same attributes name {} in all files".format(vkey,list(vvalues)))

# check dimensions size which is not aggregated (e.g lat = 30, lon=40 not ocean_time)
for a in dimsizes[:-1]:
    for dkey, dvalue in dimsizes[-1].items():
        if (dkey != agg_var and dvalue != a[dkey]):
            print("Fail: non aggregated dimension {} differ in size".format(dkey))
        else:
            print("Pass: non aggregated dimension {} is the same in all files".format(dkey))

