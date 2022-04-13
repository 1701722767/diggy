#!/bin/bash

mkdir -p './artifacts/layers'

while read -r package; do
    echo "Creating layer for $package"

    mkdir -p ./python
    pip3 install --target=./python $package

    zip_name="${package}_layer"
    zip -r $zip_name.zip ./python
    mv $zip_name.zip './artifacts/layers'

    rm -r ./python

done < ./services/requirements.txt