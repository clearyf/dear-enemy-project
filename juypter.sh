#!/bin/sh

nix-shell -p "with import <nixpkgs> {}; python36.withPackages (ps: [ ps.numpy ps.toolz ps.jupyter ps.matplotlib ps.scipy ps.pandas ])" --run jupyter-notebook
