#!/bin/bash

mkdir -p './artifacts'

for d in ./services/* ; do
  if [ ! -d "$d" ]; then
    continue
  fi

  for f in $d/functions/* ; do
    if [ ! -d "$f" ]; then
      continue
    fi

    zip_name="${d##*/}-service_${f##*/}"

    zip -jr ./artifacts/$zip_name.zip $f/main.py
    # pip freeze > $f/requirements.txt
    # pip install -r $f/requirements.txt -t ./package
    # zip -jr ./artifacts/$zip_name.zip $f/package
    input=$f/requirements.txt
    while IFS= read -r line
    do
      pip install --target ./package $line
    done < "$input"

    zip -jr ./artifacts/$zip_name.zip $f/package

    printf '@ main.py\n@=lambda_function.py\n' | zipnote -w ./artifacts/$zip_name.zip
  done
done