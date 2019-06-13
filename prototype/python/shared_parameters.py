"""
Centralized file to store constants, parameters
"""

# For method parser
function_group_types = {'function'}
group_element_id = 0
group_function_id = 1

# For descriptor parser
err_msg_no_opening_preprocess = 1
err_msg_no_closing_preprocess = 2
err_msg_no_opening_midprocess = 3
err_msg_no_closing_midprocess = 4
err_msg_no_opening_postprocess = 5
err_msg_no_closing_postprocess = 6
err_msg_incomplete_block_preprocess = 7
err_msg_incomplete_block_midprocess = 8
err_msg_incomplete_block_postprocess = 9
err_msg_wrong_order_pre_post_process = 10
err_msg_no_code_output = 11

output_code_descriptor = 'final_code' # note: a variable name, cannot be 'code'
convention_code_assign = output_code_descriptor + '='
descriptor_part_opening = '{|'
descriptor_part_closing = '|}'
descriptor_preprocess_label = '!preprocess:'
descriptor_midprocess_label = '!code:'
descriptor_postprocess_label = '!postprocess:'

# For yaml module checker
result_pass = 1
result_failed = 0
result_unknown = -1
result_missing = -2
result_excess = -3
result_notype = -4
