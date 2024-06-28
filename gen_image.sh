#!/bin/zsh
source ~/venvs/rocm6_0_2/bin/activate
export HSA_OVERRIDE_GFX_VERSION=10.3.0
python sdfast.py \"$1\"
