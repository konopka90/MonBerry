#!/bin/bash

URL=$(curl -s 'http://localhost:3000/api/search' | python3 -c "import sys, json; print(json.load(sys.stdin)[0]['url'])")
FULL_URL="http://localhost:3000${URL}?orgId=1&refresh=5s&kiosk"

if [[ $URL == *"temperature"* ]]; then
  chromium-browser --start-fullscreen --app=$FULL_URL
else
    echo "Cannot fetch URL"
    exit 1
fi

