#! /usr/bin/env python
# encoding: utf-8
r"""
Simplistic utility to extract docstrings from a module or class and throw
them into a simple [GitHub Flavoured Markdown](md) document. Its purpose is
to quickly generate `README.md` files for small projects.

[md]: https://help.github.com/articles/github-flavored-markdown

### Project status

I stopped using this package and therefore will not push any updates (I now
usually write README.rst manually). Nonetheless, you may still find it useful.
Should you encounter bugs or have improvements, feel free to submit a PR. If
you want to take over maintenance, feel free to contact me.

For a more feature-rich and well maintained alternative, see:

- https://github.com/NiklasRosenstein/pydoc-markdown/ (I didn't try it)


### Installation

No installation necessary. However, if you want:

    $ pip install doc2md


### Usage

You can run this script from the command line like:

    $ doc2md.py [-a] [--no-toc] [-t title] [-d depth] module-name [class-name] \
        > README.md

At the moment  this is suited only  for a very specific use  case. It is
hardly forseeable, if I will decide to improve on it in the near future.

For a simple example output document, see the generated README (i.e. the
github frontpage). It is extracted from the `doc2md.py` file using this
very utility:

    $ ./doc2md.py -a -d1 doc2md > README.md


### License

Copyright © 2013-2017 Thomas Gläßle <t_glaessle@gmx.de>

This work  is free. You can  redistribute it and/or modify  it under the
terms of the MIT license. See the COPYING file for more details.

This program  is free software.  It comes  without any warranty,  to the
extent permitted by applicable law.
"""
import re
import sys
import inspect

__all__ = ['doctrim', 'doc2md']

doctrim = inspect.cleandoc

def unindent(lines):
    """
    Remove common indentation from string.

    Unlike doctrim there is no special treatment of the first line.

    """
    try:
        # Determine minimum indentation:
        indent = min(len(line) - len(line.lstrip())
                     for line in lines if line)
    except ValueError:
        return lines
    else:
        return [line[indent:] for line in lines]

def code_block(lines, language=''):
    """
    Mark the code segment for syntax highlighting.
    """
    return ['```' + language] + unindent(lines) + ['```']

def doctest2md(lines):
    """
    Convert the given doctest to a syntax highlighted markdown segment.
    """
    is_only_code = True
    lines = unindent(lines)
    for line in lines:
        if not line.startswith('>>> ') and not line.startswith('... ') and line not in ['>>>', '...']:
            is_only_code = False
            break
    if is_only_code:
        orig = lines
        lines = []
        for line in orig:
            lines.append(line[4:])
    return lines

def doc_code_block(lines, language):
    if language == 'python':
        lines = doctest2md(lines)
    return code_block(lines, language)

_reg_section = re.compile('^#+ ')
def is_heading(line):
    return _reg_section.match(line)

def get_heading(line):
    assert is_heading(line)
    part = line.partition(' ')
    return len(part[0]), part[2]

def make_heading(level, title):
    return '#'*max(level, 1) + ' ' + title

def find_sections(lines):
    """
    Find all section names and return a list with their names.
    """
    sections = []
    for line in lines:
        if is_heading(line):
            sections.append(get_heading(line))
    return sections

def make_toc(sections, maxdepth=0):
    """
    Generate table of contents for array of section names.
    """
    if not sections:
        return []
    outer = min(n for n,t in sections)
    refs = []
    for ind,sec in sections:
        if maxdepth and ind-outer+1 > maxdepth:
            continue
        ref = sec.lower()
        ref = ref.replace('`', '')
        ref = ref.replace(' ', '-')
        ref = ref.replace('?', '')
        refs.append("    "*(ind-outer) + "- [%s](#%s)" % (sec, ref))
    return refs

def _doc2md(lines, shiftlevel=0):
    md = []
    is_code = False
    for line in lines:
        trimmed = line.lstrip()
        if is_code:
            if line:
                code.append(line)
            else:
                is_code = False
                md += doc_code_block(code, language)
                md += [line]
        elif trimmed.startswith('>>> '):
            is_code = True
            language = 'python'
            code = [line]
        elif trimmed.startswith('$ '):
            is_code = True
            language = 'bash'
            code = [line]
        elif shiftlevel != 0 and is_heading(line):
            level, title = get_heading(line)
            md += [make_heading(level + shiftlevel, title)]
        else:
            md += [line]
    if is_code:
        md += doc_code_block(code, language)
    return md

