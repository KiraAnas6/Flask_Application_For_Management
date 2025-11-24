@echo off
setlocal enabledelayedexpansion
goto :main
:main 
for /l %%i in (1,1,5) do @(curl -L -O "https://elzerowebschool.github.io/HTML_And_CSS_Template_Four/imgs/course-0%%i.jpg")
endlocal 
