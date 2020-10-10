#!/bin/bash
files=($(ufs ls | tr ' ' '\n'))
for i in "${files[@]}"
do
   ufs rm $i
done