# Cross Compile Qt for Raspberry PI

* Qt version - 5.12.10 lts
* Raspbian OS lite - Release date: January 11th 2021, Kernel version: 5.4

Tested on Ubuntu 20.04 and Debian 10.

Install QT and QT creator for linux - `https://www.qt.io/download-open-source` - If you already have a copy of Qt and Qt creator, skip.

## Setup

Download configure shell script file and set execute permissions to it.

```bash
wget https://github.com/akhilharihar/Cross-Compile-Qt-for-Raspberry-PI/releases/download/v1.0/configure
chmod +x ./configure
```

### Configuration

Open configure script file in your text editor and make changes in the variables section per your requirement.

* QtFLocation - QT Installation Directory - default - user home. 

* RPI_DEVICE -
  * RPI, RPI zero - `linux-rasp-pi-g++`
  * RPI 2 - `linux-rasp-pi2-g++`
  * RPI 3 - `linux-rasp-pi3-g++`

* SKIP_MODULES - Bash array type - Exclude module that you do not want to build. 
  * qtxmlpatterns
  * qtx11extras
  * qtwinextras
  * qtwebview
  * qtwebsockets
  * qtwebglplugin
  * qtwebengine
  * qtwebchannel
  * qtwayland
  * qtvirtualkeyboard
  * qttranslations
  * qttools
  * qtsvg
  * qtspeech
  * qtserialport
  * qtserialbus
  * qtsensors
  * qtscxml
  * qtscript - compile error. Is skipped by default.
  * qtremoteobjects
  * qtquickcontrols2
  * qtquickcontrols
  * qtpurchasing
  * qtnetworkauth
  * qtmultimedia
  * qtmacextras
  * qtlocation
  * qtimageformats
  * qtgraphicaleffects
  * qtgamepad
  * qtdoc
  * qtdeclarative
  * qtdatavis3d
  * qtconnectivity
  * qtcharts
  * qtcanvas3d
  * qtbase
  * qtandroidextras
  * qtactiveqt
  * qt3d

Ex: Below command will skip qtdoc, qtgamepad, qtspeech modules
```bash
---

SKIP_MODULES=(qtdoc qtgamepad qtspeech)
---
```

## Compile and Install

Create a new folder and source configure script in it.


```bash
mkdir qt_build && cd qt_build
source /path/to/configure

make -j $(nproc)
make install
```

Copy `sysroot` and `rpi_tools` folder to `$Qt_ROOT`
```bash
rsync -az sysroot $Qt_ROOT
rsync -az rpi_tools $Qt_ROOT
```

## Setting RPI to compile QT

Copy contents of `qt` in `$Qt_ROOT` to your RPI `/usr/local/qt5` folder.

```bash
rsync -az "$Qt_ROOT"qt/ root@raspberrypi_ip:/usr/local/qt5/
```
 
## Creating a Raspbian image with Qt binaries (Optional)

Mount rootfs partition in raspbian image.

```bash
mkdir ./temp_rpi_rootfs

sudo mount "$PWD"/2021-01-11-raspios-buster-armhf-lite.img -o loop,offset=$(( 512 * 532480 )) "$PWD"/temp_rpi_rootfs

sudo rsync -avz "$Qt_ROOT"qt/ "$PWD"/temp_rpi_rootfs/usr/local/qt5/

sudo umount "$PWD"/temp_rpi_rootfs && rmdir "$PWD"/temp_rpi_rootfs
```

## Setup QT creator to compile Qt Apps

Open options in Qt creator. Tools -> options.

### Devices Section

Click Add > Generic Linux Device > enter device name, username, ip address > deploy public key > Finish.

Name it as RPI.

### Kits Section

**Compilers**

In Compilers Tab, add GCC, G++ compilers with below paths.

C++ compiler path - `Qt_ROOT_directory/rpi_tools/bin/arm-linux-gnueabihf-g++`

C compiler path -  `Qt_ROOT_directory/rpi_tools/bin/arm-linux-gnueabihf-gcc`

Name them as RPI C++ and RPI C

**Qt**

In Qt Versions tab, click add and select qmake file in `Qt_ROOT_directory/qt_tools/bin`.

Name it as RPI Qt

**Device Kit**

In Kit tab, click add and select below options.

Device Type: Generic Linux Device

Device: RPI.

Sysroot: Qt_ROOT_directory/sysroot

Compiler: RPI C++, RPI C.

Qt version: RPI Qt.

Click Apply and Ok.


### Cleaning UP
You can now delete the qt_build directory that we've created initially.

```bash
rm -rf /path/to/qt_build
```