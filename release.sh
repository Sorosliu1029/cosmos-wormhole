#!/usr/bin/env bash

hatch_option=$1
if [ -z "$hatch_option" ]; then
  echo "Usage: $0 <hatch_option>"
  exit 1
fi

case "$hatch_option" in
  patch | fix | minor | major | release)
    hatch version "$hatch_option"
    hatch_version=$(hatch version)
    echo "Releasing version $hatch_version"
    hatch build
    hatch publish
    ;;
  *)
    echo "Invalid option. Use 'patch', 'fix', 'minor', 'major', or 'release'."
    exit 1
    ;;
esac
