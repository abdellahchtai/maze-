#!/bin/env python3.10
from parsing import parse_config
from renderer import ft_render
import sys



if len(sys.argv) != 2:
    sys.exit(1)
config = parse_config(sys.argv[1])
if isinstance(config, Exception):
    print(config)
    sys.exit(1)
ft_render(config)
