#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
import oyaml as yaml

from sys import path
from collections import OrderedDict

# Run pytest in the top folder, the current folder is where pytest runs
from prototype.python import method_parser
from prototype.python import utils
from prototype.python.shared_parameters import *

def test_read_group_1():
    file = 'tests/test_python/test_method_parser/averaging.yml'
    yaml_block = utils.yaml_file_read(file)
    group = method_parser.read_group(yaml_block)
    assert group == group_function_id

def test_read_group_2():
    file = 'tests/test_python/test_method_parser/add.yml'
    yaml_block = utils.yaml_file_read(file)
    group = method_parser.read_group(yaml_block)
    assert group == group_element_id

def test_get_inputs():
    file = 'tests/test_python/test_method_parser/grad_f.yml'
    yaml_series = utils.yaml_file_read(file)
    inputs = method_parser.get_inputs(yaml_series)
    assert inputs == [OrderedDict([('name','X_val'), ('type','float'), ('length',1)])]

def test_get_outputs():
    file = 'tests/test_python/test_method_parser/grad_f.yml'
    yaml_series = utils.yaml_file_read(file)
    inputs = method_parser.get_outputs(yaml_series)
    assert inputs == [OrderedDict([('name','Grad_f_val'), ('type','float'), ('length',1)])]
