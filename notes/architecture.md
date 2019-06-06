# Components

## Data

`format` templates: each type has one file for for object syntax requirement.

`type` definitions: YAML files that define types.

`type` translations: YAML files that define mapping from YAML_MATH types to different target languages.

`element` definitions: YAML files that define elements, e.g. operators, external functions. Each element has a simple way to be translated to target languages, through descriptors.

`descriptor` translations: each one defines mapping (in text) from a YAML_MATH element to a target language.

`function` definitions: YAML files that express the functions.

Functions will be translated to target languages by: parsing to understand the function sequence, and substituting the correct translations of elements inside the sequence.

## Engines

YAML parser: (based on oyaml) parse all YAML files, output YAML blocks, each block is either a function or an external function.

Syntax checker: check syntax in each YAML block.

Element translator: translate each element into the target language.

Function translator: translate each YAML function block into the target language.

Project translator: combine functions and create a project setting in the target language (e.g. Makefile in C).
