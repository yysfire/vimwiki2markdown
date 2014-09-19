# vimwiki2markdown

This is a Vim plugin for converting [Vimwiki](http://www.vim.org/scripts/script.php?script_id=2226) file to Markdown file. It's written with Python, so your Vim must be compiled with feature "+python" or "+python3".

## Installation

Use your plugin manager of choice.

- [Pathogen](https://github.com/tpope/vim-pathogen)
  - `git clone https://github.com/yysfire/vimwiki2markdown ~/.vim/bundle/vimwiki2markdown`
- [Vundle](https://github.com/gmarik/vundle)
  - Add `Bundle 'https://github.com/yysfire/vimwiki2markdown'` to .vimrc
  - Run `:BundleInstall`
- [NeoBundle](https://github.com/Shougo/neobundle.vim)
  - Add `NeoBundle 'https://github.com/yysfire/vimwiki2markdown'` to .vimrc
  - Run `:NeoBundleInstall`
- [vim-plug](https://github.com/junegunn/vim-plug)
  - Add `Plug 'https://github.com/yysfire/vimwiki2markdown'` to .vimrc
  - Run `:PlugInstall`

## Todo

1. Convert Vimwiki file to [Strict Markdown](http://daringfireball.net/projects/markdown/syntax) file
1. Convert Vimwiki file to Markdown file for [Pelican](http://docs.getpelican.com/)
1. Add command to convert all Vimwiki files to Markdown
1. Write documentation
1. Support Github Flavored Markdown
1. Support PHP Markdown Extra
1. Support MultiMarkdown
1. Support converting Markdown to Vimwiki
