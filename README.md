# ThermalHMD
Designing thermal HMD project

1. [Example](#Hardware)
2. [Example2](#example2)
3. [Third Example](#third-example)




## Hardware



### Single Board Computer

Raspberry pi 4B



### Display
![image](https://github.com/doyounyu/ThermalHMD/assets/103356310/fec750ca-0163-45fe-b5d3-f3b2fcc3efa9)

 FLCOS Micro display module

https://ko.aliexpress.com/item/1005003368754176.html?spm=a2g0o.order_list.order_list_main.10.65921802Ic7Kpc&gatewayAdapt=glo2kor



| Parameter    | Specification      |
| ------------ | ------------------ |
| pixel        | 960x540            |
| aspect ratio | 16:9               |
| video format | Composite(AV+ AV-) |
| VIN          | 5V                 |





#### Rest of the specifications



#### Pinmap

| Color  | Purpose     |
| ------ | ----------- |
| Orange | AV+         |
| White  | AV-         |
| Blue   | Brightness+ |
| Green  | Brightness- |
| Yellow | Empty       |
| Black  | GND         |
| Red    | 3.6-5V      |



### Thermal Camera

Milessey TR256i



## Software

- **2023-05-03-raspios-bullseye-armhf-full.img  !Important!**
- opencv-python





## 1. RPi - Display Connection: Hardware Setting

1. Get a TRRS 3.5mm jack and strip the wire of it.
2. connect the sleeve(the most far part from the tip) with the AV+, and second far part to the AV-.
3. connect 5V+ and GND to the raspberry pi's 5V power supply.

![image](https://github.com/doyounyu/ThermalHMD/assets/103356310/3a0b8037-585f-4820-aea4-866614bb43d9)


RPi 3.5mm Composite output pinmap

<img src="https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png" style="zoom: 10%;" />



## 2. RPi - Display Connection: BIOS Setting

1. Go to `config.txt` file inside the boot folder either by connecting sd card with os image on to the pc, or by  directly modifying`config.txt` by `sudo nano /boot/config.txt`.

2. add following parameters:

   ```bash
   enable_tvout=1 #enables composite output through 3.5mm audio jack
   sdtv_mode=2    #enables "Normal PAL" for the composite output
   sdtv_aspect=3  #defines aspect ratio of 16:9
   ```

   check the link below to see what other option can be made, but other `sdtv_mode`, such as 0 or 1 shows terrible video output.

https://www.raspberrypi.com/documentation/computers/legacy_config_txt.html#sdtv_mode

3. Save and reboot the RPi.
Note: You better connect your debug monitor first after you flash the OS, unless RPi will set the FLCOS as your default monitor setting.
   
## 3. OpenCV installation

python version: 3.9.2

followed procedure from:
https://raspberrypi-guide.github.io/programming/install-opencv


```bash
sudo apt-get update
sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
pip install opencv-python==4.5.3.56
pip install numpy==1.20.0

```


## Troubleshooting

https://stackoverflow.com/questions/33859531/runtimeerror-module-compiled-against-api-version-a-but-this-version-of-numpy-is


### ImportError: numpy.core.multiarray failed to import

```bash
RuntimeError: module compiled against API version 0xe but this version of numpy is 0xd
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/doyounyu/.local/lib/python3.9/site-packages/cv2/__init__.py", line 5, in <module>
    from .cv2 import *
ImportError: numpy.core.multiarray failed to import

```

`pip install numpy --upgrade` might work, but sometimes version new numpy might incompatable with the opencv. to figure out, you need to focus on the `RuntimeError`:
RuntimeError: module compiled against API version **0xe** but this version of numpy is **0xd**


so you need **0xe** version of numpy. but what is **0xe** version?


https://github.com/numpy/numpy/blob/maintenance/1.26.x/numpy/core/setup_common.py#L35-L51
check for the table below:

| Color| Purpose|
|------|--------|
| 0x8  | 1.7.x  |  
| 0x9  | 1.8.x  |
| 0x9  | 1.9.x  |
| 0xa  | 1.10.x |
| 0xa  | 1.11.x |
| 0xa  | 1.12.x |
| 0xb  | 1.13.x |
| 0xc  | 1.14.x |
| 0xc  | 1.15.x |
| 0xd  | 1.16.x |
| 0xd  | 1.19.x |
| 0xe  | 1.20.x |
| 0xe  | 1.21.x |
| 0xf  | 1.22.x |
| 0x10 | 1.23.x |
| 0x10 | 1.24.x |
| 0x11 | 1.25.x |

thus you need to install 0xe version, which is either 1.20 or 1.21 by `pip install numpy==1.20`.
