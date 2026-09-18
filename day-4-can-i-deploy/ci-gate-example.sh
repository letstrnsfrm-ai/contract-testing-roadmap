#!/bin/bash
echo "Running can-i-deploy..."
npm run can-i-deploy
if [ $? -eq 0 ]; then
  echo "Proceeding with deployment..."
else
  echo "Deployment blocked due to contract verification failures!"
  exit 1
fi
