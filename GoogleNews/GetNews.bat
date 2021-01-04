@ECHO OFF
TITLE UNI Modify Sys1 and Sys2
COLOR 7C




	IF EXIST ScriptLog.log (
		del ScriptLog.log
		)
	for %%i in (run.py) do (
		echo Executing %%i
		py %%i >> ScriptLog.log 
	)
)
:EXIT1
@echo off
pause