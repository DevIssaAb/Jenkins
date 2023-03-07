if %ReleaseNewVersion% == false (
echo A new version has not been updated
exit 0
)

setlocal EnableDelayedExpansion

set status_conf=CONFLICTING
set status_mergeable=MERGEABLE
set mergeable=null

REM Split branch parameter by / delimiter (remote/branch) for pushing to git (other Jenkins plugins to publish on Git did not work!)
for /F "tokens=1,2 delims=/" %%a in (^"%Branch:"=.%^") do (
set branchname=%%b
)
set /p BUILD=<C:\Jenkins\Slave\Workspace\FullBuilder\version.log

rem set first branch
set head_branch=%branchname%_v%BUILD%

set paths=C:\Jenkins\Slave\Workspace\FullBuilder,C:\Jenkins\Slave\Workspace\FullBuilder\scripts\system
FOR %%a in (%paths%) do  (
cd %%a

rem get mergeable the PR for brqancch !head_branch!
set "cmd=gh pr list -H !head_branch! --json mergeStateStatus,number,mergeable --jq .[].mergeable"
FOR /f %%b in ('!cmd!') do set mergeable=%%b

rem get number the PR for brqancch !head_branch!
set "cmd=gh pr list -H !head_branch! --json mergeStateStatus,number,mergeable --jq .[].number"
FOR /f %%c in ('!cmd!') do set number=%%c

echo !mergeable!
echo !head_branch!

if !mergeable! == %status_conf% (

echo the  branch !head_branch! can't merge.

rem create an issue
gh issue create --title "The PR can't merge for branch !head_branch!" --body "PR #!number!" -a CPP-Team-Ltd -p "Work @ CPP Team"
)

if !mergeable! == %status_mergeable% (

rem merge PR #!number! and delete the branch !head_branch!
gh pr merge !number! -m 
git push --delete origin !head_branch!
echo !number!
echo !head_branch!
)

if !mergeable! == null (
echo delete !head_branch!
git push --delete origin !head_branch!

)

rem set next breanch
set head_branch=main_v%BUILD%

rem it is possible that the branch is deleted
set mergeable=null
)