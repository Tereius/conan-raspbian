#/bin/bash

current=$(pwd)

rsync -vR --progress -rl --delete-after --copy-unsafe-links pi@$1:/{lib,usr,etc/ld.so.conf.d,opt/vc/lib,opt/vc/include} $(pwd)/rootfs

rm -r $(pwd)/rootfs/usr/bin/*
rm -r $(pwd)/rootfs/usr/sbin/*
rm -r $(pwd)/rootfs/usr/share/*
mv $(pwd)/rootfs/usr/lib/arm-linux-gnueabihf/libEGL.so.1.0.0 $(pwd)/rootfs/usr/lib/arm-linux-gnueabihf/libEGL.so.1.0.0_backup
mv $(pwd)/rootfs/usr/lib/arm-linux-gnueabihf/libGLESv2.so.2.0.0 $(pwd)/rootfs/usr/lib/arm-linux-gnueabihf/libGLESv2.so.2.0.0_backup
cd $(pwd)/rootfs/opt/vc/lib
ln -s libEGL.so libEGL.so.1.0.0
ln -s libGLESv2.so libGLESv2.so.2.0.0
ln -s libbrcmEGL.so libEGL.so
ln -s libbrcmGLESv2.so libGLESv2.so
ln -s libEGL.so libEGL.so.1
ln -s libGLESv2.so libGLESv2.so.2
cd $current

tar -czvf rootfs.tar.gz ./rootfs