def doc2md(docstr, title, min_level=1, more_info=False, toc=True, maxdepth=0):
    """
    Convert a docstring to a markdown text.
    """
    text = doctrim(docstr)
    lines = text.split('\n')

    sections = find_sections(lines)
    if sections:
        level = min(n for n,t in sections) - 1
    else:
        level = 1

    shiftlevel = 0
    if level < min_level:
        shiftlevel = min_level - level
        level = min_level
        sections = [(lev+shiftlevel, tit) for lev,tit in sections]

    head = next((i for i, l in enumerate(lines) if is_heading(l)), 0)
    md = [
        make_heading(level, title),
        "",
    ] + lines[:head]
    if toc:
        md += make_toc(sections, maxdepth)
        md += ['']
    md += _doc2md(lines[head:], shiftlevel)
    if more_info:
        return (md, sections)
    else:
        return "\n".join(md)

def mod2md(module, title, title_api_section, toc=True, maxdepth=0):
    """
    Generate markdown document from module, including API section.
    """
    docstr = module.__doc__

    text = doctrim(docstr)
    lines = text.split('\n')

    sections = find_sections(lines)
    if sections:
        level = min(n for n,t in sections) - 1
    else:
        level = 1

    api_md = []
    api_sec = []
    if title_api_section and module.__all__:
        sections.append((level+1, title_api_section))
        for name in module.__all__:
            api_sec.append((level+2, "`" + name + "`"))
            api_md += ['', '']
            entry = module.__dict__[name]
            if entry.__doc__:
                md, sec = doc2md(entry.__doc__, "`" + name + "`",
                        min_level=level+2, more_info=True, toc=False)
                api_sec += sec
                api_md += md

    sections += api_sec

    # headline
    head = next((i for i, l in enumerate(lines) if is_heading(l)), 0)
    md = [
        make_heading(level, title),
        "",
    ] + lines[:head]

    # main sections
    if toc:
        md += make_toc(sections, maxdepth)
        md += ['']
    md += _doc2md(lines[head:])

    # API section
    md += [
        '',
        '',
        make_heading(level+1, title_api_section),
    ]
    if toc:
        md += ['']
        md += make_toc(api_sec, 1)
    md += api_md

    return "\n".join(md)

def main(args=None):
    # parse the program arguments
    import argparse
    parser = argparse.ArgumentParser(
            description='Convert docstrings to markdown.')

    parser.add_argument(
            'module', help='The module containing the docstring.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
            'entry', nargs='?',
            help='Convert only docstring of this entry in module.')
    group.add_argument(
            '-a', '--all', dest='all', action='store_true',
            help='Create an API section with the contents of module.__all__.')
    parser.add_argument(
            '-t', '--title', dest='title',
            help='Document title (default is module name)')
    parser.add_argument(
            '--no-toc', dest='toc', action='store_false', default=True,
            help='Do not automatically generate the TOC')
    parser.add_argument(
            '-d', '--depth', dest='depth', type=int, default=0,
            help='Max subsection level in TOC')
    args = parser.parse_args(args)

    import importlib
    import inspect
    import os

    def add_path(*pathes):
        for path in reversed(pathes):
            if path not in sys.path:
                sys.path.insert(0, path)

    file = inspect.getfile(inspect.currentframe())
    add_path(os.path.realpath(os.path.abspath(os.path.dirname(file))))
    add_path(os.getcwd())

    mod_name = args.module
    if mod_name.endswith('.py'):
        mod_name = mod_name.rsplit('.py', 1)[0]
    title = args.title or mod_name.replace('_', '-')

    module = importlib.import_module(mod_name)

    if args.all:
        print(mod2md(module, title, 'API', toc=args.toc, maxdepth=args.depth))

    else:
        if args.entry:
            docstr = module.__dict__[args.entry].__doc__
        else:
            docstr = module.__doc__

        print(doc2md(docstr, title, toc=args.toc, maxdepth=args.depth))

if __name__ == "__main__":
    main()
