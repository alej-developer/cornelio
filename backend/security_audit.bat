@echo off
echo ========================================================
echo   Cornelio - Automated Security Audit (Bandit)
echo ========================================================

echo.
echo [1] Running Bandit SAST analyzer on /app...
bandit -r app/ -c "pyproject.toml" -f screen -ll

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Vulnerabilidades encontradas. Por favor revisa el reporte anterior.
    exit /b %errorlevel%
)

echo.
echo [OK] Auditoria de seguridad completada. No se encontraron vulnerabilidades de severidad alta/media.
exit /b 0
