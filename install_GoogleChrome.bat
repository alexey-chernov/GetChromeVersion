IF EXIST "C:\Program Files (x86)\Google" ( 
	rd /S /Q "C:\Program Files (x86)\Google"
)

rem Запускаємо встановлення Google Chrome
google-chrome-126-0-6478-57.exe

rem Пауза в 10 сек
timeout /T 10

rem Перейменовуємо каталог GoogleUpdater в GoogleUpdater_bak для відключення автооновлення Google Chrome
ren "C:\Program Files (x86)\Google\GoogleUpdater\" GoogleUpdater_bak