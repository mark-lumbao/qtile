# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
import os
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
alt = "mod1"
scratchpad_class = "scratch"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Application Shortcuts
    Key(
        [mod, "shift"],
        "p",
        lazy.spawn("alacritty --class " + scratchpad_class + " -e pulsemixer"),
        desc="Print Screen",
    ),
    Key(
        [mod, "shift"],
        "e",
        lazy.spawn("alacritty --class " + scratchpad_class + " -e ranger"),
        desc="Print Screen",
    ),
    Key(
        [mod, "shift"],
        "t",
        lazy.spawn("alacritty --class " + scratchpad_class + " -e htop"),
        desc="Print Screen",
    ),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Print Screen"),
    Key(
        [mod],
        "p",
        lazy.spawn(
            "dmenu_run -nf '#fbf1c7' -sf '#282828' -sb '#98971a' -fn 'Hasklug Nerd Font:size=10'"
        ),
    ),
    Key(
        [alt],
        "p",
        lazy.spawn(
            "rofi -theme gruvbox-dark-hard -lines 12 -padding 18 -width 60 -location 0 -show drun -sidebar-mode -columns 3 -font 'Hasklug Nerd Font 12'"
        ),
    ),
    Key([alt], "s", lazy.spawn("slack"), desc="Launch slack"),
    Key([alt], "e", lazy.spawn("element-desktop"), desc="Launch element"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn("brave"), desc="Launch browser"),
    Key(
        [alt],
        "b",
        lazy.spawn("brave --incognito"),
        desc="Launch private browser",
    ),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Traverse between active groups
    Key(
        [mod, "control"],
        "k",
        lazy.screen.next_group(skip_managed=False, skip_empty=True),
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.screen.prev_group(skip_managed=False, skip_empty=True),
    ),
    # MonadTall Suggested
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "shift"], "space", lazy.layout.flip()),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Backlight
    Key([mod], "F1", lazy.spawn("brightnessctl s 1%")),
    Key([mod], "F2", lazy.spawn("brightnessctl s 10%-")),
    Key([mod], "F3", lazy.spawn("brightnessctl s 10%+")),
    Key([mod], "F4", lazy.spawn("bash -c ~/.config/mybin/dm_msi_opt")),
    # Volume
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc="Lower Volume by 10",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"),
        desc="Lower Volume by 10",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"),
        desc="Raise Volume by 10",
    ),
    # Misc
    Key([mod], "f", lazy.hide_show_bar(), desc="Toggle show/hide bar"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + control + letter of group = move focused window to group
            Key(
                [mod, "control"],
                i.name,
                lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.MonadTall(
        single_border_width=0,
        border_normal="282828",
        border_focus="98971a",
        border_width=4,
        margin=5,
        single_margin=0,
    ),
    layout.Max(),
]

widget_defaults = dict(
    font="Hasklug Nerd Font",
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()

spacer_length = 5
space_widget = widget.Spacer(length=spacer_length)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(foreground="fe8019"),
                widget.GroupBox(
                    hide_unused=True,
                    active="ebdbb2",
                    highlight_method="block",
                    block_highlight_text_color="282828",
                    this_current_screen_border="98971a",
                ),
                widget.Prompt(),
                widget.WindowName(foreground="fabd2f"),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.PulseVolume(
                    foreground="689d6a",
                    fmt=" {}",
                    update_interval=0.2,
                    volume_up_command="pactl set-sink-volume @DEFAULT_SINK@ +10%",
                    volume_down_command="pactl set-sink-volume @DEFAULT_SINK@ -10%",
                ),
                space_widget,
                widget.NvidiaSensors(fmt="GPU {}", foreground="ebdbb2"),
                space_widget,
                widget.CPU(foreground="b8bb26"),
                space_widget,
                widget.Memory(
                    foreground="b16286",
                    measure_mem="G",
                    format="RAM{MemUsed: .0f}{mm} /{MemTotal: .0f}{mm}",
                ),
                space_widget,
                widget.Clock(foreground="458588", format=" %Y-%m-%d %a %I:%M %p"),
                space_widget,
                widget.Battery(
                    foreground="fe8019",
                    full_char="",
                    charge_char="",
                    discharge_char="",
                    unknown_char="",
                    format="{char} {percent:2.0%}",
                ),
                widget.Systray(),
            ],
            24,
            background="#282828",
            opacity=0.9,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="azote"),  # gitk
        Match(wm_class=scratchpad_class),  # gitk
    ],
    border_focus="98971a",
    border_normal="282828",
    border_width=3,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


# Autostarts
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser(
        "~/.config/qtile/autostart.sh"
    )  # path to my script, under my user directory
    subprocess.run([home])
