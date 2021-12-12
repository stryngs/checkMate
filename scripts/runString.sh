#!/bin/bash
rm -rf tmpDir; rm -rf artifacts; rm -rf DEBUG; mkdir DEBUG; for i in *.sh; do bash "$i"; done
