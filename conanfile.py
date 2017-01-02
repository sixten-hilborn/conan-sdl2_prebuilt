from conans import ConanFile, CMake
from conans.tools import get, replace_in_file
import os, shutil

class SDL2PrebuiltConan(ConanFile):
    name = "SDL2_prebuilt"
    description = 'SDL2 binaries'
    version = "any"
    folders = []
    settings = "os", "arch", "compiler"
    generators = "cmake"
    url = "http://github.com/sixten-hilborn/conan-sdl2_prebuilt"
    license = "Zlib - https://en.wikipedia.org/wiki/Zlib_License"

    def source(self):
        if self.settings.os == "Windows":
            get("http://libsdl.org/release/SDL2-devel-2.0.5-VC.zip")
            get("https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-devel-2.0.1-VC.zip")
            get("https://www.libsdl.org/projects/SDL_image/release/SDL2_image-devel-2.0.1-VC.zip")
            get("https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-devel-2.0.14-VC.zip")
            get("https://github.com/sixten-hilborn/SDL2_gfx-prebuilt/raw/master/SDL2_gfx-devel-1.0.1-VC.zip")

    def build(self):
        if self.settings.os == "Linux":
            # TODO: Should check if the packages are already installed
            self.run("sudo apt-get update && sudo apt-get install -y libsdl2-dev libsdl2-mixer-dev libsdl2-image-dev libsdl2-gfx-dev libsdl2-ttf-dev")
        elif self.settings.os == "Windows":
            self.folders = [
                'SDL2-2.0.5',
                'SDL2_mixer-2.0.1',
                'SDL2_image-2.0.1',
                'SDL2_ttf-2.0.14',
                'SDL2_gfx-1.0.1'
            ]
        else:
            raise Exception(str(self.settings.os) + ' is not yet supported')
        
    def package(self):
        arch = 'x86' if self.settings.arch == 'x86' else 'x64'
        for folder in self.folders:
            self.copy(pattern="*.h", dst="include/SDL2", src="{0}/include".format(folder))
            self.copy(pattern="*.lib", dst="lib", src="{0}/lib/{1}".format(folder, arch), keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src="{0}/lib/{1}".format(folder, arch), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SDL2", "SDL2_mixer", "SDL2_image", "SDL2_ttf", "SDL2_gfx"]
        # Workaround to skip dat SDL2main stuff
        self.cpp_info.defines = ["_SDL_main_h"]
