#!/bin/bash
set -e

for dir in day-*/; do
  echo "Running tests in $dir"
  cd "$dir"
  npm install
  npm test
  cd ..
done
echo "All tests completed successfully."
