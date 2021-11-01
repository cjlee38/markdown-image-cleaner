# Markdown-Image-Cleaner
This program can delete or display images which are not linked to Markdown files.
It is written in Python 3.8, but migth be used in different version.


# Requirements

(In progress...)

# Usage
You can also see help described below with command `python3 main.py --help`

## Parameters
1. `--clean-type`, `-c` : determine type to clean. options are `display`, `collect`, `sweep`
    1) `dispay` : just show you image links not connected to any file or web. And if there is any image file (.png, .jpg) also not connected to any link, it will also show it
  	2) `collect` : Annotate links that are not linked to the file, and collect image files not connected to any link on current directory
  	3) `sweep` : (WARNING) remove links, and delete file. This action is irreversible.(Not implemented yet)

2. `--directory` : select project directory. default is current directory (.)
3. `--ignore-image`, `-i` : Image files in these specified directories will be ignored
4. `--ignore-markdown`, `-m` : Markdown files in these specified directories will be ignored

# p.s.
This program is demo program, so not tested enough. be careful on using it.
