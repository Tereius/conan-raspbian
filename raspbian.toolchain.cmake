set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_SYSROOT $ENV{SYSROOT})
set(CMAKE_STAGING_PREFIX /home/devel/stage)

set(tools /home/devel/gcc-4.7-linaro-rpi-gnueabihf)
set(CMAKE_C_COMPILER $ENV{CC})
set(CMAKE_CXX_COMPILER $ENV{CXX})

# Those variables are not set by the NDK CMake toolchain, but
# CMAKE_<LANG>_STANDARD_LIBRARIES_INIT is.
# Therefore we must force clear it everytime
#unset(CMAKE_C_STANDARD_LIBRARIES CACHE)
#unset(CMAKE_CXX_STANDARD_LIBRARIES CACHE)

# Setting to BOTH will allow CMake to find zlib while still finding other Conan packages
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM BOTH)
