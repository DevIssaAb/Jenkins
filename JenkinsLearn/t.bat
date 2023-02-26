git log -n 1 --pretty=format:%%H -- %cd%\JenkinsLearn\Note.txt>commit.txt
set /p ID=<commit.txt
echo %ID%