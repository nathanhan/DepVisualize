#!/bin/bash -eu

PREFIX=$1
> $PREFIX-binary-packages-full.txt
> $PREFIX-binary-packages-short.txt
> $PREFIX-source-packages-full.txt
> $PREFIX-source-packages-short.txt

while read -r nevra; do
  [[ "$nevra" == *.src || "$nevra" == *.nosrc ]] && type_="source" || type_="binary"
  name=${nevra%-*-*}
  echo "$nevra" >> $PREFIX-$type_-packages-full.txt
  echo "$name" >> $PREFIX-$type_-packages-short.txt
done

export LC_ALL=C
for f in $PREFIX-{binary,source}-packages-{full,short}.txt; do
  sort -u $f -o $f
done