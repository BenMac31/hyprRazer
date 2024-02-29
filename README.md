hypr - razer
==========

*Visualize hotkeys on a Razer keyboard*

A tool to show possible hotkeys or commands (e.g. hyprland or vim commands) on a Razer keyboard with rgb lighting. 
Based on the excellent project [i3razer](https://github.com/leofah/i3razer) by Leo Fahrbach.
This project is currently *highly* unpolished, and works in a hacky way.
Anything that works well can be attributed to i3razer, anything buggy & hacky can be attributed to my own "improvements."
Any sort of PRs to help improve it or flat out forking because my code base is irredeemably cursed is welcome!

<!-- Installation -->
<!-- ============ -->

<!-- **Disclaimer** *This project is currently highly unpolished.* -->

<!-- ``` -->
<!-- $ nix-build hyprrazer.nix -->
<!-- ``` -->
<!-- If installed with privileged rights the executable `i3razer` will already be in the path. -->
<!-- Otherwise it can be found in `$HOME/.local/bin` -->

Usage
=====

Setting layout:
If the layout does not work by default it will be necessary to set it up, run:
```
$ hyprrazer --map
```
In a terminal running on Xwayland (original code base was designed for X11, and I don't know how to convert this function to work natively on Wayland.)

Afterwards
```
$ hyprrazer -f /path/to/csv.nix
```
can be run on a csv of the format key,hexcolor EX:
```
q,ffffff
w,ff0000
9,06ff00
tab,7000ff
f1,dd00fa
```
This will set the colors of each key to the specified hex color.
To view what keys are valid read the layout.py file.

To use with Hyprland add the following to your config file

```
# Trigger hyprrazer on SUPER down
bindni=SUPER,SUPER_L,exec,hyprrazer -f ~/.cache/hyprrazer/SUPER.csv
# Set layout back to what it was before upon key release. This is currently not handled within hyprrazer.
bindirnt=SUPER,SUPER_L,exec,polychromatic-cli -d laptop -z main -o static -c fbf1c7
```
