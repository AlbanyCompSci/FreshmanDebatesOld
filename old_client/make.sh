#!/usr/bin/env bash

for f in `ls js/*.jsx`
do
    new=`echo f | sed 's/\..*//'`.js
    jsx $f > "js/$new"
done
