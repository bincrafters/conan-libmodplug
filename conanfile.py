# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibmodplugConan(ConanFile):
    name = "libmodplug"
    version = "0.8.9.0"
    description = "libmodplug - the library which was part of the Modplug-xmms project"
    topics = ("conan", "libmodplug", "audui", "multimedia", "sound", "music", "mod", "mod music",
              "tracket music")
    url = "https://github.com/bincrafters/conan-libmodplug"
    homepage = "http://modplug-xmms.sourceforge.net/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Unlicense"  # public domain
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://netcologne.dl.sourceforge.net/project/modplug-xmms/{n}/{v}/libmodplug-{v}.tar.gz".format(v=self.version, n=self.name)
        tools.get(source_url, sha256="457ca5a6c179656d66c01505c0d95fafaead4329b9dbaa0f997d00a3508ad9de")
        os.rename(self.name + "-" + self.version, self._source_subfolder)

        # CMakeLists.txt is missing from distribution
        tools.download("https://raw.githubusercontent.com/Konstanty/libmodplug/master/CMakeLists.txt",
                       os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["modplug"]
        self.cpp_info.includedirs.append(os.path.join("include", "libmodplug"))
        if not self.options.shared:
            self.cpp_info.defines.append("MODPLUG_STATIC")
