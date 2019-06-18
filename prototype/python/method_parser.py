"""
Parse a YAML block for methods, detect whether it is element or function.
"""

from .shared_parameters import *

def read_name(yaml_block):
    keys = [key for key in yaml_block.keys()]
    block_name = keys[0]
    return block_name

def read_group(yaml_block):
    keys = [key for key in yaml_block.keys()]
    block_content = yaml_block[keys[0]]
    block_type = block_content['type']
    if block_type in function_group_types:
        group = group_function_id
    else:
        group = group_element_id
    return group

def get_inputs(yaml_block):
    # yaml_block == OrderedDict([('grad_f', OrderedDict([('type', 'function'), ('inputs', [OrderedDict([('name', 'X_val'), ('type', 'float')])]), ('outputs', [OrderedDict([('name', 'Grad_f_val'), ('type', 'float')])]), ('commands', [OrderedDict([('assign', OrderedDict([('input_left', 'Grad_f_val'), ('input_right', OrderedDict([('add', [OrderedDict([('multiply', [OrderedDict([('value', 2), ('type', 'float')]), 'X_val'])]), OrderedDict([('value', 3), ('type', 'float')])])]))]))])])]))])
    keys = [key for key in yaml_block.keys()]
    block_content = yaml_block[keys[0]]
    inputs = block_content['inputs']
    return inputs

def get_outputs(yaml_block):
    # yaml_block == OrderedDict([('grad_f', OrderedDict([('type', 'function'), ('inputs', [OrderedDict([('name', 'X_val'), ('type', 'float')])]), ('outputs', [OrderedDict([('name', 'Grad_f_val'), ('type', 'float')])]), ('commands', [OrderedDict([('assign', OrderedDict([('input_left', 'Grad_f_val'), ('input_right', OrderedDict([('add', [OrderedDict([('multiply', [OrderedDict([('value', 2), ('type', 'float')]), 'X_val'])]), OrderedDict([('value', 3), ('type', 'float')])])]))]))])])]))])
    keys = [key for key in yaml_block.keys()]
    block_content = yaml_block[keys[0]]
    outputs = block_content['outputs']
    return outputs
