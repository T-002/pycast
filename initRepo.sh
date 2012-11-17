#!/bin/bash

make clean
make html
make latexpdf
nosetests -c nose.cfg
