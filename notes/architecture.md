# Components

## Data

Object syntax requirement: each type has one file for requirement

Type definitions: YAML files that define types

Type translations: YAML files that define mapping from YAML_MATH types to different target languages

Operator definitions: YAML files that define operators

Operator translations: YAML files that define mapping from YAML_MATH operators to different target languages

Function definitions: YAML files that express the functions


## Engines

YAML parser: (based on oyaml) parse all YAML files, output YAML blocks, each block is either a function or an external function

Syntax checker: check syntax in each YAML block

Function translator: translate each YAML function block into the target language

Project translator: combine functions and create a project setting in the target language (e.g. Makefile in C)
