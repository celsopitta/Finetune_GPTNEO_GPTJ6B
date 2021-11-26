

import logging
import math
import os
import sys
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
import re
import argparse
import shutil


parser = argparse.ArgumentParser("limpa checkpoints")
parser.add_argument("-d","--directory",type=str, default='/data/training/gptj-qa-classifier')

args = parser.parse_args()
input_dir = args.directory

PREFIX_CHECKPOINT_DIR = "checkpoint"
_re_checkpoint = re.compile(r"^" + PREFIX_CHECKPOINT_DIR + r"\-(\d+)$")


def get_first_checkpoint(folder):
    content = os.listdir(folder)
    checkpoints = [
        path
        for path in content
        if _re_checkpoint.search(path) is not None and os.path.isdir(os.path.join(folder, path))
    ]
    if len(checkpoints) == 0:
        return
    
    return os.path.join(folder, min(checkpoints, key=lambda x: int(_re_checkpoint.search(x).groups()[0]))), len(checkpoints)


first_checkpoint, n_checkpoints = get_first_checkpoint(input_dir)
disk_info = shutil.disk_usage(input_dir)

print(f'first_checkpoint:{first_checkpoint}, number of checkpoints:{n_checkpoints}, free disk space (GB):{disk_info.free/(1000**3) }')

if n_checkpoints > 2 and disk_info.free/(1000**3) < 150.0:
    print(f'Removing checkpoint{first_checkpoint}')
    shutil.rmtree(first_checkpoint)