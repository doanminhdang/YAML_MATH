# import pdb
import sys
import oyaml as yaml

result_pass = 1
result_failed = 0
result_unknown = -1
result_missing = -2
result_notype = -3

def yaml_file_check_against_folder(yaml_file, yaml_template_folder):
    templates = yaml_template_folder_read(yaml_template_folder)
    print(templates)
    result = yaml_file_check(yaml_file, templates)
    return result

def yaml_template_folder_read(yaml_template_folder):
    import glob, os
    list_yaml_template_files = glob.glob(yaml_template_folder + '/*.yml', recursive=True)
    templates = dict()
    for yaml_template_file in list_yaml_template_files:
        filename_only = os.path.basename(yaml_template_file)
        main_name, ext_name = os.path.splitext(filename_only)
        templates.update({main_name: yaml_template_file_read(yaml_template_file)})
    return templates

def yaml_template_file_read(yaml_template_file):
    with open(yaml_template_file, 'r') as yf:
        yaml_series = yaml.load(yf)
    return yaml_series

def yaml_file_check(yaml_file, templates):
    with open(yaml_file, 'r') as yf:
        yaml_series = yaml.load(yf)
    list_block_names = [key for key in yaml_series.keys()] # convert odict_keys to list
    result = []
    for block_name in list_block_names:
        yaml_block = yaml_series[block_name]
        result_block = yaml_block_check(yaml_block, templates)
        result.append({block_name: result_block})
    return result

def yaml_block_check(yaml_block, templates):
    if 'type' not in yaml_block:
        result = result_notype
    else:
        block_type = yaml_block['type']
        print('Type to check: ', block_type)
        type_template = templates[block_type]
        result = yaml_block_type_check(yaml_block, type_template)
    return result
# required:
#   - inputs:
#       form: list
#       length: max

def yaml_block_type_check(yaml_block, type_template):
    result_required = check_condition_group(yaml_block, type_template, 'required')
    result_additional = check_condition_group(yaml_block, type_template, 'additional')
    result = {'required': result_required, 'additional': result_additional}
    return result

def check_condition_group(yaml_block, type_template, group_type):
    # group_type: 'required' or 'additional'
    print('yaml_block: ', yaml_block)
    print('type_template: ', type_template)
    print('group_type: ', group_type)
    result_required = []
    for condition in type_template[group_type]: # condition = OrderedDict([('inputs', ...
        condition_keys = [key for key in condition.keys()] # ['inputs']
        for key in condition_keys: # key = 'input'
            print('key: ', key)
            # print('yaml_block:', yaml_block)
            # print('yaml_block_key', yaml_block[key])
            # if yaml_block[key] is missing: report missing
            if key not in yaml_block:
                result_key = result_missing
            else:
                result_key = check_condition_key(yaml_block[key], condition[key])
            result_required.append({key: result_key})
    return result_required

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
    yaml_template_folder = str(sys.argv[2])
    print("Check syntax of a YAML file against templates in a folder")
    result = yaml_file_check_against_folder(yaml_command_file, yaml_template_folder)
    print(result)
