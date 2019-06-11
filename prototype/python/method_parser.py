"""
Parse a YAML block for methods, detect whether it is element or function.
"""

from shared_parameters import *

def read_group(yaml_block):
    type = yaml_block['type']
    if type in function_group_types:
        group = group_function_id
    else:
        group = group_element_id
    return group

def get_inputs(yaml_block):
    # yaml_block == OrderedDict([('grad_f', OrderedDict([('type', 'function'), ('inputs', [OrderedDict([('name', 'X_val'), ('type', 'float')])]), ('outputs', [OrderedDict([('name', 'Grad_f_val'), ('type', 'float')])]), ('commands', [OrderedDict([('assign', OrderedDict([('input_left', 'Grad_f_val'), ('input_right', OrderedDict([('add', [OrderedDict([('multiply', [OrderedDict([('value', 2), ('type', 'float')]), 'X_val'])]), OrderedDict([('value', 3), ('type', 'float')])])]))]))])])]))])
    inputs = yaml_block['inputs']
    return inputs

def get_outputs(yaml_block):
    yaml_block == OrderedDict([('grad_f', OrderedDict([('type', 'function'), ('inputs', [OrderedDict([('name', 'X_val'), ('type', 'float')])]), ('outputs', [OrderedDict([('name', 'Grad_f_val'), ('type', 'float')])]), ('commands', [OrderedDict([('assign', OrderedDict([('input_left', 'Grad_f_val'), ('input_right', OrderedDict([('add', [OrderedDict([('multiply', [OrderedDict([('value', 2), ('type', 'float')]), 'X_val'])]), OrderedDict([('value', 3), ('type', 'float')])])]))]))])])]))])
    outputs = yaml_block['outputs']
    return outputs
