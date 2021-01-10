# leeleilei.github.io

## Introduction
This is a simple static site with markdown files only. 
The render depends on github's own markdown to html.

The markdown syntax follows Github markdown format and supports metadata as well.

It is rendered everytime when pushing by Github Action.
See [blank.yaml](.github/workflows/blank.yaml) for detail.

**It does not supported nested path in folders**. It is flat and use tag to organize your content.

## Requirements
```
Python 3.8
```

## Usage
### Pages

Place your pages in ./pages

### Posts

Place your posts in ./posts

### Bookmarks
Place your personal bookmarks in ./bookmarks. Basically it is another 
repository that sync. specific bookmarks from "SAVE" bookmark api.

Place ```urlitem``` meta in metadata section.
### About

Place resume and tags in about


