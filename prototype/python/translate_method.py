"""
Translate a method, which is described by the method YAML file
 and a descriptor file, into a target function.

Procedure:

1. When analyzing a YAML file, parse the call to the method, to get:
- list of inputs,
- list of outputs
2. Parse the YAML of that method, to know the name of the inputs and outputs,
create inputs and outputs with such names, value are translated-names (string,
given by the name-allocator before translating methods), they will be accessed
in the descriptor of that method.
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
