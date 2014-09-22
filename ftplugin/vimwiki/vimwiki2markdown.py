# encoding: utf-8

import re

url1 = re.compile(r'^([a-zA-z]+://[^\s]*)(\s*)')
url2 = re.compile(r'(\s)([a-zA-z]+://[^\s]*)(\s*)')
email = re.compile(r'(mailto:)?(?P<mail>\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)')
lbold1 = re.compile(r' \*(\S)')
lbold2 = re.compile(r'^\*(\S)')
#lbold3 = re.compile(r'^(\s*>+)\*(\S)')
rbold1  = re.compile(r'(\S)\* ')
rbold2  = re.compile(r'(\S)\*$')
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

def blockquote(m):
    return m.group('space').replace('\t', '>').replace('    ', '>')

def vimwiki2markdown(text, mkdtype = 'pelican'):
    if re.search(r'(?mi)^%nohtml', text) != None:
        return ''
        #return []

    # Code block
    if (mkdtype == 'pelican'):
        text = re.sub(r'(?im)^\s*({{{)[ \t]*class="brush:[ \t]*(.*?)"', r'\1\n:::\2\n', text)
        text = re.sub(r'(?im)^\s*({{{)[ \t]*([\w].*)', r'\1\n:::\2\n', text)

    text = re.sub(r'(?ms)^(?P<preline>\s*[-*#] .*?)\n+(?P<indent>{{{.*?}}})',
            indent4, text)

    text_list_split_by_codeblock = \
            re.split(r'(?ms)({{{.*?}}})', text)
            #re.split(r'(?ms)(^\s*{{{.*?}}}\s*$)', text)

    for i, text in enumerate(text_list_split_by_codeblock):
        if not text.startswith('{{{') or not text.endswith('}}}'):
            # eol(Only for non code block)
            text = re.sub('\r\n', '\n', text)

            if (mkdtype == 'pelican'):
                # Metadata(Only for non code block)
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

            # Comment(Only for non code block)
            text = re.sub(r'(?m)^%% (.*)$', r'<!-- \1 -->', text)

            # Header(Only for non code block)
            text = re.sub(r'(?m)^======[ \t]+(.*)[ \t]+======\s*$', r'###### \1\n', text)
            text = re.sub(r'(?m)^=====[ \t]+(.*)[ \t]+=====\s*$', r'##### \1\n', text)
            text = re.sub(r'(?m)^====[ \t]+(.*)[ \t]+====\s*$', r'#### \1\n', text)
            text = re.sub(r'(?m)^===[ \t]+(.*)[ \t]+===\s*$', r'### \1\n', text)
            text = re.sub(r'(?m)^==[ \t]+(.*)[ \t]+==\s*$', r'## \1\n', text)
            if mkdtype == 'pelican':
                text = re.sub(r'(?m)^=[ \t]+(.*)[ \t]+=\s*$', r'\n', text)
            elif mkdtype == 'strict':
                text = re.sub(r'(?m)^=[ \t]+(.*)[ \t]+=\s*$', r'\1\n====\n', text)

            # Centered Header(Only for non code block)
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
            for line in text.split('\n'):
                #line = line.rstrip()
                line_list_split_by_inlinecode = inlinecode.split(line)

                for j, line in enumerate(line_list_split_by_inlinecode):
                    if not (line.startswith('`') and line.endswith('`')):
                        # Link(Both for non code block and non inline code)
                        line = link1.sub(r'[\2](\1)', line)
                        line = diarylink.sub(r'[\2](diary/\2)', line)
                        line = link2.sub(r'[\1](\1)', line)

                        # Image link(Both for non code block and non inline code)
                        line = image1.sub(r'![\2](\1)', line)
                        line = image2.sub(r'![pic](\1)', line)

                        # Raw URLs(Both for non code block and non inline code)
                        line = url1.sub(r'<\1>\2', line)
                        line = url2.sub(r'\1<\2>\3', line)
                        line = email.sub(r'<\g<mail>>', line)

                        # Bold text(Both for non code block and non inline code)
                        line = lbold1.sub(r' **\1', line)
                        line = lbold2.sub(r'**\1', line)
                        #line = lbold3.sub(r'\1**\2', line)
                        line = rbold1.sub(r'\1** ', line)
                        line = rbold2.sub(r'\1**', line)

                    line_list_split_by_inlinecode[j] = line

                line = ''.join(line_list_split_by_inlinecode)
                a.append(line)
            text = '\n'.join(a)

            # Blockquotes(Only for non code block)
            text = re.sub(r'(?m)^(?P<space>(    |\t)+)(?!(\* |- |# |\d[.] |\s*$))', blockquote, text)
            text = re.sub(r'(?ms)^(?P<preline>\s*[-*#] .*?)\n+(?P<indent>>.*?)(?P<suffix>\n[^>])',
                    indent4, text)

            # Ordered list(Only for non code block)
            text = re.sub(r'(?m)^(\s*)# (.*)$', r'\g<1>1. \2', text)
        else:
            #text = re.sub(r'(?ms){{{\s*\n(?P<indent>.*?)\n\s*}}}', indent4, text)
            text = re.sub(r'(?ms){{{[^\n]*\n(?P<indent>.*?)\n[^\n]*}}}', indent4, text)

        text_list_split_by_codeblock[i] = text

    text = ''.join(text_list_split_by_codeblock)

    return text
    #return a
