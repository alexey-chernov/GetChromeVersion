rem Запуск прихованої деінсталяції Google Chrome
"C:\Program Files\Google\Chrome\Application\%1\Installer\setup.exe" --uninstall --channel=stable --system-level --verbose-logging --force-uninstall

rem Видаляємо каталог C:\Program Files (x86)\Google
rd /S /Q "C:\Program Files (x86)\Google"