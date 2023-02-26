set file=test\test.txt

setlocal EnableDelayedExpansion

set "cmd=type !file! | find /c /v """
for /f %%a in ('!cmd!') do set number=%%a
echo %number%

set "cmd=git log -n 1 --pretty=format:%%H -- !file!"
for /f %%a in ('!cmd!') do set id=%%a
echo %id%

set "cmd=git log -n 1 --pretty=format:%%H "
for /f %%a in ('!cmd!') do set id2=%%a
echo %id2%

set "cmd=git log -n 1 --pretty=format:%%h "
for /f %%a in ('!cmd!') do set id3=%%a
echo %id3%


if %id% == %id2% (
gh issue create --title "The test.txt has been changed-%id3%" --body "https://github.com/DevIssaAb/Test101/blob/%ID2%/test/test.txt#L1-L%number%"

)
