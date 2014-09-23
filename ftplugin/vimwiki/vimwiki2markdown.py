#!/usr/bin/env python
# encoding: utf-8

import re
import io

#codeblock = re.compile(r'(?ms)({{{.*?}}})')
#listblock = re.compile(r'(?m)^((?:\s*[-*#][ \t]+.*\n)(?:[^\n]+\n)*)')
#tableblock = re.compile(r'(?m)((?:^[ \t]*[|].*?[|].*?[|]\n){2,})')

list_item_begin = re.compile(r'^\s*[-*#]\s+')
url1 = re.compile(r'^([a-zA-z]+://[^\s]*)(\s*)')
url2 = re.compile(r'(\s)([a-zA-z]+://[^\s]*)(\s*)')
email = re.compile(r'(mailto:)?(?P<mail>\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)')
lbold1 = re.compile(r' \*(\S)')
lbold2 = re.compile(r'^\*(\S)')
rbold1  = re.compile(r'(\S)\* ')
rbold2  = re.compile(r'(\S)\*$')
lbold3 = re.compile(r'^(\s*>+)\*(\S)')
rbold3  = re.compile(r'(\S)\*\n')
link1 = re.compile(r'\[\[([^:][^|]+?)[|](.+?)\]\]')
link2 = re.compile(r'\[\[([^:].+?)\]\]')
diarylink = re.compile(r'\[\[(diary:)?(\d{4}-\d{2}-\d{2})\]\]')
image1 =  re.compile(r'{{([^|{]+?)[|]([^|]*?)([|]([^|]+?))?}}')
image2 =  re.compile(r'{{([^{]+?)}}')
inlinecode = re.compile(r'(`.+?`)')

def indent4(m):
    if ('preline' in m.groupdict()) and ('suffix' in m.groupdict()):
        return m.group('preline') + '\n    ' + m.group('indent').replace('\n', '\n    ') + m.group('suffix')
    elif 'preline' in m.groupdict():
        return m.group('preline') + '\n    ' + m.group('indent').replace('\n', '\n    ')
    else:
        return '\n    ' + m.group('indent').replace('\n', '\n    ')


