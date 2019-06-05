#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
import oyaml as yaml

from sys import path

# Run pytest in the top folder, the current folder is where pytest runs
from prototype.python import method_translator

def test_get_inputs():
    file = 'tests/test_python/test_method_parser/grad_f.yml'
    with open(file, 'r') as yf:
        yaml_series = yaml.load(yf)
    inputs = method_translator.get_inputs(yaml_series)
    assert inputs == [{name:'X_val', type:'float', length:1}]


def test_translate_file():
    file = 'tests/test_python/test_method_parser/grad_f.yml'
    translated_text = method_translator.translate_method_file(file)
    assert
