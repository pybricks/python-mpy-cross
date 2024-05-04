import pathlib
import platform
import shutil
import subprocess
from distutils.command.build import build
from distutils.command.install import install

from setuptools import setup
from wheel.bdist_wheel import bdist_wheel

PROJECT_DIR = pathlib.Path(__file__).parent
MPY_CROSS_DIR = PROJECT_DIR / "micropython" / "mpy-cross"

# map of distutils platform id to compiler target triple
PLAT_TO_CLANG_TARGET = {
    "macosx-10.9-x86_64": "-target x86_64-apple-macos10.9",
    "macosx-10.12-x86_64": "-target x86_64-apple-macos10.12",
    "macosx-11.0-arm64": "-target arm64-apple-macos11",
    "macosx-12-arm64": "-target arm64-apple-macos12",
}


class custom_build(build):
    def run(self):
        super().run()

        mpy_cross_exe = (
            MPY_CROSS_DIR / f"build-{self.plat_name}" / "mpy-cross"
        ).with_suffix(".exe" if platform.system() == "Windows" else "")

        # all builds put exe in the same place, so we have to remove to avoid
        # make not rebuilding for different arch
        mpy_cross_exe.unlink(missing_ok=True)

        make_command = [
            "make",
            "-C",
            MPY_CROSS_DIR,
            f"BUILD=build-{self.plat_name}",
        ]

        # special case to handle potential cross-compiling on macOS
        if self.plat_name.startswith("macosx"):
            cflags = PLAT_TO_CLANG_TARGET[self.plat_name]

            make_command.extend(
                [
                    f"CFLAGS_EXTRA={cflags}",
                    f"LDFLAGS_EXTRA={cflags}",
                ]
            )

        subprocess.check_call(make_command)

        shutil.copy(str(mpy_cross_exe), self.build_lib + "/mpy_cross_v6_2")


class custom_install(install):
    def finalize_options(self) -> None:
        super().finalize_options()
        self.install_lib = self.install_lib.replace("/purelib/", "/platlib/")


class custom_bdist_wheel(bdist_wheel):
    def finalize_options(self):
        super().finalize_options()

        # this indicates that there is a binary component so that we get the
        # binary platform tag later instead of "any"
        self.root_is_pure = False

    def get_tag(self):
        _, _, platform_tag = super().get_tag()

        # since this isn't an extension that calls CPython APIs, we don't need
        # specific Python or ABI tags, only the platform
        return "py3", "none", platform_tag


setup(
    cmdclass={
        "build": custom_build,
        "install": custom_install,
        "bdist_wheel": custom_bdist_wheel,
    },
)
