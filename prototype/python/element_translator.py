"""
Translate an element, which is described by the YAML method file
 and a descriptor file, into a target function.

Procedure:

1. When analyzing a YAML file, parse the call to the method-element, to get:
- list of inputs,
- list of outputs
2. Parse the YAML of that element, to know the name of the inputs and outputs,
create inputs and outputs with such names, value are translated-names (string,
given by the name-allocator before translating methods), they will be accessed
in the descriptor of that element.
3. Process the descriptor:
- If preprocess part is available: execute the preprocess part as Python 3 code.
- Treat the code part as text (a string), parse that text to detect:
anywhere there is the structure <var_name>, then replace it with the value
of that variable currently in Python memory (within scope of processing that
specific descriptor). The new text after processing the code part is named code.
- If postprocess part is available: execute the postprocess part as Python 3
code. By requirement, at the end of postprocess part, there will be a variables
named `code`. Write the value of `code` into the output string.
"""

from .descriptor_parser import *
from .utils import *
from .shared_parameters import *

# def descriptor_file_parse(descriptor_file, method_file):
#     descriptor = descriptor_file_read(descriptor_file)
#     yaml_method = yaml_method_file_read(method_file)
#     preprocess_parse(descriptor_file)

def yaml_single_method_file_read(yaml_method_file):
    """
    Read a method file which contains only one block
    """
    yaml_block = utils.yaml_file_read(yaml_method_file)
    # Analyze its commands
    return

def translate_command_element(odict_command, element_file, descriptor_file):
    descriptor = descriptor_parser.descriptor_file_read(descriptor_file)
    preprocess_string = descriptor['preprocess']
    code_string = descriptor['code']
    postprocess_string = descriptor['postprocess']
    yaml_element = utils.yaml_file_read(element_file)

    list_command_keys = [key for key in odict_command.keys()]
    first_key = list_block_keys[0]
    input_names = odict_command[first_key]

    list_element_keys = [key for key in yaml_element.keys()]
    element_name = list_element_keys[0]
    element_inputs = yaml_element[element_name]['inputs']
    if first_key != element_name:
        raise ValueError('Element does not match command.')
    else:
        real_inputs = analyze_inputs(input_names, element_inputs)
        translated_code = translate_single_code(real_inputs, preprocess_string,\
        code_string, postprocess_string)
    return translated_code

def analyze_inputs(input_names, element_inputs):
    """
    Get decoded names from the input_names (list) and the template
    element_inputs (odict).
    The output is a dict, with keys from element_inputs and values are picked
    with corresponding order from input_names.
    If element_inputs contains both 'name' and 'array_name', then array_name
    must be the last item. This function automatically assign the rest of the
    input names into an array, if 'array_name' is found in element_inputs.
    """
    real_inputs = {}
    index_input_names = 0
    for item in element_inputs:
        # item == OrderedDict([('array_name', 'input_'), ('length', ''), ('type', 'float')])
        if 'name' in item:
            real_inputs.update({item['name']: input_names[index_input_names]})
            index_input_names += 1
        elif 'array_name' in item:
            names_left = input_names[index_input_names:]
            array_length = len(names_left)
            for k in range(array_length):
                real_inputs.update({item['array_name'] + '[' + str(k) + ']': names_left[k]})
    return real_inputs

def translate_single_code(input_names, preprocess_string, code_string,\
    postprocess_string):
    exec(preprocess_string)
