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

- [X] Convert Vimwiki file to [Strict Markdown](http://daringfireball.net/projects/markdown/syntax) file
- [X] Convert Vimwiki file to Markdown file for [Pelican](http://docs.getpelican.com/)
- [X] Add command to convert all Vimwiki files to Markdown
- [ ] Write documentation
- [X] Support Github Flavored Markdown
- [ ] Support PHP Markdown Extra
- [ ] Support MultiMarkdown
- [ ] Support converting Markdown to Vimwiki
