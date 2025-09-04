#!/usr/bin/env bash
set -euo pipefail

./gradlew --no-daemon clean build
./gradlew --no-daemon test
./gradlew --no-daemon check
