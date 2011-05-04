#!/bin/bash
set -e
# Install PyPy
mkdir -p /home/hadoop/pypy
wget http://pypy.org/download/pypy-1.5-linux.tar.bz2
tar -C /home/hadoop/pypy -xjvf pypy-1.5-linux.tar.bz2
ln -s /home/hadoop/pypy/pypy-c-jit-43780-b590cf6de419-linux/bin/pypy /home/hadoop/bin/pypy
# Install MrJob
wget http://pypi.python.org/packages/source/m/mrjob/mrjob-0.2.5.tar.gz
tar xzvf mrjob-0.2.5.tar.gz
cd mrjob-0.2.5
/home/hadoop/bin/pypy setup.py install
