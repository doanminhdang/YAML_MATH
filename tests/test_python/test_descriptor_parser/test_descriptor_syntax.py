#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

from sys import path

# Run pytest in the top folder, the current folder is where pytest runs
from prototype.python import descriptor_parser

def test_check_descriptor_syntax_file():
    descriptor_file = 'tests/test_python/test_descriptor_parser/assign.c'
    check_flag, error_message = descriptor_parser.check_descriptor_syntax_file(descriptor_file)
    assert check_flag == True
