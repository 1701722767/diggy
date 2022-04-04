mkdir -p './artifacts'
tree

for d in ./services/* ; do
  if [ ! -d "$d" ]; then
    continue
  fi

  for f in $d/functions/* ; do
    if [ ! -d "$f" ]; then
      continue
    fi

    echo "$f"
    zip -jr ./artifacts/sample-service_sample.zip $f/main.py
    printf "@ main.py\n@=lambda_function.py\n" | zipnote -w ./artifacts/sample-service_sample.zip
  done
done