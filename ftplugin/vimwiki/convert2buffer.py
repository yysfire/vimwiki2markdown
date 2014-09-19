from vimwiki2markdown import *

def create_new_buffer(file_name, file_type, contents):
    vim.command('rightbelow vsplit {0}'.format(file_name))
    #vim.command('normal! ggdG')
    vim.command('setlocal filetype={0}'.format(file_type))
    vim.command('setlocal fileencoding=utf-8')
    vim.command('setlocal buftype=nowrite')
    #vim.command('call append(0, {0})'.format(contents))
    vim.current.buffer[:] = contents

def get_visual_selection():
    buf = vim.current.buffer
    (starting_line_num, col1) = buf.mark('<')
    (ending_line_num, col2) = buf.mark('>')
    lines = vim.eval('getline({}, {})'.format(starting_line_num, ending_line_num))
    lines[0] = lines[0][col1:]
    lines[-1] = lines[-1][:col2]
    return lines

def get_correct_buffer(buffer_type):
    if buffer_type == "buffer":
        return vim.current.buffer
    elif buffer_type == "selection":
        return get_visual_selection()

buf = '\n'.join(get_correct_buffer(vim.eval("a:selection_or_buffer")))
mkd_type = vim.eval("g:vimwiki2markdown_markdown_type")
mkd_contents = vimwiki2markdown(buf, mkd_type)
if mkd_contents:
    create_new_buffer("markdown_equivalent", "mkd", mkd_contents.split('\n'))
