let
pkgs = import <nixpkgs> {};
stdenv = pkgs.stdenv;
in with pkgs; {
  myProject = stdenv.mkDerivation {
    name = "myProject";
    version = "1";
    src = if pkgs.lib.inNixShell then null else nix;
    buildInputs = let
      pyPkgs = python36.withPackages (ps: [
      ps.numpy
      ps.toolz
      ps.jupyter
      ps.matplotlib
      ps.statsmodels
    ]);
    in [pyPkgs];
  };
}
