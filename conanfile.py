#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


os.environ["CONAN_SKIP_BROKEN_SYMLINKS_CHECK"] = "True"

class RaspbianConan(ConanFile):
    name = "raspbian"
    version = "2020-02-14"
    description = "Linaro Cross-Toolchain"
    license = "GPL"
    url = "https://github.com/Tereius/conan-raspbian"
    homepage = "https://github.com/Pro/raspi-toolchain"
    default_user = "tereius"
    default_channel = "stable"
    exports_sources = ["rootfs.tar.gz"]
    settings = {"os": ["Linux"], "arch": None, "compiler": None, "build_type": None}

    def source(self):
        git = tools.Git("linux")
        tools.download("https://raw.githubusercontent.com/Pro/raspi-toolchain/v1.0.1/Toolchain-rpi.cmake",
                       "Toolchain-rpi.cmake")
        tools.replace_in_file("Toolchain-rpi.cmake",
                              "set(CMAKE_PREFIX_PATH \"${CMAKE_PREFIX_PATH};${SYSROOT_PATH}/usr/lib/${TOOLCHAIN_HOST}\")",
                              "set(CMAKE_PREFIX_PATH \"${CMAKE_PREFIX_PATH};${SYSROOT_PATH}/usr/lib/${TOOLCHAIN_HOST}\")\nset(CMAKE_PREFIX_PATH \"${CMAKE_PREFIX_PATH};${SYSROOT_PATH}/opt/vc\")")
        tools.get("https://github.com/Pro/raspi-toolchain/releases/download/v1.0.1/raspi-toolchain.tar.gz")

    @property
    def arch(self):
        if hasattr(self, "settings_target"):
            return self.settings_target.arch
        return self.settings.arch

    @property
    def toolchainabi(self):
        return "arm-linux-gnueabihf"

    def build(self):
        tools.unzip("rootfs.tar.gz", destination=self.package_folder)

    def package(self):
        self.copy(pattern="*")
        tools.replace_in_file(
            os.path.join(self.package_folder, "cross-pi-gcc", "arm-linux-gnueabihf", "lib", "libc.so"),
            "/opt/cross-pi-gcc/arm-linux-gnueabihf/lib", ".")

    def define_tool_var(self, name, value, bin_folder):
        path = os.path.join(bin_folder, value)
        self.output.info('Creating %s environment variable: %s' % (name, path))
        return path

    def package_info(self):
        package = self.package_folder

        toolchain = os.path.join(package, 'cross-pi-gcc')

        cmake_toolchain = os.path.join(package, 'Toolchain-rpi.cmake')
        toolchain_bin = os.path.join(toolchain, 'bin')

        self.output.info('Creating RASPBIAN_ROOT environment variable: %s' % package)
        self.env_info.RASPBIAN_ROOT = package

        self.output.info('Creating CHOST environment variable: %s' % self.toolchainabi)
        self.env_info.CHOST = self.toolchainabi

        self.output.info('Appending PATH environment variable: %s' % toolchain_bin)
        self.env_info.PATH.append(toolchain_bin)

        self.output.info('Creating CONAN_CMAKE_TOOLCHAIN_FILE environment variable: %s' % cmake_toolchain)
        self.env_info.CONAN_CMAKE_TOOLCHAIN_FILE = cmake_toolchain

        rootfs = os.path.join(package, 'rootfs')
        self.output.info('Creating RASPBIAN_ROOTFS environment variable: %s' % rootfs)
        self.env_info.RASPBIAN_ROOTFS = rootfs

        self.env_info.CC = self.define_tool_var('CC', self.toolchainabi + '-gcc', toolchain_bin)
        self.env_info.CXX = self.define_tool_var('CXX', self.toolchainabi + '-g++', toolchain_bin)
        self.env_info.AS = self.define_tool_var('AS', self.toolchainabi + '-as', toolchain_bin)
        self.env_info.LD = self.define_tool_var('LD', self.toolchainabi + '-ld', toolchain_bin)
        self.env_info.AR = self.define_tool_var('AR', self.toolchainabi + '-ar', toolchain_bin)
        self.env_info.RANLIB = self.define_tool_var('RANLIB', self.toolchainabi + '-ranlib', toolchain_bin)
        self.env_info.STRIP = self.define_tool_var('STRIP', self.toolchainabi + '-strip', toolchain_bin)
        self.env_info.NM = self.define_tool_var('NM', self.toolchainabi + '-nm', toolchain_bin)
        self.env_info.ADDR2LINE = self.define_tool_var('ADDR2LINE', self.toolchainabi + '-addr2line', toolchain_bin)
        self.env_info.OBJCOPY = self.define_tool_var('OBJCOPY', self.toolchainabi + '-objcopy', toolchain_bin)
        self.env_info.OBJDUMP = self.define_tool_var('OBJDUMP', self.toolchainabi + '-objdump', toolchain_bin)
        self.env_info.READELF = self.define_tool_var('READELF', self.toolchainabi + '-readelf', toolchain_bin)
        self.env_info.ELFEDIT = self.define_tool_var('ELFEDIT', self.toolchainabi + '-elfedit', toolchain_bin)

    def package_id(self):
        del self.info.settings.arch
        del self.info.settings.build_type
