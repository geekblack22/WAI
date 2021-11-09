#!/usr/bin/sh

for f in *.py; do
	sed -i 's/    /\t/g' $f
done

