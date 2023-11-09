# ThermalHMD
Designing thermal HMD project





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

```bash
doyounyu1@raspberrypi:~ $ pip install --upgrade pip
doyounyu1@raspberrypi:~ $ pip install opencv-python==4.5.3.56
```
