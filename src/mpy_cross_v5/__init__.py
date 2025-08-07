from enum import Enum
import subprocess
import sys
import pathlib
import platform
from typing import List, Optional, Tuple


MPY_CROSS_PATH = str(
    (pathlib.Path(__file__).parent / "mpy-cross")
    .with_suffix(".exe" if platform.system() == "Windows" else "")
    .absolute()
)


class Arch(Enum):
    X86 = "x86"
    X64 = "x64"
    ARMV6 = "armv6"
    ARMV7M = "armv7m"
    ARMV7EM = "armv7em"
    ARMV7EMSP = "armv7emsp"
    ARMV7EMDP = "armv7emdp"
    XTENSA = "xtensa"
    XTENSAWIN = "xtensawin"


class Emitter(Enum):
    BYTECODE = "bytecode"
    NATIVE = "native"
    VIPER = "viper"


def mpy_cross_compile(
    file_name: str,
    file_contents: str,
    optimization_level: Optional[int] = None,
    small_number_bits: Optional[int] = None,
    no_unicode: bool = False,
    arch: Optional[Arch] = None,
    emit: Optional[Emitter] = None,
    heap_size: Optional[int] = None,
    extra_args: Optional[List[str]] = None,
) -> Tuple[subprocess.CompletedProcess[bytes], Optional[bytes]]:
    """
    Compiles a file using mpy-cross.

    Args:
        file_name: The file name.
        file_contents: The MicroPython source code to compile.
        optimization_level: The optimization level 0 to 3.
        small_number_bits: The number of bits in a MP_SMALL_INT.
        no_unicode: Flag needed if the MicroPython target firmware was compiled
            with ``MICROPY_PY_BUILTINS_STR_UNICODE (0)``.
        arch: The target architecture.
        emit: The type of bytecodes to emit.
        heap_size: The heap size.
        extra_args: Additional args to pass directly.

    Returns:
        The completed process and the raw mpy data if compiling succeeded,
        otherwise ``None``.

    Example::

        proc, mpy = mpy_cross_compile("example.py", "print('hello mpy')")

        # be sure to check the return code for failure
        try:
            proc.check_returncode()
        except subprocess.CalledProcessError:
            # stderr should contain more information about the failure
            print(proc.stderr)
            ...

        ...

    """
    args: list[str] = [MPY_CROSS_PATH, "-", "-s", file_name]

    if optimization_level is not None:
        if optimization_level not in range(4):
            raise ValueError("optimization_level must be between 0 and 3")

        args.append(f"-O{optimization_level}")

    if small_number_bits is not None:
        args.append(f"-msmall-int-bits={small_number_bits}")

    if no_unicode:
        args.append("-mno-unicode")

    if arch is not None:
        args.append(f"-march={arch.value}")

    if emit is not None:
        args += ["-X", f"emit={emit.value}"]

    if heap_size is not None:
        args += ["-X", f"heapsize={heap_size}"]

    if extra_args:
        args += extra_args

    process = subprocess.run(args, capture_output=True, input=file_contents.encode())

    return process, process.stdout if process.returncode == 0 else None


def mpy_cross_version() -> str:
    """
    Gets the version string from the ``mpy-cross`` executable.
    """
    proc = subprocess.run([MPY_CROSS_PATH, "--version"], capture_output=True)
    proc.check_returncode()
    return proc.stdout.decode().strip()


def run() -> None:
    """
    Run mpy-cross directly.
    """
    proc = subprocess.run([MPY_CROSS_PATH] + sys.argv[1:])
    sys.exit(proc.returncode)
