with import <nixpkgs> {};
with pkgs.python3Packages;

buildPythonPackage rec {
  name = "hyprrazer";
  src = ./.;
  version = "1.0.0";
  pyproject = true;
nativeBuildInputs = with pkgs.python311Packages; [
#   openrazer
    setuptools
#     yamllint
#     xlib
# #     pywayland
# #     pywlroots
#     pip
]; 
# nativeBuildInputs = [ xorg.libX11 ];
  propagatedBuildInputs = with pkgs.python311Packages; [
    openrazer
    yamllint
    xlib
    # setuptools
    pip
  ];

}
