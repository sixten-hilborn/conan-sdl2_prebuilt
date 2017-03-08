from conans import ConanFile, CMake
from conans.tools import get, download, replace_in_file, SystemPackageTool
import os, shutil

class SDL2PrebuiltConan(ConanFile):
    name = "SDL2_prebuilt"
    description = 'SDL2 binaries'
    version = "any"
    folders = []
    settings = "os", "arch"
    generators = "cmake"
    url = "http://github.com/sixten-hilborn/conan-sdl2_prebuilt"
    license = "Zlib - https://en.wikipedia.org/wiki/Zlib_License"
    exports = ["install_mac.sh"]

    def system_requirements(self):
        if self.settings.os == "Linux":
            installer = SystemPackageTool()
            for package in ["libsdl2-dev", "libsdl2-mixer-dev", "libsdl2-image-dev", "libsdl2-gfx-dev", "libsdl2-ttf-dev"]:
                if self.settings.arch == 'x86':
                    package += ':i386'
                elif self.settings.arch == 'x86_64':
                    package += ':amd64'
                installer.install(package)

    def source(self):
        if self.settings.os == "Windows":
            get("http://libsdl.org/release/SDL2-devel-2.0.5-VC.zip")
            get("https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-devel-2.0.1-VC.zip")
            get("https://www.libsdl.org/projects/SDL_image/release/SDL2_image-devel-2.0.1-VC.zip")
            get("https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-devel-2.0.14-VC.zip")
            get("https://github.com/sixten-hilborn/SDL2_gfx-prebuilt/raw/master/SDL2_gfx-devel-1.0.1-VC.zip")
        elif self.settings.os == "Macos":
            download("http://libsdl.org/release/SDL2-2.0.5.dmg", "SDL2-2.0.5.dmg")
            download("https://www.libsdl.org/projects/SDL_image/release/SDL2_image-2.0.1.dmg", "SDL2_image-2.0.1.dmg")
            download("https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.1.dmg", "SDL2_mixer-2.0.1.dmg")
            download("https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.14.dmg", "SDL2_ttf-2.0.14.dmg")

    def build(self):
        if self.settings.os == "Windows":
            self.folders = [
                'SDL2-2.0.5',
                'SDL2_mixer-2.0.1',
                'SDL2_image-2.0.1',
                'SDL2_ttf-2.0.14',
                'SDL2_gfx-1.0.1'
            ]
        elif self.settings.os == "Linux":
            pass
        elif self.settings.os == "Macos":
            self.run("bash -ex ./install_mac.sh")
        else:
            raise Exception(str(self.settings.os) + ' is not yet supported')

    def package(self):
        arch = 'x86' if self.settings.arch == 'x86' else 'x64'
        for folder in self.folders:
            self.copy(pattern="*.h", dst="include/SDL2", src="{0}/include".format(folder))
            self.copy(pattern="*.lib", dst="lib", src="{0}/lib/{1}".format(folder, arch), keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src="{0}/lib/{1}".format(folder, arch), keep_path=False)

    def package_info(self):
        if self.settings.os == 'Macos':
            frameworks = [
                "-framework SDL2",
                "-framework SDL2_image",
                "-framework SDL2_mixer",
                "-framework SDL2_ttf",
            ]
            self.cpp_info.cflags.extend(frameworks)
            self.cpp_info.cppflags.extend(frameworks)
            self.cpp_info.exelinkflags.extend(frameworks)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        else:
            self.cpp_info.libs = ["SDL2", "SDL2_mixer", "SDL2_image", "SDL2_ttf", "SDL2_gfx"]
        # Workaround to skip dat SDL2main stuff
        self.cpp_info.defines = ["_SDL_main_h"]
