{
  description = "HyprRazer nix flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
  inherit (nixpkgs) lib;
  in
  {
    packages."<sytem>".hyprrazer = nixpkgs.callPackage ./default.nix;
  };
}
