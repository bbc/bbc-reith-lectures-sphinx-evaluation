#!/bin/bash

mkdir -p build
cd build
echo "Downloading SphinxBase source from trunk (>= 0.7) and building/installing in /usr/local..."
wget "http://cmusphinx.svn.sourceforge.net/viewvc/cmusphinx/trunk/sphinxbase/?view=tar" -O sphinxbase.tar
tar xvf sphinxbase.tar
cd sphinxbase
./autogen.sh
./autogen.sh && ./configure && make && sudo make install

if [ "$?" -ne "0" ]; then
    echo "Sorry, cannot build sphinxbase"
    exit 1
fi

cd ..
echo "Downloading Sphinx3 source from trunk (>= 0.8) and building/installing in /usr/local..."
wget "http://cmusphinx.svn.sourceforge.net/viewvc/cmusphinx/trunk/sphinx3/?view=tar" -O sphinx3.tar
tar xvf sphinx3.tar
cd sphinx3
./autogen.sh
./autogen.sh && ./configure && make && sudo make install

if [ "$?" -ne "0" ]; then
    echo "Sorry, cannot build sphinx3"
    exit 1
fi

cd python
sudo python setup.py install

if [ "$?" -ne "0" ]; then
    echo "Sorry, cannot build sphinx3 python bindings"
    exit 1
fi
