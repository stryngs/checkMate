#!/bin/bash
cd .. && rm -rf checkMate cmUpdate.tgz && python update.py && tar zxf cmUpdate.tgz && cd checkMate && bash runString.sh
