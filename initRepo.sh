#!/bin/bash

echo "Removing old documentation"
make clean > /dev/null 2> /dev/null

echo "Building HTML documentation"
make html  > /dev/null 2> /dev/null

echo "Building LaTeX documentation"
make latexpdf > /dev/null 2> /dev/null

echo "Executing tests..."
nosetests -c nose.cfg
