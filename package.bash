#!/usr/bin/env bash
################################################################################
# help create distribution for daily.
################################################################################

version="$(grep Version DEBIAN/control | awk '{print $2}')"
pkgname="daily_$version"

# Make man pages
cd docs/man
make
cd - > /dev/null

if [ "$1" == "python3" ]
then
    python3 setup.py bdist_wheel
elif [ "$1" == "deb" ]
then
    export DEBBUILD=1
    pybuild --build
    pybuild --install
    mkdir $pkgname
    cp -r debian/tmp/* $pkgname
    cp -r DEBIAN $pkgname
    dpkg-deb --build ./$pkgname
elif [ "$1" == "rpm" ]
then
    python3 setup.py bdist_rpm \
        --release 1 \
        --group Applications/Productivity \
        --requires "python3 python3-argcomplete python3-PrettyTable>=0.7.2 python3-PrettyTable<1.0 python3-dateparser python3-dateutil" \

#        --build-requires "python3-devel python3-argcomplete python3-docutils"

elif [ "$1" == "gz" ]
then
    python3 setup.py bdist --format=gztar
elif [ "$1" == "clean" ]
then
    rm -rf .pybuild *.deb daily_*/ dist/ *.egg-info build/ debian/ *.rpm
    cd docs/man
    make clean
    exit 0
else
    echo "Did nothing"
fi
