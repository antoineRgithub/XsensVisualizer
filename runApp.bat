@echo off
echo Welcome !
echo Updating pip...


rem Test with "python"
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_COMMAND=python
) else (
    
    rem Test with "py"
    where py >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_COMMAND=py
    ) else (
        
        rem Test with "python3"
        python3 --version >nul 2>&1
        if %errorlevel% equ 0 (
            set PYTHON_COMMAND=python3
        ) else (
            echo Aucune installation de Python trouvee.
        )
    )
)

%PYTHON_COMMAND% -m pip install --upgrade pip
echo Installing required packages...
%PYTHON_COMMAND% -m pip install -r requirements.txt
echo Packages installed.


:::                 (                           )
:::          ) )( (                           ( ) )( (
:::       ( ( ( )  ) )                     ( (   (  ) )(
:::      ) )     ,,\\\                     ///,,       ) (
:::   (  ((    (\\\\//                     \\////)      )
:::    ) )    (-(__//                       \\__)-)     (
:::   (((   ((-(__||                         ||__)-))    ) )
:::  ) )   ((-(-(_||           ```\__        ||_)-)-))   ((
:::  ((   ((-(-(/(/\\        ''; 9.- `      //\)\)-)-))    )
:::   )   (-(-(/(/(/\\      '';;;;-\~      //\)\)\)-)-)   (   )
:::(  (   ((-(-(/(/(/\======,:;:;:;:,======/\)\)\)-)-))   )
:::    )  '(((-(/(/(/(//////:%%%%%%%:\\\\\\)\)\)\)-)))`  ( (
:::   ((   '((-(/(/(/('uuuu:WWWWWWWWW:uuuu`)\)\)\)-))`    )
:::     ))  '((-(/(/(/('|||:wwwwwwwww:|||')\)\)\)-))`    ((
:::  (   ((   '((((/(/('uuu:WWWWWWWWW:uuu`)\)\))))`     ))
:::        ))   '':::UUUUUU:wwwwwwwww:UUUUUU:::``     ((   )
:::          ((      '''''''\uuuuuuuu/``````         ))
:::           ))            `JJJJJJJJJ`           ((
:::             ((            LLLLLLLLLLL         ))
:::               ))         ///|||||||\\\       ((
:::                 ))      (/(/(/(^)\)\)\)       ((
:::                  ((                           ))
:::                    ((                       ((
:::                      ( )( ))( ( ( ) )( ) (()


for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
echo Running...
py .\appshiny.py
pause
