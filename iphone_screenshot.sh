#!/bin/bash
screencapture -l$(osascript -e 'tell app "QuickTime Player" to id of window 1') ./screenshot.png
