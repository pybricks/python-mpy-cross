from enum import IntFlag
import struct

from mpy_cross_v5 import mpy_cross_compile, mpy_cross_version


class FeatureFlags(IntFlag):
    UNICODE = 1 << 1


def test_compile_no_opts():
    p, mpy = mpy_cross_compile("test.py", "")
    p.check_returncode()
    assert mpy is not None

    magic, version, flags, small_int_bits = struct.unpack_from("BBBB", mpy)

    assert chr(magic) == "M"
    assert version == 5
    assert flags == FeatureFlags.UNICODE
    assert small_int_bits == 31


def test_compile_opt_no_unicode():
    p, mpy = mpy_cross_compile("test.py", "", no_unicode=True)
    p.check_returncode()

    magic, version, flags, small_int_bits = struct.unpack_from("BBBB", mpy)

    assert chr(magic) == "M"
    assert version == 5
    assert flags == 0
    assert small_int_bits == 31


def test_compile_opt_small_int_bits():
    p, mpy = mpy_cross_compile("test.py", "", small_number_bits=63)
    p.check_returncode()
    assert mpy is not None

    magic, version, flags, small_int_bits = struct.unpack_from("BBBB", mpy)

    assert chr(magic) == "M"
    assert version == 5
    assert flags == FeatureFlags.UNICODE
    assert small_int_bits == 63


def test_compile_with_syntax_error():
    p, mpy = mpy_cross_compile("test.py", "$")

    assert p.returncode != 0
    assert b"SyntaxError:" in p.stderr
    assert mpy is None


def test_version():
    ver = mpy_cross_version()

    assert "mpy-cross emitting mpy v5" in ver
