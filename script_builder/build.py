#!/usr/bin/python3

import pathlib
import stat

PD = pathlib.Path(pathlib.Path(__file__).parent)

patch_content = ""
setup_content = ""

for qt_patch_file in list(PD.glob("qt_patches/*.txt")):
    content = 'if [[ "$Qt"=="'
    content += pathlib.PurePath(qt_patch_file).stem + '"'
    content += ' ]]; then\n'
    with open(qt_patch_file) as f:
        content += f.read()
    content += "\nfi\n"

    patch_content += content

with open(pathlib.Path(PD, "configure.example")) as f:
    setup_content += f.read()

setup_content = setup_content.replace("***CONTENT_TO_BE_REPLACED***",
                                      patch_content)

setup_file = pathlib.Path(PD, "..", "configure")

if(setup_file.exists()):
    setup_file.unlink()

with open(setup_file, 'w') as f:
    f.write(setup_content)

setup_file.chmod(setup_file.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP |
                 stat.S_IXOTH)
