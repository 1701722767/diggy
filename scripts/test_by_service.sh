#!/bin/bash
exit_code = 0
for d in ./services/* ; do
  if [ ! -d "$d" ]; then
    continue
  fi

  cd $d


  ## Run test by service
  python -m pytest -v

  if [ $? -eq 1 ]; then
      $exit_code = 1
  fi

  cd -

done

exit $exit_code