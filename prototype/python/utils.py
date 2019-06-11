import oyaml as yaml

def yaml_file_read(yaml_file):
    with open(yaml_file, 'r') as yf:
        yaml_series = yaml.load(yf, Loader=yaml.FullLoader)
    return yaml_series

def odict_to_json(odict):
    """
    Dump an OrderedDict into JSON series
    """
    import json
    json_series = json.dumps(odict)
    return json_series

def json_to_odict(json_series):
    """
    Load a JSON series into OrderedDict
    """
    import json
    from collections import OrderedDict
    odict = json.loads(js, object_pairs_hook=OrderedDict)
    return odict

def json_to_ast(json_series):
    """
    Load a JSON series into AST - abstract syntax tree
    """
    # TODO
