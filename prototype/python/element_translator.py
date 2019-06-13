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
import re
from . import descriptor_parser
from . import utils
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
    output_name = utils.get_var_name_from_bank(1)

    list_element_keys = [key for key in yaml_element.keys()]
    element_name = list_element_keys[0]
    element_inputs = yaml_element[element_name]['inputs']
    element_output = yaml_element[element_name]['outputs']
    if first_key != element_name:
        raise ValueError('Element does not match command.')
    else:
        real_inputs = analyze_inputs(input_names, element_inputs)
        real_output = analyze_outputs(output_name, element_output)
        translated_code = translate_single_code(real_inputs, real_output,\
        preprocess_string, code_string, postprocess_string)
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
            real_inputs.update({item['array_name']: names_left})
            # for k in range(array_length):
                # real_inputs.update({item['array_name'] + '[' + str(k) + ']': names_left[k]})
    return real_inputs

def analyze_outputs(output_name, element_output):
    output_var = element_output[0]['name']
    output_dict = {output_var: output_name[0]}
    return output_dict

def parse_code(code_string):
    """
    Parse the multi-line string which contains the code, pick variable in <>.
    Output: list of segments, each is a dict with key `text` or `var`,
    and value is the text or the variable name.
    """
    code = []
    var_pattern = r'\<[\w\[\]]+\>'
    rolling_code = code_string
    while re.search(var_pattern, rolling_code):
        start_index = re.search(var_pattern, rolling_code).start()
        var_group = re.search(var_pattern, rolling_code).group()
        var_name = var_group.strip('<>')
        if start_index > 0:
            text_before = rolling_code[0:start_index]
            code.append({'text': text_before})
        code.append({'var': var_name})
        rolling_code = rolling_code[start_index+len(var_group):]
    return code


def translate_single_code(input_dict, output_dict, preprocess_string,\
    code_string, postprocess_string):
    """
    input_dict == {'input_': ['A_1', 'A_2', 'A_3']}
    output_dict == {'output': 'Alpha'}
    parsed_code == [{'var': 'output'}, {'text': ' := '}, {'var': 'command_text'}]
    """
    _code_series = parse_code(code_string)
    print(_code_series)
    for _key in input_dict:
        if isinstance(input_dict[_key], list):
            # it is an array
            _assign_code = _key + '=' + '['
            for _item in input_dict[_key]:
                _assign_code += '\'' + _item + '\','
            _assign_code = _assign_code[:-1]+']' # remove the last comma
        else:
            _assign_code = _key + '=' + '\'' + input_dict[_key] + '\''
        exec(_assign_code)
    for _key in output_dict:
        _assign_code = _key + '=' + '\'' + output_dict[_key] + '\''
        exec(_assign_code)

    exec(preprocess_string)

    # 1st round: substitute variable names in code string
    _1st_processed_code = ''
    for _chunk in _code_series:
        if 'text' in _chunk:
            _1st_processed_code += _chunk['text']
        if 'var' in _chunk:
            _1st_processed_code += eval(_chunk['var'])

    #2nd round: replace variable names left, which might come from preprocess,
    # like: input_[0]
    _parsed_2nd_code = parse_code(_1st_processed_code)
    code = ''
    for _chunk in _parsed_2nd_code:
        if 'text' in _chunk:
            code += _chunk['text']
        if 'var' in _chunk:
            code += eval(_chunk['var'])

    print(code)
    exec(postprocess_string)
    print('after postprocess:')
    final_processed_code = code
    print(final_processed_code)
    # Note that at the end of postprocess, `code` could already be changed

    return final_processed_code
