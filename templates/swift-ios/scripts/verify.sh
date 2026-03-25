#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MODE="${1:-verify}"

SIMULATOR_ID="${SIMULATOR_ID:-}"
DERIVED_DATA_PATH="${DERIVED_DATA_PATH:-DerivedData}"
PROJECT_NAME="${PROJECT_NAME:-APPNAME}"
SCHEME_NAME="${SCHEME_NAME:-APPNAME}"

find_simulator_id() {
  xcrun simctl list devices available | grep "iPhone 15" | head -n 1 | sed -E 's/.*\(([A-F0-9-]+)\).*/\1/'
}

resolve_destination() {
  local id="${SIMULATOR_ID}"
  if [ -z "$id" ]; then
    id="$(find_simulator_id)"
  fi

  if [ -z "$id" ]; then
    echo "Could not find an available iPhone simulator"
    exit 1
  fi

  echo "platform=iOS Simulator,id=${id}"
}

run_lint() {
  if ! command -v swiftlint >/dev/null 2>&1; then
    echo "swiftlint is required for lint mode"
    exit 1
  fi

  echo "Linting Swift files in current working directory"
  swiftlint lint --strict
}

run_build() {
  local destination
  destination="$(resolve_destination)"

  xcodegen generate
  xcodebuild -resolvePackageDependencies -project "${PROJECT_NAME}.xcodeproj" -scheme "${SCHEME_NAME}"
  echo "Using destination ${destination}"
  xcodebuild \
    -project "${PROJECT_NAME}.xcodeproj" \
    -scheme "${SCHEME_NAME}" \
    -destination "${destination}" \
    -derivedDataPath "${DERIVED_DATA_PATH}" \
    clean build
}

run_test() {
  local destination
  destination="$(resolve_destination)"

  xcodegen generate
  xcodebuild -resolvePackageDependencies -project "${PROJECT_NAME}.xcodeproj" -scheme "${SCHEME_NAME}"
  echo "Using destination ${destination}"
  xcodebuild \
    -project "${PROJECT_NAME}.xcodeproj" \
    -scheme "${SCHEME_NAME}" \
    -destination "${destination}" \
    -derivedDataPath "${DERIVED_DATA_PATH}" \
    test
}

run_verify() {
  run_lint
  run_build
  run_test
}

case "$MODE" in
  lint)
    run_lint
    ;;
  build)
    run_build
    ;;
  test)
    run_test
    ;;
  verify)
    run_verify
    ;;
  *)
    echo "Unknown mode ${MODE}"
    exit 1
    ;;
esac
