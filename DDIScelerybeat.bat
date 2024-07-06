@echo off
rem if "%1"=="h" goto begin
rem start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
cd /d C:\djangoproject\Reliability_Row_data
del celerybeat.pid
c:\Python372\mecheck\Scripts\celery.exe -A Reliability_Row_data beat -l info