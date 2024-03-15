{
  description = "HyprRazer nix flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }: {

    packages = withPkgsFor (system: pkgs: {
        hyprRazer = pkgs.callPackage ./default.nix {
        };
        })
  };
}
