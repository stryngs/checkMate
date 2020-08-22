#!/bin/bash

## Rule Title:The Red Hat Enterprise Linux operating system must be blah.
## STIG ID:RHEL-00-000000
## Rule ID:SV-86473r4_rule
## Vuln ID:V-00000
## Severity:CAT I

## Preps
source lib/prep.sh
source lib/shared.sh
################################################################################

## Grab info
echo "Hello World" > "$fResults" 2>"$errors"
tVal=$(cat "$fResults")
eLen=$(wc -l "$errors" | awk '{print $1}')

## string compare
if [[ $tVal == "Hello World" ]]; then
  status="NotAFinding"
  oVal="Hello World string found"
else
  status="Open"
  oVal="Hello World string not found"
fi

## Cleanup
closeOut--
