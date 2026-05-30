# Copied from https://wiki.nixos.org/wiki/Python
#
# Run `nix develop -f shell.nix` before running this.

# shell.nix
let
  # pinned to "Release  NixOS 23.05"
  # Necessary for metadata check from twine
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/2c6ae7132ca558f1052da0eececed3cad191b883.tar.gz") {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      build
      docutils
    ]))
    pkgs.twine
  ];
}
