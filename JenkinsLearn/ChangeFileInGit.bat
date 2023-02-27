set file=test\a_b\create_strategy.cpp

setlocal EnableDelayedExpansion


rem Get ID last commit when create_strategy.cpp changed.
set "cmd=git log -n 1 --pretty=format:%%H -- !file!"
for /f %%a in ('!cmd!') do set id=%%a
echo %id%

rem Get ID last commit.
set "cmd=git log -n 1 --pretty=format:%%H "
for /f %%a in ('!cmd!') do set id2=%%a
echo %id2%

rem Get a small id for the last commit.
set "cmd=git log -n 1 --pretty=format:%%h "
for /f %%a in ('!cmd!') do set id3=%%a
echo %id3%

rem Create an issue if the file changes in the last commit.
if %id% == %id2% (

rem Get number of line to show all a file when creating an issue
set "cmd=type !file! | find /c /v """
for /f %%a in ('!cmd!') do set number=%%a
echo !number!

rem you need install GitHub CLI 
gh issue create --title "The test.txt has been changed-%id3%" --body "https://github.com/DevIssaAb/Test101/blob/%id2%/test/a_b/create_strategy.cpp#L1-L!number!" -a DevIssaAb --project "Work @ DevIssaAb"

)
rem BUILD_NUMBER=%BUILD_NUMBER% inn Jenkins.
echo CommitFileID=%id%;CurentCommitID=%id2%;BUILD_NUMBER=%BUILD_NUMBER%>>CommitHistory.log