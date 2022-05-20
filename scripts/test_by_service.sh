#!/bin/bash

for d in ./services/* ; do
  if [ ! -d "$d" ]; then
    continue
  fi

  cd $d


  ## Run test by service
  python -m pytest -v

  if [ $? -ne 0 ]; then
      exit 1
  fi

  cd -

done