#!/bin/bash
for d in ./services/* ; do
  if [ ! -d "$d" ]; then
    continue
  fi

  cd $d

  rm -r ../.pytest_cache

  ## Run test by service
  python -m pytest -v

  if [ $? -eq 1 ]; then
      exit 1
  fi

  cd -

done