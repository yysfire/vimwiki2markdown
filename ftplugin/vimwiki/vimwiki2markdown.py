# encoding: utf-8

import re

def indent4(m):
    #codestr = m.group('indent')
    #codestr = re.sub(r'(?m)^(\s*)\* ', r'\1# ', codestr)
    if 'preline' not in m.groupdict():
        return '\n    ' + m.group('indent').replace('\n', '\n    ')
    else:
        return m.group('preline') + '\n    ' + m.group('indent').replace('\n', '\n    ')

def vimwiki2markdown(text, mkdtype = 'pelican'):
    if re.search(r'(?m)^%nohtml', text, re.IGNORECASE) != None:
        return ''
        #return []

    # eol(Only for non code block)
    text = re.sub('\r\n', '\n', text)

    # Metadata(Only for non code block)
    text = re.sub(r'(?m)^%title (.*)$', r'Title: \1', text, flags=re.IGNORECASE)
    text = re.sub(r'(?m)^%template (.*)$', r'Category: \1', text, flags=re.IGNORECASE)
    text = re.sub(r'(?m)^%toc.*$',r'[TOC]', text, flags=re.IGNORECASE)
    text = re.sub(r'(?m)^%% (Date:.*)$', r'\1',text, flags=re.IGNORECASE)
    text = re.sub(r'(?m)^%% (Modified:.*)$', r'\1', text, flags=re.IGNORECASE)
    text = re.sub(r'(?m)^%% (Tags:.*)$',r'\1', text, flags=re.IGNORECASE)
    text = re.sub(r'(?m)^%% (Slug:.*)$',r'\1', text, flags=re.IGNORECASE)
    # Comment(Only for non code block)
    text = re.sub(r'(?m)^%% (.*)$', r'<!-- \1 -->', text)

    # Header(Only for non code block)
    text = re.sub(r'(?m)^======[ \t]+(.*)[ \t]+======\s*$', r'###### \1\n', text)
    text = re.sub(r'(?m)^=====[ \t]+(.*)[ \t]+=====\s*$', r'##### \1\n', text)
    text = re.sub(r'(?m)^====[ \t]+(.*)[ \t]+====\s*$', r'#### \1\n', text)
    text = re.sub(r'(?m)^===[ \t]+(.*)[ \t]+===\s*$', r'### \1\n', text)
    text = re.sub(r'(?m)^==[ \t]+(.*)[ \t]+==\s*$', r'## \1\n', text)
    #text = re.sub(r'(?m)^=[ \t]+(.*)[ \t]+=\s*$', r'', text)
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
    #text = re.sub(r'(?m)^\s+=[ \t]+(.*)[ \t]+=\s*$', r'', text)
    text = re.sub(r'(?m)^\s+=[ \t]+(.*)[ \t]+=\s*$',
            r'<h1 style="text-align:center">\1</h1>\n', text)

    # Blockquotes(Only for non code block)
    #text = re.sub(r'(?m)^(    |\t)+(?!(\* |- |# |\d[.] ))', r'>', text)
    #text = re.sub(r'(?ms)^(\s*[-*#] .*?\n)(?P<indent>>.*?)\n{2,}[^> \t]',
            #indent4, text)

    # Code block
    if (mkdtype == 'pelican'):
        #text = re.sub(r'(?im)^\s*({{{)[ \t]*class="brush:[ \t]*(.*?)"', r'\n\1\n:::\2', text)
        #text = re.sub(r'(?im)^\s*({{{)[ \t]*([\w].*)', r'\n\1\n:::\2', text)
        text = re.sub(r'(?im)^\s*({{{)[ \t]*class="brush:[ \t]*(.*?)"', r'\1\n:::\2\n', text)
        text = re.sub(r'(?im)^\s*({{{)[ \t]*([\w].*)', r'\1\n:::\2\n', text)
    text = re.sub(r'(?ms)^(?P<preline>\s*[-*#] .*?)\n+(?P<indent>{{{.*?}}})',
            indent4, text)
    text = re.sub(r'(?ms){{{\s*\n(?P<indent>.*?)\n\s*}}}', indent4, text)

    # Ordered list(Only for non code block)
    text = re.sub(r'(?m)^(\s*)# (.*)$', r'\g<1>1. \2', text)

    a = []
    for line in text.split('\n'):
        #line = line.rstrip()

        # Link(Both for non code block and non inline code)
        line = re.sub(r'\[\[([^:][^|]+?)[|](.+?)\]\]', r'[\2](\1)', line)
        line = re.sub(r'\[\[([^:].+?)\]\]', r'[\1](\1)', line)

        # Image link(Both for non code block and non inline code)
        line = re.sub(r'{{([^|{]+?)[|]([^|]+?)}}', r'![\2](\1)', line)
        line = re.sub(r'{{([^{]+?)}}', r'![pic](\1)', line)

        # Raw URLs(Both for non code block and non inline code)
        url1 = re.compile(r'^([a-zA-z]+://[^\s]*)(\s*)')
        url2 = re.compile(r'(\s)([a-zA-z]+://[^\s]*)(\s*)')
        email = re.compile(r'(mailto:)?(?P<mail>\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)')
        line = url1.sub(r'<\1>\2', line)
        line = url2.sub(r'\1<\2>\3', line)
        line = email.sub(r'<\g<mail>>', line)

        # Bold text(Both for non code block and non inline code)
        lbold1 = re.compile(r' \*(\S)')
        lbold2 = re.compile(r'^\*(\S)')
        rbold  = re.compile(r'(\S)\* ')
        line = lbold1.sub(r' **\1', line)
        line = lbold2.sub(r'**\1', line)
        line = rbold.sub(r'\1** ', line)

        a.append(line)
    text = '\n'.join(a)
    #print("text is " + str(type(text)))

    return text
    #return a
