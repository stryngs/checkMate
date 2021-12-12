#!/bin/bash

## Set the initial status to null
status=""

## Set the V-ID
vID=$(echo $0 | cut -d. -f1)

## Create parent dirs
mkdir artifacts 2>/dev/null
mkdir tmpDir 2>/dev/null
mkdir DEBUG 2>/dev/null

## Create log vars
artifacts=artifacts/"$vID"
eLog=artifacts/"$vID"_errorLog
eMain=artifacts/errorLog
rm -rf "$artifacts"
rm -rf "$eLog"

## Create V-ID temporary dir
tmpDir=tmpDir/"$vID"_tmp
tmp="$tmpDir"/tmp
rm -rf "$tmpDir"
mkdir "$tmpDir"

## Create var for error logging
errors="$tmpDir"/errors

## Create Final Log for parsing
log=artifacts/finalResults
fResults="$tmpDir"/findResults
