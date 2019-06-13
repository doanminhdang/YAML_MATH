#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

from sys import path

# Run pytest in the top folder, the current folder is where pytest runs
from prototype.python import descriptor_parser
from prototype.python.shared_parameters import *

def test_descriptor_parse():
    preprocess_string = "# Python 3 commands\ncommand_text = \"<input_[0]>\"\nfor k in range(1, len(input_)):\n  command_text += \" + <input_[\" + str(k) + \"]>\""
    code_string = "<output> := <command_text>"
    postprocess_string = '# Python 3 commands\ncomment_code = \'//Sum of \' + str(len(input_)) + \' variables\\n\'\nfinal_code = comment_code + code\nprint(code)'
    descriptor_text = descriptor_preprocess_label + '\n' + descriptor_part_opening\
      + '\n' + preprocess_string + '\n' + descriptor_part_closing + '\n'\
      + descriptor_midprocess_label + '\n' + descriptor_part_opening + '\n'\
      + code_string + '\n' + descriptor_part_closing + '\n'\
      + descriptor_postprocess_label + '\n' + descriptor_part_opening + '\n'\
      + postprocess_string + '\n' + descriptor_part_closing
    descriptor_components = descriptor_parser.descriptor_parse(descriptor_text)
    assert descriptor_components['preprocess'] == preprocess_string
    assert descriptor_components['code'] == code_string
    assert descriptor_components['postprocess'] == postprocess_string
