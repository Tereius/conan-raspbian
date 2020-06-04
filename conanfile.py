#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
from conans.errors import ConanException
import os
import shutil


class RaspbianConan(ConanFile):
    name = "raspbian"
    version = "2020-02-14"
    description = "Linaro Cross-Toolchain"
    url = "https://github.com/Tereius/conan-raspbian"
    homepage = "https://github.com/raspberrypi/tools"
    default_user = "tereius"
    default_channel = "stable"
    exports = ["raspbian.toolchain.cmake"]
    #short_paths = True
    #no_copy_source = True
    #options = {"makeStandalone": [True, False]}
    #default_options = "makeStandalone=True"
    settings = {
                "compiler": ["gcc"],
                "os": ["Linux"],
                "arch": "armv6"}

    def source(self):
        self.run("git clone https://github.com/raspberrypi/tools.git")
        #tools.get("https://github.com/raspberrypi/tools/archive/master.zip")
        #tools.get("https://downloads.raspberrypi.org/raspbian_lite/archive/2020-02-14-13:49/root.tar.xz")
        #os.unlink("root.tar.xz")

    @property
    def toolchain(self):
        return {"armv6": "arm-linux-gnueabihf",
                "armv6hf": "arm-linux-gnueabihf"}.get(str(self.settings.arch))

    @property
    def android_arch(self):
        return {"armv7": "arm",
                "armv8": "arm64",
                "mips": "mips",
                "mips64": "mips64",
                "x86": "x86",
                "x86_64": "x86_64"}.get(str(self.settings.arch))

    @property
    def android_abi(self):
        return {"armv7": "armeabi-v7a",
                "armv8": "arm64-v8a",
                "mips": "mips",
                "mips64": "mips64",
                "x86": "x86",
                "x86_64": "x86_64"}.get(str(self.settings.arch))

    @property
    def triplet(self):
        arch = {'armv6': 'arm',
                'armv6hf': 'arm',
                'armv7': 'arm',
                'armv7hf': 'arm',
                'armv8': 'arm'}.get(str(self.settings.arch))
        return '%s-linux-%s' % (arch, "gnueabihf")

    def package(self):
        self.copy(pattern="*")

    def define_tool_var(self, name, value, ndk_bin):
        path = os.path.join(ndk_bin, value)
        self.output.info('Creating %s environment variable: %s' % (name, path))
        return path

    def package_info(self):
        package = self.package_folder
        toolchain = os.path.join(package, 'tools', 'arm-bcm2708', self.toolchain)
        cmake_toolchain = os.path.join(package, 'raspbian.toolchain.cmake')
        toolchain_bin = os.path.join(toolchain, 'bin')

        self.output.info('Creating RASPBIAN_ROOT environment variable: %s' % package)
        self.env_info.RASPBIAN_ROOT = package

        self.output.info('Creating CHOST environment variable: %s' % self.toolchain)
        self.env_info.CHOST = self.toolchain

        self.output.info('Appending PATH environment variable: %s' % toolchain_bin)
        self.env_info.PATH.append(toolchain_bin)
        
        sysroot = os.path.join(toolchain, self.toolchain, 'sysroot')
        
        self.output.info('Creating CONAN_CMAKE_TOOLCHAIN_FILE environment variable: %s' % cmake_toolchain)
        self.env_info.CONAN_CMAKE_TOOLCHAIN_FILE = cmake_toolchain
        
        self.output.info('Creating CONAN_CMAKE_FIND_ROOT_PATH environment variable: %s' % sysroot)
        self.env_info.CONAN_CMAKE_FIND_ROOT_PATH = sysroot
        
        self.output.info('Creating SYSROOT environment variable: %s' % sysroot)
        self.env_info.SYSROOT = sysroot

        self.output.info('Creating self.cpp_info.sysroot: %s' % sysroot)
        self.cpp_info.sysroot = sysroot

        self.env_info.CC = self.define_tool_var('CC', self.toolchain + '-gcc', toolchain_bin)
        self.env_info.CXX = self.define_tool_var('CXX', self.toolchain + '-g++', toolchain_bin)
        self.env_info.AS = self.define_tool_var('AS', self.toolchain + '-as', toolchain_bin)
        self.env_info.LD = self.define_tool_var('LD', self.toolchain + '-ld', toolchain_bin)
        self.env_info.AR = self.define_tool_var('AR', self.toolchain + '-ar', toolchain_bin)
        self.env_info.RANLIB = self.define_tool_var('RANLIB', self.toolchain + '-ranlib', toolchain_bin)
        self.env_info.STRIP = self.define_tool_var('STRIP', self.toolchain + '-strip', toolchain_bin)
        self.env_info.NM = self.define_tool_var('NM', self.toolchain + '-nm', toolchain_bin)
        self.env_info.ADDR2LINE = self.define_tool_var('ADDR2LINE', self.toolchain + '-addr2line', toolchain_bin)
        self.env_info.OBJCOPY = self.define_tool_var('OBJCOPY', self.toolchain + '-objcopy', toolchain_bin)
        self.env_info.OBJDUMP = self.define_tool_var('OBJDUMP', self.toolchain + '-objdump', toolchain_bin)
        self.env_info.READELF = self.define_tool_var('READELF', self.toolchain + '-readelf', toolchain_bin)
        self.env_info.ELFEDIT = self.define_tool_var('ELFEDIT', self.toolchain + '-elfedit', toolchain_bin)
