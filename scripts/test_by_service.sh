#!/bin/bash

for d in ./services/* ; do
  if [ ! -d "$d" ]; then
    continue
  fi

  cd $d


  ## Run test by service
  python -m pytest -v

  cd -

done