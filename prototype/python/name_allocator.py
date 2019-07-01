"""
Analyze the whole sequence of program - the OrderedDict that was parsed from
YAML files. Then assign names to inputs and outputs of each method.
The result will be passed to the translator for each method-call.

Names will be drawn from name banks, each target language has its own name bank.
"""

def read_name_bank():
    """Specify name bank (as a text file)"""
    return name_list

def read_used_names():
    """Specify list of names used in the project (as a text file)"""
    return used_name_list

def draw_new_name(name_list, used_name_list):
    """Pick a name in name_list that doesn't belong to used_name_list"""
    return new_name

def update_used_names(new_name):
    used_name_list.append(new_name)

def find_a_name():
    name_list = read_name_bank()
    used_name_list = read_used_names()
    new_name = draw_new_name(name_list, used_name_list)
    update_used_names(new_name)
    return new_name
