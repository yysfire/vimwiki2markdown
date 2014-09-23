" Init
"if exists('g:did_vimwiki2markdown_loaded')
  "finish
"endif

if v:version < '703'
  echohl WarningMsg|echomsg "vimwiki2markdown unavailable: requires Vim 7.3+"|echohl None
  "let g:did_vimwiki2markdown_loaded = 0
  finish
endif

if !has('python') && !has('python3')
  echohl WarningMsg|echomsg "vimwiki2markdown unavailable: requires Vim to be compiled with Python 2.6+"|echohl None
  "let g:did_vimwiki2markdown_loaded = 0
  finish
endif

"let g:did_vimwiki2markdown_loaded = 1

if !exists('g:vimwiki2markdown_markdown_type')
  let g:vimwiki2markdown_markdown_type = 'pelican'
endif

if !exists('s:pluginPath')
  let s:pluginPath= escape(expand('<sfile>:p:h'), ' ')
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

" --------------------------------
"  Function(s)
" --------------------------------
function! s:Convert2Buffer(selection_or_buffer)
  if has('python3')
    exec "py3file " . expand(s:pluginPath . "/convert2buffer.py")
  else
    exec "pyfile " . expand(s:pluginPath . "/convert2buffer.py")
endif

endfunction

function! s:Convert2File()
  if has('python3')
    exec "py3file " . expand(s:pluginPath . "/convert2file.py")
  else
    exec "pyfile " . expand(s:pluginPath . "/convert2file.py")
endif

endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
if !exists(":VimwikiBuf2MkdBuf")
  command -buffer -nargs=0 VimwikiBuf2MkdBuf call s:Convert2Buffer("buffer")
endif
if !exists(":VimwikiSel2MkdBuf")
  command -buffer -nargs=0 -range VimwikiSel2MkdBuf call s:Convert2Buffer("selection")
endif
if !exists(":VimwikiBuf2MkdFile")
  command -buffer -nargs=? -complete=file VimwikiBuf2MkdFile call s:Convert2File(<f-args>)
endif
