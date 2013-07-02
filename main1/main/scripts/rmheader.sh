#!/bin/bash

cat "$1" | tail -n +2 > "$1"".tmp"
mv "$1"".tmp" "$1"
