#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
import oyaml as yaml

from sys import path
from collections import OrderedDict

# Run pytest in the top folder, the current folder is where pytest runs
from prototype.python import element_translator

def test_analyze_inputs():
    input_names = ['A_1', 'A_2', 'A_3']
    template_inputs = [OrderedDict([('array_name', 'input_'), ('length', ''), ('type', 'float')])]
    real_inputs = element_translator.analyze_inputs(input_names, template_inputs)
    assert real_inputs == {'input_': ['A_1', 'A_2', 'A_3']}

def test_analyze_outputs():
    template_outputs = [OrderedDict([('name', 'output'), ('length', '=1'), ('type', 'float')])]
    output_name = ['Alpha']
    real_output = element_translator.analyze_outputs(output_name, template_outputs)
    assert real_output == {'output': 'Alpha'}

def test_parse_code():
    code = '<output> := <command_text>'
    parsed_code = element_translator.parse_code(code)
    assert parsed_code == [{'var': 'output'}, {'text': ' := '}, {'var': 'command_text'}]

def test_translate_single_code_1():
    # input_dict = {'input_[0]': 'A_1', 'input_[1]': 'A_2', 'input_[2]': 'A_3'}
    input_dict = {'input_': ['A_1', 'A_2', 'A_3']}
    output_dict = {'output': 'Alpha'}
    preprocess_string = "# Python 3 commands\ncommand_text = \"<input_[0]>\"\nfor k in range(1, len(input_)):\n  command_text += \" + <input_[\" + str(k) + \"]>\""
    code_string = "<output> := <command_text>"
    postprocess_string = ''
    code = element_translator.translate_single_code(input_dict, output_dict,\
    preprocess_string, code_string, postprocess_string)
    assert code == "Alpha := A_1 + A_2 + A_3"

def test_translate_single_code_2():
    # input_dict = {'input_[0]': 'A_1', 'input_[1]': 'A_2', 'input_[2]': 'A_3'}
    input_dict = {'input_': ['A_1', 'A_2', 'A_3']}
    output_dict = {'output': 'Alpha'}
    preprocess_string = "# Python 3 commands\ncommand_text = \"<input_[0]>\"\nfor k in range(1, len(input_)):\n  command_text += \" + <input_[\" + str(k) + \"]>\""
    code_string = "<output> := <command_text>"
    postprocess_string = '# Python 3 commands\ncomment_code = \'//Sum of \' + str(len(input_)) + \' variables\\n\'\nfinal_code = comment_code + code\nprint(code)'
    print(postprocess_string)
    code = element_translator.translate_single_code(input_dict, output_dict,\
    preprocess_string, code_string, postprocess_string)
    assert code == "//Sum of 3 variables\nAlpha := A_1 + A_2 + A_3"


def test_translate_el_short():
    module_file = 'tests/test_python/test_element_translator/averaging.yml'
    command = OrderedDict([('add', ['A_1', 'A_2', 'A_3'])])
    # mydict = OrderedDict([('averaging', OrderedDict([('type', 'function'), ('inputs', [OrderedDict([('name', 'A_1'), ('type', 'float')]), OrderedDict([('name', 'A_2'), ('type', 'float')]), OrderedDict([('name', 'A_3'), ('type', 'float')])]), ('outputs', None), ('commands', [OrderedDict([('add', ['A_1', 'A_2', 'A_3'])])])]))])
    element_file = 'prototype/yaml/methods/add__float.yml'
    descriptor_file = 'prototype/yaml/descriptors/add__float.c'
    translated_text = element_translator.translate_command_element(command, element_file, descriptor_file)
    assert translated_text == 'A_1 + A_2 + A_3'
