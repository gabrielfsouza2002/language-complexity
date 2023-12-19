{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-22.11") {} }:
  let python-packages = ps: with ps; [
    black
    ipywidgets
    jupyterlab
    matplotlib
    mypy
    nltk
    numpy
    openpyxl
    pandas
  ];
  in
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
    	(python3.withPackages python-packages)
    ];
  }

