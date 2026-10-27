#!/bin/sh
# Packages the home folder into an unsigned Tizen widget (dist/RefabHome.wgt), for macOS and Linux.
# Apps2Samsung signs it with your Samsung certificate when it installs it.
set -e
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/RefabHome.wgt
(cd home && zip -qr -X ../dist/RefabHome.wgt . -x '.*' -x '*/.*')
unzip -l dist/RefabHome.wgt | tail -1
echo "built dist/RefabHome.wgt"
