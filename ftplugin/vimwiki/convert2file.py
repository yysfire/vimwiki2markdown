#!/usr/bin/env python
# encoding: utf-8

from vimwiki2markdown import *
import os
from os.path import *
import io
from shutil import copy

def processpath(filepath):
    (dirpath, basename_tmp) = split(filepath)
    filepath = join(dirpath, basename_tmp)
    (dirpath, basename) = split(abspath(filepath))

    if basename_tmp == '':
        return (1, dirpath, basename) # 1 表示目录
    else:
        return (0, dirpath, basename) # 0 表示文件

def main():
    args = vim.eval("a:000")
    mkd_output_dir = vim.eval('g:vimwiki2markdown_output_dir')
    if len(args) >= 2:
        mkd_file_path_arg = args[0]
        mkd_type = args[1]
    elif len(args) == 1:
        mkd_file_path_arg = args[0]
        mkd_type = vim.eval("g:vimwiki2markdown_markdown_type")
    else:
        mkd_file_path_arg = None
        mkd_type = vim.eval("g:vimwiki2markdown_markdown_type")

    if vim.eval("a:curbuf_or_allwiki") == "curbuf":
        buf = vim.current.buffer
        if buf.options["filetype"] != "vimwiki":
            return

        if mkd_file_path_arg == None or mkd_file_path_arg == '':
            mkd_file_path_arg = splitext(buf.name)[0] + '.md'
        else:
            (pathtype, dirpath, basename) = processpath(mkd_file_path_arg)
            if pathtype == 0:
                if not isdir(dirpath):
                    os.makedirs(dirpath)
                mkd_file_path_arg = join(dirpath, basename)
            else:
                dirpath = join(dirpath, basename)
                if not isdir(dirpath):
                    os.makedirs(dirpath)
                mkd_file_path_arg = join(dirpath, splitext(os.path.basename(buf.name))[0] + '.md')

        buf_encoding = 'utf-8'
        if buf.options["fileencoding"] == '':
            buf_encoding = vim.eval("&encoding")
        else:
            buf_encoding = buf.options["fileencoding"]
        buf = '\n'.join(buf)
        if not isinstance(buf,unicode):
            buf = buf.decode(buf_encoding)
        mkd_contents = vimwiki2markdown(buf, mkd_type)
        if mkd_contents:
            with io.open(mkd_file_path_arg, 'wt', encoding='utf-8') as mkdf:
                mkdf.write(mkd_contents)

    elif vim.eval("a:curbuf_or_allwiki") == "allwiki":
        if mkd_file_path_arg != None and mkd_file_path_arg != '':
            (pathtype, dirpath, basename) = processpath(mkd_file_path_arg)
            if pathtype == 0:
                vim.command("echohl  WarningMsg|echomsg 'Conversion stoped: the given output path is a file not a directory'|echohl None")
                return
            else:
                dirpath = join(dirpath, basename)
                if not isdir(dirpath):
                    os.makedirs(dirpath)
                mkd_output_dir = dirpath

        wiki_root_path = vim.eval("expand(VimwikiGet('path'))") # 末尾带有路径分隔符
        # 去掉末尾的路径分隔符
        wiki_root_path = dirname(wiki_root_path)
        wiki_ext = vim.eval("VimwikiGet('ext')")
        for root, dirs, files in os.walk(wiki_root_path):
            if mkd_output_dir != '':
                for d in dirs:
                    mkdf_dir = join(root, d).replace(wiki_root_path, mkd_output_dir)
                    if not isdir(mkdf_dir):
                        os.makedirs(mkdf_dir)

                for f in files:
                    (filename, fileext) = splitext(f)
                    if fileext == wiki_ext:
                        wikif = join(root, f)
                        mkdf = splitext(wikif.replace(wiki_root_path, mkd_output_dir))[0] + ".md"
                        vimwikifile2markdownfile(wikif, mkdf, mkd_type)
                    else:
                        nonwikif = join(root, f)
                        copy(nonwikif, nonwikif.replace(wiki_root_path, mkd_output_dir))

            else:
                for f in files:
                    (filename, fileext) = splitext(f)
                    if fileext == wiki_ext:
                        wikif = join(root, f)
                        mkdf = splitext(wikif)[0] + ".md"
                        vimwikifile2markdownfile(wikif, mkdf, mkd_type)

    else:
        return

if __name__=='__main__':
    main()
