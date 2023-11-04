# ThermalHMD
Designing thermal HMD project

from: https://wiki.banana-pi.org/OpenCV_3.4x_on_BananaPi

## Prerequisite

```
apt-get update
apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler
apt-get install libgflags-dev libgoogle-glog-dev
liblmdb-dev
apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev v4l-utils libxvidcore-dev libx264-dev ffmpeg
apt-get install libgtk2.0-dev libatlas-base-dev gfortran python2.7-dev python3-dev checkinstall
```

```
git clone https://github.com/opencv/opencv.git --branch 3.4.0
git clone https://github.com/opencv/opencv_contrib.git --branch 3.4.0
```

```
cd <path>/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=Release  -D CMAKE_INSTALL_PREFIX=/usr/local -D PYTHON_INCLUDE_DIR=/usr/bin/python -D OPENCV_EXTRA_MODULES_PATH=<path>/opencv_contrib/modules ..
```


