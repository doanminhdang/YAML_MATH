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

convention_code_assign = 'code='
descriptor_part_opening = '{|'
descriptor_part_closing = '|}'
descriptor_preprocess_label = '!preprocess:'
descriptor_midprocess_label = '!code:'
descriptor_postprocess_label = '!postprocess:'

def descriptor_file_read(descriptor_file):
    with open(descriptor_file, 'r') as text_file:
        descriptor_text = text_file.read()
    descriptor_components = {'preprocess': '', 'code': '', 'postprocess': ''}
    check_ok, check_err_msg = check_descriptor_syntax(descriptor_text)
    if check_ok:
        descriptor_components = descriptor_parse(descriptor_text)
    return descriptor_components

def check_descriptor_syntax_file(descriptor_file):
    with open(descriptor_file, 'r') as text_file:
        descriptor_text = text_file.read()
    check_ok, check_err_msg = check_descriptor_syntax(descriptor_text)
    return check_ok, check_err_msg

def check_descriptor_syntax(descriptor_text):
    """
    Check syntax of a descriptor text:
    - If preprocess part exist: it must have an opening then a closing markup
    - If postprocess part exist: it must have an opening then a closing markup
    - the preprocess part must be before the postprocess part
    - in the postprocess part, there must be a variable named `code` to be assigned at the last line
    Output: check_flag, error_message
    - check_flag: True is good, False is bad
    - error_message: id of error, specifed in the module. 0 for no error.
    """
    lines = descriptor_text.split('\n')
    check_flag = True
    error_message = 0
    if descriptor_preprocess_label in lines:
        if not descriptor_part_opening in lines:
            check_flag = False
            error_message = err_msg_no_opening_preprocess
        else:
            if not descriptor_part_closing in lines:
                check_flag = False
                error_message = err_msg_no_closing_preprocess
            else:
                if not lines.index(descriptor_part_opening) < \
                    lines.index(descriptor_part_closing):
                    check_flag = False
                    error_message = err_msg_incomplete_block_preprocess
                else:
                    preprocess_closing = lines.index(descriptor_part_closing)
                    lines = lines[preprocess_closing+1:]

    if descriptor_midprocess_label in lines:
        if not descriptor_part_opening in lines:
            check_flag = False
            error_message = err_msg_no_opening_midprocess
        else:
            if not descriptor_part_closing in lines:
                check_flag = False
                error_message = err_msg_no_closing_midprocess
            else:
                if not lines.index(descriptor_part_opening) < \
                    lines.index(descriptor_part_closing):
                    check_flag = False
                    error_message = err_msg_incomplete_block_midprocess
                else:
                    midprocess_closing = lines.index(descriptor_part_closing)
                    lines = lines[midprocess_closing+1:]

    if descriptor_postprocess_label in lines:
        if not descriptor_part_opening in lines:
            check_flag = False
            error_message = err_msg_no_opening_postprocess
        else:
            if not descriptor_part_closing in lines:
                check_flag = False
                error_message = err_msg_no_closing_postprocess
            else:
                if not lines.index(descriptor_part_opening) < \
                    lines.index(descriptor_part_closing):
                    check_flag = False
                    error_message = err_msg_incomplete_block_postprocess
                else:
                    postprocess_closing = lines.index(descriptor_part_closing)
                    if lines[postprocess_closing-1].replace(' ', '')\
                        .find(convention_code_assign)<0:
                        check_flag = False
                        error_message = err_msg_no_code_output
                    if descriptor_preprocess_label in lines:
                        # preprocess should not be after postprocess
                        check_flag = False
                        error_message = err_msg_wrong_order_pre_post_process
    return check_flag, error_message

def descriptor_parse(descriptor_text):
    lines = descriptor_text.split('\n')
    if descriptor_preprocess_label in lines:
        preprocess_line = lines.index(descriptor_preprocess_label)
        # any text before preprocess label is discarded
        lines = lines[preprocess_line:]
        preprocess_opening = lines.index(descriptor_part_opening)
        preprocess_closing = lines.index(descriptor_part_closing)
        preprocess = lines[preprocess_opening+1:preprocess_closing]
        # remove any text up to the closing of preprocess
        lines = lines[preprocess_closing+1:]
    else:
        preprocess = ''
    if descriptor_postprocess_label in lines:
        postprocess_line = lines.index(descriptor_postprocess_label)
        # split text from postprocess label, the remaining is for midprocess
        postprocess_part = lines[postprocess_line:]
        lines = lines[:postprocess_line]
        postprocess_opening = lines.index(descriptor_part_opening)
        postprocess_closing = lines.index(descriptor_part_closing)
        # discard any text after the closing of postprocess
        postprocess = postprocess_part[postprocess_opening+1:postprocess_closing]
    else:
        postprocess = ''
    # remaining of lines is for code (default)
    code = lines
    preprocess = '\n'.join(preprocess)
    code = '\n'.join(code)
    postprocess = '\n'.join(postprocess)

    descriptor_components = {'preprocess': preprocess, 'code': code, 'postprocess': postprocess}
    return descriptor_components