def vimwiki2markdown(text, mkdtype = 'pelican'):
    if re.search(r'(?mi)^%nohtml', text) != None:
        return ''

    # eol
    text = re.sub('\r\n', '\n', text)

    # Code block
    if (mkdtype == 'pelican'):
        text = re.sub(r'(?im)^\s*({{{)[ \t]*class="brush:[ \t]*(.*?)".*$', r'\1\n:::\2', text)
        text = re.sub(r'(?im)^\s*({{{)[ \t]*([\w].*)$', r'\1\n:::\2', text)

    #text = re.sub(r'(?ms)^(?P<preline>\s*[-*#] .*?)\n+(?P<indent>{{{.*?}}})', indent4, text)
    text = re.sub(r'(?ms)^(?P<preline>\s*[-*#][ \t]+[^\n]*?)\s+(?P<indent>{{{.*?}}})', indent4, text)

    text_list_split_by_codeblock = \
            re.split(r'(?ms)({{{.*?}}})', text)
            #re.split(r'(?ms)(^\s*{{{.*?}}}\s*$)', text)

    for i, text in enumerate(text_list_split_by_codeblock):
        if not text.startswith('{{{') or not text.endswith('}}}'):
            if (mkdtype == 'pelican'):
                # Metadata
                text = re.sub(r'(?mi)^%title (.*)$', r'Title: \1', text)
                text = re.sub(r'(?mi)^%template (.*)$', r'Category: \1', text)
                text = re.sub(r'(?mi)^%toc.*$',r'[TOC]', text)
                text = re.sub(r'(?mi)^%% (Date:.*)$', r'\1',text)
                text = re.sub(r'(?mi)^%% (Modified:.*)$', r'\1', text)
                text = re.sub(r'(?mi)^%% (Tags:.*)$',r'\1', text)
                text = re.sub(r'(?mi)^%% (Slug:.*)$',r'\1', text)
            elif mkdtype == 'strict':
                text = re.sub(r'(?mi)^%title (.*)$', r'', text)
                text = re.sub(r'(?mi)^%template (.*)$', r'', text)
                text = re.sub(r'(?mi)^%toc.*$',r'', text)

            # Comment
            text = re.sub(r'(?m)^%% (.*)$', r'<!-- \1 -->', text)

            # Header
            text = re.sub(r'(?m)^======[ \t]+(.*)[ \t]+======\s*$', r'###### \1\n', text)
            text = re.sub(r'(?m)^=====[ \t]+(.*)[ \t]+=====\s*$', r'##### \1\n', text)
            text = re.sub(r'(?m)^====[ \t]+(.*)[ \t]+====\s*$', r'#### \1\n', text)
            text = re.sub(r'(?m)^===[ \t]+(.*)[ \t]+===\s*$', r'### \1\n', text)
            text = re.sub(r'(?m)^==[ \t]+(.*)[ \t]+==\s*$', r'## \1\n', text)
            if mkdtype == 'pelican':
                text = re.sub(r'(?m)^=[ \t]+(.*)[ \t]+=\s*$', r'\n', text)
            elif mkdtype == 'strict':
                text = re.sub(r'(?m)^=[ \t]+(.*)[ \t]+=\s*$', r'\1\n====\n', text)

            # Centered Header
            text = re.sub(r'(?m)^\s+======[ \t]+(.*)[ \t]+======\s*$',
                    r'<h6 style="text-align:center">\1</h6>\n', text)
            text = re.sub(r'(?m)^\s+=====[ \t]+(.*)[ \t]+=====\s*$',
                    r'<h5 style="text-align:center">\1</h5>\n', text)
            text = re.sub(r'(?m)^\s+====[ \t]+(.*)[ \t]+====\s*$',
                    r'<h4 style="text-align:center">\1</h4>\n', text)
            text = re.sub(r'(?m)^\s+===[ \t]+(.*)[ \t]+===\s*$',
                    r'<h3 style="text-align:center">\1</h3>\n', text)
            text = re.sub(r'(?m)^\s+==[ \t]+(.*)[ \t]+==\s*$',
                    r'<h2 style="text-align:center">\1</h2>\n', text)
            if mkdtype == 'pelican':
                text = re.sub(r'(?m)^\s+=[ \t]+(.*)[ \t]+=\s*$', r'', text)
            elif mkdtype == 'strict':
                text = re.sub(r'(?m)^\s+=[ \t]+(.*)[ \t]+=\s*$',
                        r'<h1 style="text-align:center">\1</h1>\n', text)

            a = []
            blockquote_start = False
            previous_line = None
            for line in text.split('\n'):
                if line.isspace():
                    line = ''
                    previous_line = line
                    a.append(line)
                    continue

                if (previous_line == '' or blockquote_start) and line.startswith(('    ','\t')) and list_item_begin.match(line) == None:
                    blockquote_start = True
                    line = '>' + line.lstrip() + '\n>'
                else:
                    blockquote_start = False

                previous_line = line

                line_list_split_by_inlinecode = inlinecode.split(line)

                for j, line in enumerate(line_list_split_by_inlinecode):
                    if not (line.startswith('`') and line.endswith('`')):
                        # Link
                        line = link1.sub(r'[\2](\1)', line)
                        line = diarylink.sub(r'[\2](diary/\2)', line)
                        line = link2.sub(r'[\1](\1)', line)

                        # Image link
                        line = image1.sub(r'![\2](\1)', line)
                        line = image2.sub(r'![pic](\1)', line)

                        # Raw URLs
                        line = url1.sub(r'<\1>\2', line)
                        line = url2.sub(r'\1<\2>\3', line)
                        line = email.sub(r'<\g<mail>>', line)

                        # Bold text
                        line = lbold1.sub(r' **\1', line)
                        line = lbold2.sub(r'**\1', line)
                        line = rbold1.sub(r'\1** ', line)
                        line = rbold2.sub(r'\1**', line)

                        line = lbold3.sub(r'\1**\2', line)
                        line = rbold3.sub(r'\1**\n', line)

                    line_list_split_by_inlinecode[j] = line

                line = ''.join(line_list_split_by_inlinecode)
                a.append(line)
            text = '\n'.join(a)

            text = re.sub(r'(?ms)^(?P<preline>\s*[-*#] [^\n]*?)\s+(?P<indent>>.*?)(?P<suffix>\n[^>])',
            # Blockquotes
                    indent4, text)

            # Ordered list
            text = re.sub(r'(?m)^(\s*)# (.*)$', r'\g<1>1. \2', text)
        else:
            text = re.sub(r'(?ms){{{[^\n]*\n(?P<indent>.*?)\n[^\n]*}}}', indent4, text)

        text_list_split_by_codeblock[i] = text

    text = ''.join(text_list_split_by_codeblock)

    return text


def vimwikifile2markdownfile(wikif, mkdf, mkdtype = 'pelican'):
    """Convert vimwiki file to markdown file

    :wikif: vimwiki file path
    :mkdf:  markdown file path
    :mkdtype: markdown file type

    """

    with io.open(wikif,'rt', encoding='utf-8') as wikifp:
          text = wikifp.read()

    mkd_contents = vimwiki2markdown(text, mkdtype)
    if mkd_contents:
        with io.open(mkdf, 'wt', encoding='utf-8') as mkdfp:
            mkdfp.write(mkd_contents)
