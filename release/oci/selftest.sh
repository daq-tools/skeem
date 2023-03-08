#!/bin/bash

# Fail on error.
set -e

# Display all commands.
# set -x

flavor=$1

echo "Invoking Skeem"
skeem --version
skeem info

if [ "${flavor}" == "full" ]; then
  echo "Checking libraries"
  python -c 'import cfgrib; print("cfgrib:", cfgrib.__version__)'
  python -c 'import scipy; print("scipy:", scipy.__version__)'
  python -c 'import xarray; print("xarray:", xarray.__version__)'
fi
