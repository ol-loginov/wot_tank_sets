Mod page on wgmods.net: https://wgmods.net/7161/


# Mod configuration

## Change set icons

You may put PNG file named "1.png" in "[WoT Installation]/mods/configs/com.github.ol_loginov.wot_tank_sets", and this icon will be used
for set 1. The same is valid for other sets (just use "2.png", "3.png", etc)

## XVM compatibility

This mod cannot run with XVM carousel installed. But there is a way to disable XVM carousel to get this mod working.
Here are details: https://github.com/ol-loginov/wot_tank_sets/issues/2#issuecomment-1493420544


# Assembly

Thanks for https://github.com/StranikS-Scan/WorldOfTanks-Decompiled

How-To Steps

1) Develop with PyCharm PY-145.597.11
2) Clone this git in "[WOT]/res_mods/[WOT Version]"
3) Unpack pycharm-debug.egg in "[WOT]/res_mods/[WOT Version]/scripts/common/pydev/pycharm/pydev" and compile folder with Python 2.7

4) Clone "StranikS-Scan/WorldOfTanks-Decompiled" in some folder (let's name it [WOT-Decompiled])
5) Create empty PyCharm project. Add "[WOT]/res_mods/[WOT Version]" as new content root to it, and "[WOT-Decompiled]" either


## mod settings api

* https://wiki.wargaming.net/ru/ModsettingsAPI
* https://bitbucket.org/IzeBerg/modssettingsapi

## mods list

https://gitlab.com/wot-public-mods/mods-list

## Icons

To create icons the following commands is used:

```shell
convert -size 32x17 xc:none -fill white -font "SF-Pro-Bold" -pointsize 12 -gravity center -draw "text 1,0 '1'" 1.png
```


## 2.0

Карусель теперь в react.
python классы, отвечающие за критерии - хз где используются.
Фильтровать можно прямо в gameface. Однако плохо выглядит при двойной карусели. Перетаскивать элементы наверное можно, но чревато...

```html
<div class="Information_details_e5340a0c"><div class="VehicleLevel_3c938122 Information_text_7b2995dc Information_text__level_e5a9014e" data-name="VehicleLevel">III</div><div class="VehicleType_30b4aab0 VehicleType_base__x24x24_a3dc7aa3" style="background-image: url(img://gui/maps/icons/ui_kit/vehicle_type/x24x24/light_tank_x24x24.png); background-repeat: no-repeat no-repeat; background-size: contain; background-position-x: 50.000000%; background-position-y: 50.000000%; " src="img://gui/maps/icons/ui_kit/vehicle_type/x24x24/light_tank_x24x24.png"></div></div>
```

Вот тут, в `.Information_details_e5340a0c` лежит `tag.__reactFiber$nfjywfmtamm.return.memoizedProps.vehicle`