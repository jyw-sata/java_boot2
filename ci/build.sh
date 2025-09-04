#!/usr/bin/env bash
# Gradle 빌드, 테스트, 정적 분석 및 파이썬 테스트를 수행
set -euo pipefail

./gradlew --no-daemon clean build
./gradlew --no-daemon test
./gradlew --no-daemon check

pytest
