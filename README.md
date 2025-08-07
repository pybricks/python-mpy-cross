# Python packaging for mpy-cross

This repository contains Python packaging to distribute the `mpy-cross` tool
from [MicroPython](https://github.com/micropython/micropython) via PyPI.

There are multiple MPY ABI versions, so you will need to install the package
that corresponds to the target MicroPython version.

Alternatively, you can install the [mpy-cross-multi](https://pypi.org/project/mpy-cross-multi/)
package to install all versions of `mpy-cross` at once.

For MicroPython 1.23 and up:

    pip install mpy-cross-v6.3

For MicroPython 1.22:

    pip install mpy-cross-v6.2

For MicroPython 1.20 to 1.21:

    pip install mpy-cross-v6.1

For MicroPython 1.19:

    pip install mpy-cross-v6

For MicroPython 1.12 to 1.18:

    pip install mpy-cross-v5
