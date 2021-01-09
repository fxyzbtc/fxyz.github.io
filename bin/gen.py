# -*- coding: utf8 -*-

from os import name
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)
import re
import datetime
from markdown2 import markdown
RE_TITLE = re.compile(r'(?<=<title>).*(?=</title>)')
PATHS = map(Path, ['about', 'pages', 'posts'])
BOOKMARKS = map(Path, ['bookmarks'])

EXTS = ('md', 'html', 'htm')

# 解析html的title
def extract_html_title(fpath: Path) -> str:
    '''提取html.title作为链接名字'''
    html = open(fpath).read()
    try:
        title = RE_TITLE.findall(html)[0]
    except IndexError:
        title = fpath.name
    finally:
        return title

class MD(object):
    def __init__(self, fpath: Path):
        with open(fpath, encoding='utf8') as fp:
            self.md = markdown(fp.read(), extras=['metadata'])

    @property
    def date(self) -> str:
        try:
            return self.md.metadata['date'][:10]
        except KeyError:
            return datetime.datetime.now().strftime('%Y-%m-%d')
    
    @property
    def title(self) -> str:
        try:
            return self.md.metadata['title']
        except KeyError:
            return 'No Title'
    # 解析md的tag字段
    @property
    def tags(self) -> list:
        try:
            tags = self.md.metadata['tags'].replace('[').replace(']').split(',')
        except KeyError:
            tags = []
        finally:
            return tags

    # 判断是否是draft
    @property
    def is_draft(self) -> bool:
        try:
            draft = self.md.metadata['draft']
        except KeyError:
            draft = 'false'
        finally:
            return True if 'true' in draft else False

def main(dirs: Iterator, index: Path, tpl: str) -> None:
    """
    dir: Path, be iterated path
    index: Path, be written with file list
    """
    with open(index, 'w', encoding='utf8') as index_fp:
        result = []
        result.append(tpl)
        for fpath in dirs:
            result.append(f'## {fpath.name}')
            for sub_fpath in fpath.iterdir():
                if sub_fpath.is_file() and sub_fpath.name.split('.')[1] == 'md':
                    mk = MD(sub_fpath)
                    if not mk.is_draft:
                        result.append(f'1. {mk.date}, [{mk.title}]({fpath.name}/{sub_fpath.name})')
                
                if sub_fpath.is_file() and sub_fpath.name.split('.')[1] == 'html':
                    
                    title = extract_html_title(sub_fpath)
                    result.append(f'1. [{title}]({fpath.name}/{sub_fpath.name})')
        index_fp.write('\n'.join(result))
        logging.info(f'{index.name} is updated successfully')

if __name__ == '__main__':
    updated_time = datetime.datetime.now().strftime('%Y-%m-%d')
    index_tpl = f'> Last Update: {updated_time}\n'
    main(PATHS, Path('index.md'), tpl=index_tpl)

    bookmarks_tpl = '''---
title: "我的书签"
---
'''
    main(BOOKMARKS, Path('pages/bookmarks.md'), tpl=bookmarks_tpl)

