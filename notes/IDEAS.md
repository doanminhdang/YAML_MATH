# Aim

A program flow chart is expressed by YAML syntax (YAML_MATH language). Such program could be generated into a "target language" which would be compiled/interpreted in the manner of the target language.

The generator has two parts: first part is to parse the YAML program into the convention, second part is to use mappings between YAML_MATH language and the target language to generate the target program.

# Components

Each type, function, object... is described in a YAML block.

A YAML file can contain any number of YAML blocks.

A project is contained in a folder (directory), with the file main.yaml expressing the main program (program handle).

There is a structure definition for each type of YAML block. Ex: "function" has inputs, outputs, "type" has equivalences in target programming languages (C, C++...).

External functions could be specified, each is wrapped in a YAML block. That YAML block also contains information on where to find the external function, e.g. system, or header file in C/C++.

Some sketches on types of YAML blocks:

- Operator: add, subtract, multiply, divide...

- Type: u_int, int8_t, float, double... Data structures could also be in this group.

- Function: considered as a system with inputs and outputs

# Possible bottlenecks

- Manage memory

- Treating "pointers"

- Function overloading, with scalar and array/matrix

# Examples

A program could look like:

(find minimum of x^2 + 3*x + 5)

```
main:
  type: function
  inputs:
    -
  outputs:
    -
  const:
    - name: Daisy
      type: float
      init: 3
    - name: Paul
      type: float
      init: 5
    - name: Gamma
      type: float
      init: 1
  var:
    - name: X_mickey
      type: float
      init: 0
    - name: F_opt
      type: float
      init: 0
  commands:
    assign:
      input_left: X_mickey
      input_right: grad_descent(grad_f, X_mickey)
    assign:
      input_left: F_opt
      input_right: f_objective(Daisy, Paul, X_mickey)

f_objective:
  type: function
  inputs:
    - name: A_1
      type: float
    - name: A_2
      type: float
    - name: X_val
      type: float
  outputs:
    - name: F_val
      type: float
  commands:
  - assign:
      input_left: F_val
      input_right:
        add:
        - exp:
            input_1: X_val # base
            input_2: # power
              value: 2
              type: int
        - multiply:
          - A_1
          - X_val
          - A_2

grad_f:
  type: function
  inputs:
    - name: X_val
      type: float
  outputs:
    - name: Grad_f_val
      type: float
  commands:
    - assign:
        input_left: Grad_f_val
        input_right:
          add:
            - multiply:
              - value: 2
                type: float
              - X_val
            - value: 3
              type: float

grad_descent:
  type: function
  inputs:
    - name: grad_cat
      type: function
    - name: X_init
      type: float
  outputs:
    - name: Dog
      type: float
  var:
    - name: X_current
      type: float
      init: X_init
    - name: X_next
      type: float
      init: 0
  const:
    - name: Tol
      type: float
      init: 0.000001
  commands:
    - assign:
        input_left: X_next
        input_right:
          subtract:
            input_1: X_current
            input_2:
              multiply:
                - Gamma
                - grad_cat(X_current)
    - while:
        stop:
          - less_than:
              input_left:
                abs:
                  subtract:
                    input_1: X_next
                    input_2: X_current
              input_right: Tol
        commands:
          - assign:
              input_left: X_next
              input_right:
                subtract:
                  input_1: X_current
                  input_2:
                    multiply:
                      - Gamma
                      - grad_cat(X_current)
    - assign:
        input_left: Dog
        input_right: X_next

lp_solver:
  type: ext_function
  inputs:
  outputs:
  where:

qp_solver:
  type: ext_function
  inputs:
  outputs:
  where:

nlp_solver:
  type: ext_function
  inputs:
  outputs:
  where:
```
