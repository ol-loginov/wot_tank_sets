# wot-tank-filter

Thanks for https://github.com/StranikS-Scan/WorldOfTanks-Decompiled 
:)

Debugging?

1) install pydecd-pycharm.egg in "<WOT>/res_mods/1.12.1.1/scripts/common/pydev/pycharm/pydev" and compile
2) make soft link from "<current folder>/target/wotmod/res/scripts/client/gui" to "<WOT>/res_mods/1.12.1.1/scripts/client/gui"

3) Search for preferences.xml in Local/Roaming/Wargaming.net/WorldOfTanks
4) Add node 'scriptsPreferences/development/pydevd' with text:

```xml
	<scriptsPreferences>
		<development>
			<pydevd>
				<port>5678</port>
				<suspend>True</suspend>
				<replacePath>
					<to>aloha</to>
					<from>aloha</from>
				</replacePath>
				<autoConnect>
					<client>True</client>
				</autoConnect>
			</pydevd>
		</development>
    </scriptsPreferences>
```