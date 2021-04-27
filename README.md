# wot-tank-filter

Thanks for https://github.com/StranikS-Scan/WorldOfTanks-Decompiled 
:)

Debugging?

1) Search for preferences.xml in Local/Roaming/Wargaming.net/WorldOfTanks
2) Add node 'scriptsPreferences/development/pydevd' with text:

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

```