# MapleWiki Skillbox Converter

Honestly pointless, so much hardcoding involved. I'm just putting it here to make it open how I did it so that people don't bug me.

## Usage

Type `from maplewikiskillbox import *` in a python console when the directory is the same as the py file. Tadaa, the functions are accessible!

`replace_all_skill_in_page()` takes a page's source code (copypasted from a page's Edit page, or extracted from API) and returns a converted page's source code, which can then be fed back into the wiki by an API. Alternatively it can also write to a new file.

## Demo

Just run `python demo.py`, which will demonstrate the code on a previous version of the Beast Tamer/Skills page. The output will be in `result.txt`, and copy-pasting its contents into the edit page of the maplewiki and previewing it will show you that the beast tamer page is now snazzy as FUCK