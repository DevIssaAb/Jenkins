setlocal EnableDelayedExpansion
set "cmd=type test.txt | find /c /v """
for /f %%a in ('!cmd!') do set number=%%a
echo %number%

set "cmd=git log -n 1 --pretty=format:%%H -- test.txt"
for /f %%a in ('!cmd!') do set id=%%a
echo %id%

set "cmd=git log -n 1 --pretty=format:%%H "
for /f %%a in ('!cmd!') do set id2=%%a
echo %id2%
