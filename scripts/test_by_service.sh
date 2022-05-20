#!/bin/bash
for d in ./services/* ; do
  if [ ! -d "$d" ]; then
    continue
  fi

  for f in $d/functions/* ; do
    if [ ! -d "$f" ]; then
      continue
    fi

    cd $f


    ## Run test by service
    python -m pytest -v

    if [ $? -eq 1 ]; then
        exit 1
    fi

    cd -
  done

done