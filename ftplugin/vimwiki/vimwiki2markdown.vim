if !has('python') && !has('python3')
  echo "Error: Required vim compiled with +python or +python3"
  finish
endif

" --------------------------------
" Add our plugin to the path
" --------------------------------
if has('python3')
  python3 import sys
  python3 import vim
  python3 sys.path.append(vim.eval('expand("<sfile>:h")'))
else
  python import sys
  python import vim
  python sys.path.append(vim.eval('expand("<sfile>:h")'))
endif

if !exists('g:vimwiki2markdown_markdown_type')
  let g:vimwiki2markdown_markdown_type = 'pelican'
endif

if !exists('s:pluginPath')
  let s:pluginPath= escape(expand('<sfile>:p:h'), ' ')
endif

" --------------------------------
"  Function(s)
" --------------------------------
function! Convert2Buffer(selection_or_buffer)
  if has('python3')
    exec "py3file " . expand(s:pluginPath . "/convert2buffer.py")
  else
    exec "pyfile " . expand(s:pluginPath . "/convert2buffer.py")
endif

endfunction

function! Convert2File()
  if has('python3')
    exec "py3file " . expand(s:pluginPath . "/convert2file.py")
  else
    exec "pyfile " . expand(s:pluginPath . "/convert2file.py")
endif

endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! VimwikiBuf2MkdBuf call Convert2Buffer("buffer")
command! -range VimwikiSel2MkdBuf call Convert2Buffer("selection")
command! VimwikiBuf2MkdFile call Convert2File()
