print('Run outside a function:')

code = 'aaa'
print('code = ' + code)
comment_code = 'bbb'
command_1 = 'new_code = comment_code + code'
command_2 = 'code = comment_code + code'
exec(command_1)
exec(command_2)
print('Result command 1: new_code = ' + new_code)
print('Result command 2: code = ' + new_code)

print('Run within a function:')

def embed_exec_in_function():
    code = 'aaa'
    print('code = ' + code)
    comment_code = 'bbb'
    command_1 = 'new_code = comment_code + code'
    command_2 = 'code = comment_code + code'
    exec(command_1)
    exec(command_2)
    print('Result command 1: new_code = ' + new_code)
    print('Result command 2: code = ' + new_code)

embed_exec_in_function()
