#!/bin/zsh

trap 'exit 0' INT TERM

# Keep the process alive without emitting startup text.
while IFS= read -r line; do
  :
done
