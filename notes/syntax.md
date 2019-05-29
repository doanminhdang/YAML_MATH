# formats:

These are YAML files, each corresponds to a type of methods.

Structure:
```
- key_name:
  category:
  form:
  length:
```
In which, for each key:

- category: either "required" or "additional"

- form: either "list" or "map"

- length: either be compared with an integer using 1-char comparison (>=, <= are not acceptable), e.g. >1, =2..., or "free" means that there is no restriction on the number.

# methods:

These are YAML files, each corresponds to a method.

These keys are required:

- type: (so the syntax of the method will be checked with this type format)

- required keys that are in the type format

Keys are optional:

- keys that are allowed, with category "additional", in the type format

- versions: used for the purpose of overloading. It will be followed by a list of possible specific versions, ranked in the most-to-least priority order.

Example: in add.yml for the method `add`, it has versions pointing to specific methods `add__int` and `add__float`, they are respectively described in add__int.yml and add__float.yml.
```
- versions:
  - add__int
  - add__float
```
Then add__int is the most preferred because it is listed first, if the data given to the method is suitable with condition of that specific version. The checking of specific version should be done by "Syntax checker": overloading should be decidable by analyzing the syntax. And if there is no specific version suitable for the given data, it should be an error (no "catch-all version").

In the YAML file of each method, each of the required or additional keys can have the sub_keys:

- name: so that the name pointing to that key will be used in the translators

- array_name: for the case it is an array, later the items in the given array will be called by the array name with suffix [0], [1]... (an integer in square brackets, starting with index 0). Example: `array_name: input_` will be accessed by the name `input_[0]`, `input_[1]`...

Each "name" or "array_name" include the following required keys:

- length: either be compared with an integer using 1-char comparison (>=, <= are not acceptable), e.g. >1, =2..., or "free" means that there is no restriction on the number.

- type: list all the allowed type, separated with comma. Example: int, float. If type is "free", then type will not be checked.

- type_qualifier: list type qualifiers like var, const. If type_qualifier is "free", then type qualifier will not be checked.

TODO: consider dropping the requirement for those keys, no key is equivalent to key: free. Then only listed keys are to be checked.

# descriptors:

For each method, there must be a descriptor that describes how the method should be translated into the desired programming language; except with overloading methods, for such case only descriptors for the specific methods are required.

Example: with method add.yml there are two versions add__int.yml and add__float.yml, in order to translate the project into C, there must be add__int.c and add__float.c.

In each descriptor, there could be three sections: `!preprocess`, `!template`, `!postprocess`, each block of commands is put inside `{|` and `|}`, each of these opening and closing block markers must take a whole line.

`!preprocess` and `!postprocess` are optional, if they exist, the commands in `!preprocess` written in Python will be evaluated first, then processing the text in `!template` as a string, then `!postprocess` written in Python. If the keyword `!template` does not exists, the default template text is anything between the end of `!preprocess` and the beginning of `!postprocess` blocks. If none of these three keywords exists, then everything is considered `!template` code.

 Example: in add__float.c, we want to construct a loop to create the series of pluses: `<output> := <input_[0]> + ... + <input_[end]>`, we use Python commands in the !preprocess block:

```
!preprocess:
{|
command_text = "<input_[0]>"
for k in range(1, len(input_)):
  command_text += " + <input_[" + str(k) + "]>"
|}

!template:
{|
<output> := <command_text>
|}

!postprocess:
{|
<action>
|}

```

The code in `!preprocess` and `!postprocess` are written in Python 3. The content inside `!template` will be treated as text, where each block `<var_name>` (put a variable name inside brackets `<>`) will be detected and compared to all names that appear in: the YAML file that describes the method (name of items in inputs, outputs), the `!preprocess` section in the same descriptor. For example, if `!preprocess` produce the variable `command_text` with value `'input_[0] + input_[1] + input_[2]'`, then the placeholder `<command_text>` in `!template` will be evaluated by the default translator (written in Python) with commands like
```
var_name = 'command_text'
eval(var_name)
```
and the result of translating the section `!template` is: `'<output> = <input_[0]> + <input_[1]> + <input_[2]>'`. This string will be accessed by the Python code in the section `!postprocess` with the name `<template>`. At the end of `!postprocess`, there must be a string with the name `template`, that would be used by the translator. The translator will replace placeholders of the naming `<var_name>` in `template` to the corresponding variables in the YAML file describing the method.
