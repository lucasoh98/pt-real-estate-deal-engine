@echo off
setlocal enableextensions enabledelayedexpansion
TITLE Kafka Ecosystem Starter

set SCRIPT_DIR=%~dp0
for %%I in ("%SCRIPT_DIR%..") do set REPO_ROOT=%%~fI
set ENV_PATH=%REPO_ROOT%\conda_env
set KAFKA_REAL_HOME=%REPO_ROOT%\tools\kafka\kafka_2.13-3.9.0

set KAFKA_HOME=%KAFKA_REAL_HOME%
set KAFKA_DRIVE=
for /f "tokens=1,2,*" %%A in ('subst') do (
    if /I "%%C"=="%KAFKA_REAL_HOME%" (
        set KAFKA_HOME=%%A
        set KAFKA_HOME=!KAFKA_HOME:~0,3!
        set KAFKA_DRIVE=!KAFKA_HOME!
    )
)

if "%KAFKA_DRIVE%"=="" (
    for %%D in (K L M N O P Q R S T U V W X Y Z) do (
        if not exist %%D\NUL (
            subst %%D "%KAFKA_REAL_HOME%" >nul 2>&1
            if !errorlevel!==0 (
                set KAFKA_DRIVE=%%D
                set KAFKA_HOME=!KAFKA_DRIVE!\
                goto :drive_done
            )
        )
    )
)
:drive_done

if not exist "%KAFKA_REAL_HOME%" (
    echo [ERRO] Kafka nao encontrado em "%KAFKA_REAL_HOME%".
    echo Execute antes: powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%download_kafka.ps1"
    pause
    exit /b 1
)

echo [1/3] A validar Java no ambiente...
if not exist "%ENV_PATH%\Library\bin\java.exe" (
    echo.
    echo [ERRO] Java nao encontrado em "%ENV_PATH%\Library\bin\java.exe".
    echo Verifique se o Java esta instalado no conda_env.
    pause
    exit /b 1
)

"%ENV_PATH%\Library\bin\java.exe" -version

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Nao foi possivel encontrar o conda ou o Java no ambiente.
    echo Verifique se o Anaconda/Miniconda esta no PATH do Windows.
    pause
    exit /b 1
)

echo.
echo [2/3] A iniciar Zookeeper...
start "zookeeper" /min cmd /k ""%SCRIPT_DIR%run_zookeeper.bat""

echo Aguardando 15 segundos para estabilizacao...
timeout /t 15 /nobreak > nul

echo [3/3] A iniciar Kafka Broker...
start "kafka-broker" /min cmd /k ""%SCRIPT_DIR%run_kafka_broker.bat""

echo.
echo ======================================================
echo   Kafka Ativo via Conda Run!
echo ======================================================
pause
