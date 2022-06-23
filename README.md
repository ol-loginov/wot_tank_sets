# Mod configuration

## Change set icons

You may put PNG file named "1.png" in "WoT Installation/mods/config/com.github.ol_loginov.wot_tank_sets", and this icon will be used
for set 1. The same is valid for other sets (just use "2.png", "3.png", etc)

# Assembly

## wot-tank-filter

Thanks for https://github.com/StranikS-Scan/WorldOfTanks-Decompiled

How-To Steps

1) Develop with PyCharm PY-145.597.11
2) Clone this git in "[WOT]/res_mods/[WOT Version]"
3) Unpack pycharm-debug.egg in "[WOT]/res_mods/[WOT Version]/scripts/common/pydev/pycharm/pydev" and compile folder with Python 2.7

4) Clone "StranikS-Scan/WorldOfTanks-Decompiled" in some folder (let's name it [WOT-Decompiled])
5) Create empty PyCharm project. Add "[WOT]/res_mods/[WOT Version]" as new content root to it, and "[WOT-Decompiled]" either


## mod settings api

https://wiki.wargaming.net/ru/ModsettingsAPI
https://bitbucket.org/IzeBerg/modssettingsapi

## mods list

https://gitlab.com/wot-public-mods/mods-list

## get tankopedia

items_cache = dependency.descriptor(IItemsCache)
items_cache.items.getVehicleDossiersIterator()
