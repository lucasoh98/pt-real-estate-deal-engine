$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

$kafkaVersion = "3.9.0"
$scalaVersion = "2.13"
$kafkaFolderName = "kafka_${scalaVersion}-${kafkaVersion}"
$kafkaRoot = Join-Path $repoRoot "tools\kafka"
$kafkaHome = Join-Path $kafkaRoot $kafkaFolderName
$archiveName = "$kafkaFolderName.tgz"
$archivePath = Join-Path $kafkaRoot $archiveName
$downloadUrl = "https://downloads.apache.org/kafka/$kafkaVersion/$archiveName"

if (Test-Path $kafkaHome) {
    Write-Host "Kafka already present: $kafkaHome"
    exit 0
}

New-Item -ItemType Directory -Force -Path $kafkaRoot | Out-Null

Write-Host "Downloading Kafka $kafkaVersion..."
Invoke-WebRequest -Uri $downloadUrl -OutFile $archivePath

Write-Host "Extracting Kafka..."
tar -xf $archivePath -C $kafkaRoot

Write-Host "Kafka ready: $kafkaHome"
