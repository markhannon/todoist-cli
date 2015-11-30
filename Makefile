install:
	-pip install todoist
	-pip install pacparser
	-mkdir ${HOME}/Library/Scripts/Applications/Outlook
	-install -c osx/OutlookToTodist.osascript ${HOME}/Library/Scripts/Applications/Outlook
	-mkdir ${HOME}/Library/Scripts/Applications/Todoist
	-install -c src/todoist-add.py ${HOME}/Library/Scripts/Applications/Todoist
