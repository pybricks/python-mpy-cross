# Python packaging for mpy-cross

This repository contains Python packaging to distribute the `mpy-cross` tool
from [MicroPython](https://github.com/micropython/micropython) via PyPI.

There are multiple MPY ABI versions, so you will need to install the package
that corresponds to the target MicroPython version.

For MicroPython 1.12 to 1.18:

    pip install mpy-cross-v5

For MicroPython 1.19:

    pip install mpy-cross-v6

For MicroPython 1.20+:

    pip install mpy-cross-v6.1
