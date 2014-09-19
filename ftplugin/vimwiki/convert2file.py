from vimwiki2markdown import *
from os import path
import io

buf = vim.current.buffer
mkd_file_path = os.path.splitext(buf.name)[0] + '.md'
buf_fenc = buf.options["fileencoding"]
buf = '\n'.join(buf)
if not isinstance(buf,unicode):
    buf = buf.decode(buf_fenc)
mkd_type = vim.eval("g:vimwiki2markdown_markdown_type")
mkd_contents = vimwiki2markdown(buf, mkd_type)
if mkd_contents:
    with io.open(mkd_file_path, 'wt', encoding='utf-8') as mkdf:
        mkdf.write(mkd_contents)
