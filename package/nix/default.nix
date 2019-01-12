# Nix package for the "Papers Please" citation generator
#
# environment.systemPackages =
#   let citationGit = builtins.fetchGit {
#     url = "https://gitlab.com/Saphire/citations.git";
#     rev = "<some rev>";
#   };
#   in [ (pkgs.callPackage "${citationGit}/package/nix" {}) ];

{ pkgs }:

with pkgs.python3Packages;

buildPythonPackage rec {
  name = "citations";
  src = ../..;
  propagatedBuildInputs = [ pillow ];
}

