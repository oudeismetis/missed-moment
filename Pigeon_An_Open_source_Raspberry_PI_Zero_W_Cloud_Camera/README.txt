                   .:                     :,                                          
,:::::::: ::`      :::                   :::                                          
,:::::::: ::`      :::                   :::                                          
.,,:::,,, ::`.:,   ... .. .:,     .:. ..`... ..`   ..   .:,    .. ::  .::,     .:,`   
   ,::    :::::::  ::, :::::::  `:::::::.,:: :::  ::: .::::::  ::::: ::::::  .::::::  
   ,::    :::::::: ::, :::::::: ::::::::.,:: :::  ::: :::,:::, ::::: ::::::, :::::::: 
   ,::    :::  ::: ::, :::  :::`::.  :::.,::  ::,`::`:::   ::: :::  `::,`   :::   ::: 
   ,::    ::.  ::: ::, ::`  :::.::    ::.,::  :::::: ::::::::: ::`   :::::: ::::::::: 
   ,::    ::.  ::: ::, ::`  :::.::    ::.,::  .::::: ::::::::: ::`    ::::::::::::::: 
   ,::    ::.  ::: ::, ::`  ::: ::: `:::.,::   ::::  :::`  ,,, ::`  .::  :::.::.  ,,, 
   ,::    ::.  ::: ::, ::`  ::: ::::::::.,::   ::::   :::::::` ::`   ::::::: :::::::. 
   ,::    ::.  ::: ::, ::`  :::  :::::::`,::    ::.    :::::`  ::`   ::::::   :::::.  
                                ::,  ,::                               ``             
                                ::::::::                                              
                                 ::::::                                               
                                  `,,`


https://www.thingiverse.com/thing:2230707
Pigeon: An Open source Raspberry PI Zero W Cloud Camera by geraldoramos is licensed under the Creative Commons - Attribution license.
http://creativecommons.org/licenses/by/3.0/

# Summary

<p></p><p align="center"><img src="https://s3-us-west-1.amazonaws.com/allge.us/logo_pigeon.svg" alt="Logo" width="350px"/></p>
<p></p><p></p>
![Example](https://s3-us-west-1.amazonaws.com/allge.us/pigif.gif)

**Pigeon** is a simple cloud home surveillance camera project that uses the new Raspberry Pi Zero W single board computer ($10). It uses a custom designed 3D printed enclosure that fits the board and the camera. A wall mount is also included.

The goal of this project is to provide an easy way to setup a basic (yet functional) cloud camera at a very low cost (~$20 total). The software includes features like motion detection and Dropbox integration.

**Requirements**
* A Rasberry Pi Zero W running Raspbian and connected to the internet. The regular (no-wifi) Raspberry PI Zero also works, but will require a usb wifi doongle that will stay out of the designed enclosure: [Buy a Raspberry PI Zero W][829f44e8]
* A Raspberry Pi camera with cable: [Buy it][09e7e3d1]
* (optional) A long micro-usb power cable: [Buy it](https://www.aliexpress.com/item/1-2-3-5m-10ft-90-degree-Angle-Long-Micro-USB-Cable-20cm-Sync-data-Charging/32794612542.html?spm=2114.01010208.3.12.Xj3wx5&ws_ab_test=searchweb0_0,searchweb201602_4_10065_10130_10068_10136_10137_10138_10060_10062_10141_10056_10055_10054_10059_10099_129_10103_10102_10096_10148_10052_10053_10050_10107_10142_10051_10143_10084_10083_10119_10080_10082_10081_10110_10111_10112_10113_10114_10037_10032_10078_10079_10077_10073_10070_10123_10120_10124-10120,searchweb201603_6,afswitch_1_afChannel,ppcSwitch_7,single_sort_0_default&btsid=fc05fbd8-0d8a-47c8-b643-02df18983f6f&algo_expid=bb5c67b9-9680-48f5-8c33-d24c88072ce4-1&algo_pvid=bb5c67b9-9680-48f5-8c33-d24c88072ce4)
  [09e7e3d1]: https://www.aliexpress.com/item/New-Arrival-Raspberry-Pi-Zero-Camera-5MP-RPI-Zero-Camera-Module-Webcam-for-Raspberry-Pi-Zero/32785811007.html?spm=2114.01010208.3.12.clLgGm&ws_ab_test=searchweb0_0,searchweb201602_4_10065_10130_10068_10136_10137_10138_10060_10062_10141_10056_10055_10054_10059_10099_129_10103_10102_10096_10148_10147_10052_10053_10050_10107_10142_10051_10143_10084_10083_10119_10080_10082_10081_10110_10111_10112_10113_10114_10037_10032_10078_10079_10077_10073_10070_10123_10120_10124-10120,searchweb201603_6,afswitch_1_afChannel,ppcSwitch_7,single_sort_0_default&btsid=71405a16-56ea-4466-a92f-cae0d046ea2e&algo_expid=6607631f-0fea-4dff-8fec-95a907b45e65-1&algo_pvid=6607631f-0fea-4dff-8fec-95a907b45e65
  [2c44525c]: https://www.raspberrypi.org/blog/raspberry-pi-zero-w-joins-family/ "Info"
  [829f44e8]: https://www.raspberrypi.org/blog/raspberry-pi-zero-w-joins-family/ "Info"
* [M1.7x6mm](https://www.amazon.com/uxcell-M1-7x6mm-Thread-Nickel-Tapping/dp/B01FXMJ34S/ref=sr_1_3?ie=UTF8&qid=1497483322&sr=8-3&keywords=m1.7+screw) Thread Self Tapping Screws for the case lid
* Head Combo [Machine Screw with Nut](https://www.amazon.com/Hillman-Group-7656-Machine-6-32-Inch/dp/B000B8LOWE/ref=sr_1_fkmr0_2?s=hi&ie=UTF8&qid=1497655005&sr=1-2-fkmr0&keywords=BOLT+STOVE+COMBO+RD+6-32X1IN), 6-32-Inch x 1-Inch for the adjustable support
* M3*6 [screws](https://www.amazon.com/100pcs-Screw-Coupler-Bracket-Chassis/dp/B00M418I6G/ref=sr_1_2?s=hi&ie=UTF8&qid=1497655314&sr=1-2&keywords=M36+screws) for the adjustable support link with the wall mount.

For software installation instructions please check the [Github](http://github.com/geraldoramos/pigeon) repository

Also available on [Instructables](https://www.instructables.com/id/Pigeon-a-3D-Printed-Cloud-Home-Surveillance-Camera/)

Assembling is pretty straight forward, please use the comments if you have any questions. I apologize for the confusing screw/bolt selections for this project.



# Print Settings

Printer: Qidi Tech 1
Rafts: No
Supports: No
Resolution: 0.2
Infill: 20%