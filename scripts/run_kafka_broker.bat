@echo off
TITLE Kafka Broker

if "%KAFKA_HOME%"=="" (
    echo [ERRO] KAFKA_HOME nao definido.
    exit /b 1
)

if "%ENV_PATH%"=="" (
    echo [ERRO] ENV_PATH nao definido.
    exit /b 1
)

if not exist "%ENV_PATH%\Library\bin\java.exe" (
    echo [ERRO] Java nao encontrado em "%ENV_PATH%\Library\bin\java.exe".
    exit /b 1
)

set PATH=%ENV_PATH%\Library\bin;%ENV_PATH%\Scripts;%PATH%
call "%KAFKA_HOME%\bin\windows\kafka-server-start.bat" "%KAFKA_HOME%\config\server.properties"
