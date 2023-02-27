cd C:\Jenkins\Slave\Test





setlocal EnableDelayedExpansion

set status_conf=CONFLICTING
set status_mergeable=MERGEABLE


set cmd='C:\Jenkins\Slave\Test','C:\Jenkins\Slave\Test\Test101'
rem set cmd= '%cd:C:\Jenkins\Slave\Test %cd:C:\Jenkins\Slave\Test\Test101'

for /F  %%a in ("%cmd%") do (
set branchname=%%a
echo !branchname!
)


FOR %%a in (%cmd%) do echo %%a


