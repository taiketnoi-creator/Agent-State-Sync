@echo off
chcp 65001 >nul
python "%~dp0cleanup_old_media.py" --days 7
