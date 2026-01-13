@echo off
setlocal enableextensions enabledelayedexpansion
TITLE Kafka Ecosystem Stopper

set SCRIPT_DIR=%~dp0
set REPO_ROOT=%SCRIPT_DIR%..
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
    pause
    exit /b 1
)

echo A encerrar Kafka Broker...
call "%KAFKA_HOME%\bin\windows\kafka-server-stop.bat"

echo A encerrar Zookeeper...
call "%KAFKA_HOME%\bin\windows\zookeeper-server-stop.bat"

echo.
echo ======================================================
echo   Kafka Encerrado
echo ======================================================
pause
