"""
Check syntax of a module described in a YAML file
"""
# import pdb
import sys
import oyaml as yaml

from shared_parameters import *

def yaml_module_file_check_against_folder(yaml_file, yaml_format_folder):
    formats = yaml_format_folder_read(yaml_format_folder)
    print(formats)
    result = yaml_module_file_check(yaml_file, formats)
    return result

def yaml_format_folder_read(yaml_format_folder):
    import glob, os
    list_yaml_format_files = glob.glob(yaml_format_folder + '/*.yml', recursive=True)
    formats = dict()
    for yaml_format_file in list_yaml_format_files:
        filename_only = os.path.basename(yaml_format_file)
        main_name, ext_name = os.path.splitext(filename_only)
        formats.update({main_name: yaml_format_file_read(yaml_format_file)})
    return formats

def yaml_format_file_read(yaml_format_file):
    with open(yaml_format_file, 'r') as yf:
        yaml_series = yaml.load(yf, Loader=yaml.FullLoader)
    return yaml_series

def yaml_module_file_check(yaml_file, formats):
    with open(yaml_file, 'r') as yf:
        yaml_series = yaml.load(yf, Loader=yaml.FullLoader)
    print('YAML series from file: ', yaml_series)
    list_block_names = [key for key in yaml_series.keys()] # convert odict_keys to list
    result = []
    for block_name in list_block_names:
        yaml_block = yaml_series[block_name]
        print('block_name: ', block_name)
        result_block = yaml_block_check(yaml_block, formats)
        result.append({block_name: result_block})
    return result

def yaml_block_check(yaml_block, formats):
    if 'type' not in yaml_block:
        result = result_notype
    else:
        block_type = yaml_block['type']
        print('Type to check: ', block_type)
        type_format = formats[block_type]
        result = yaml_block_type_check(yaml_block, type_format)
    return result

def yaml_block_type_check(yaml_block, type_format):
    result_required = check_condition_required(yaml_block, type_format)
    result_allowed = check_condition_allowed(yaml_block, type_format)
    result = {'required': result_required, 'required_additional': result_allowed}
    return result

def check_condition_required(yaml_block, type_format):
    # group_type: 'required' or 'additional'

    result_required = []
    for condition in type_format: # condition = OrderedDict([('inputs', ...
        condition_keys = [key for key in condition.keys()] # ['inputs']
        for key in condition_keys: # key = 'input'
            print('key: ', key)
            # print('yaml_block:', yaml_block)
            # print('yaml_block_key', yaml_block[key])
            # if yaml_block[key] is missing: report missing

            if condition[key]['category'] == 'required':
                if key not in yaml_block:
                    result_key = result_missing
                else:
                    result_key = check_condition_key(yaml_block[key], condition[key])
                result_required.append({key: result_key})
    return result_required

def check_condition_allowed(yaml_block, type_format):
    # group_type: 'required' or 'additional'

    result_allowed = []
    # build list of allowed keys
    # type_format is a list: [OrderedDict([('inputs', ...)]), OrderedDict([('outputs', ... ]
    # all_allowed_keys = [[b for b in a.keys()] for a in type_format] #[['inputs'], ['outputs'], ... ]
    all_allowed_keys = [[b for b in a.keys()][0] for a in type_format] #['inputs', 'outputs', ... ]

    for appeared_key in yaml_block:
        if appeared_key != 'type':
            if appeared_key not in all_allowed_keys:
                result_key = result_excess
            else:
                position_key = all_allowed_keys.index(appeared_key)
                result_key = check_condition_key(yaml_block[appeared_key], type_format[position_key][appeared_key])
            result_allowed.append({appeared_key: result_key})
    return result_allowed

def check_condition_key(yaml_block_key, condition_key):
    # If it is a list, then check the length of items
    if condition_key['form'] == 'list':
        length_cond = condition_key['length'] # str
        if not isinstance(yaml_block_key, list):
        # if inputs = None, then cannot take len()
            length_block = 0
        else:
            length_block = len(yaml_block_key) # int
        result = check_length(length_block, length_cond)
    # If it is a mapping, then check the list of keys
    if condition_key['form'] == 'map':
        keys_cond = condition_key['keys'] # it could be an OrderedDict, or already a list
        if isinstance(keys_cond, list):
            allowed_keys = keys_cond
        else:
            allowed_keys = [sub_key for sub_key in keys_cond.keys()] # convert keys of OrderedDict to list
        list_block_keys = [sub_key for sub_key in yaml_block_key.keys()]
        print('list_block_keys: ', list_block_keys)
        result = check_key(list_block_keys, allowed_keys)
    return result

def check_length(length_block, length_cond):
    # length_cond is a str, it could be '=1', '<2', '>2', ... or 'max'

    result = result_unknown # in case none of conditions below matched
    if length_cond == 'free':
        result = result_pass
    if length_cond[0] == '<':
        if length_block < int(length_cond[1:]):
            result = result_pass
        else:
            result = result_failed
    if length_cond[0] == '=':
        if length_block == int(length_cond[1:]):
            result = result_pass
        else:
            result = result_failed
    if length_cond[0] == '>':
        if length_block > int(length_cond[1:]):
            result = result_pass
        else:
            result = result_failed
    return result

def check_key(list_block_keys, allowed_keys):

    result = [result_unknown] * len(list_block_keys) # redundant
    for k in range(len(list_block_keys)):
        if list_block_keys[k] in allowed_keys:
            result[k] = result_pass
        else:
            result_key = result_failed
    return result

if __name__ == '__main__':
    yaml_command_file = str(sys.argv[1])
    yaml_format_folder = str(sys.argv[2])
    print("Check syntax of a YAML file against formats in a folder")
    result = yaml_module_file_check_against_folder(yaml_command_file, yaml_format_folder)
    print(result)
