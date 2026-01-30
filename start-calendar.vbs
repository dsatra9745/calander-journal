Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Change to script directory
WshShell.CurrentDirectory = scriptDir

' Start Flask backend (hidden)
WshShell.Run "python ai_helper.py", 0, False

' Wait 3 seconds for Flask to start
WScript.Sleep 3000

' Start frontend server (hidden)
WshShell.Run "python -m http.server 8000", 0, False

' Wait 2 seconds for frontend to start
WScript.Sleep 2000

' Open browser
WshShell.Run "http://localhost:8000/calendar2nd.html", 1, False
