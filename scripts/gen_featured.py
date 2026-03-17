#!/usr/bin/env python3
"""Generate featured-openclaw.svg from live GitHub repo data.

Usage: python3 scripts/gen_featured.py "<description>" <stars>
"""
import sys
import textwrap
import pathlib

# Base64-encoded OpenClaw pixel-lobster icon (icon32.png from openclaw/openclaw)
OPENCLAW_ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAA"
    "80lEQVRYhWNgGAUjHTASUmDFxfufEguOffuM1w4mSgynBsDpOpjPYT747+9AUkgwbjzAiM0c"
    "dDD4QoCQz7+t2c/AwMDAwBXiyECMOKGQGDwhAHPh0dwgiMCNh1g1cB68xsDAwMDw3V6LKHE4"
    "0JBnYGBgYLCevI6BgQEREoMnBP6Xx6OmchwhQDaAhgDc4s6FgyMEWGAMWNzA0wCNAMweGBjw"
    "ECC5HCDZgiFTDqCDEVMXEARWXLz/KW0T4AMDHgIEW0QwQGooEGoJwcDgDwF4LelqTJLB1rvP"
    "MjAwDKc2IQwQKg9g+Z+QOTAweEMAHQzbXDAKAN+acUaL3dFjAAAAAElFTkSuQmCC"
)

DISCORD_PATH = (
    "M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375"
    "-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077"
    ".077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533"
    " 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.029"
    ".078.078 0 0 0 .084-.026 13.83 13.83 0 0 0 1.226-1.963.074.074 0 0 0-.041-.104"
    " 13.175 13.175 0 0 1-1.872-.878.075.075 0 0 1-.008-.125c.126-.094.252-.192.372"
    "-.292a.075.075 0 0 1 .078-.01c3.927 1.764 8.18 1.764 12.061 0a.075.075 0 0 1 "
    ".079.009c.12.098.245.198.372.292a.075.075 0 0 1-.006.125 12.3 12.3 0 0 1-1.873"
    ".892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084"
    ".028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674"
    "-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419"
    " 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418"
    "-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157"
    "-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"
)

DOCKER_PATH = (
    "M13.983 11.078h2.119a.186.186 0 0 0 .186-.185V9.006a.186.186 0 0 0-.186-.186h"
    "-2.119a.185.185 0 0 0-.185.185v1.888c0 .102.083.185.185.185m-2.954-5.43h2.118a"
    ".186.186 0 0 0 .186-.186V3.574a.186.186 0 0 0-.186-.185h-2.118a.185.185 0 0 0-"
    ".185.185v1.888c0 .102.082.185.185.186m0 2.716h2.118a.187.187 0 0 0 .186-.186V6"
    ".29a.186.186 0 0 0-.186-.185h-2.118a.185.185 0 0 0-.185.185v1.887c0 .102.082.1"
    "86.185.186m-2.93 0h2.12a.186.186 0 0 0 .184-.186V6.29a.185.185 0 0 0-.185-.185"
    "H8.1a.185.185 0 0 0-.185.185v1.887c0 .102.083.186.185.186m-2.964 0h2.119a.186."
    "186 0 0 0 .185-.186V6.29a.185.185 0 0 0-.185-.185H5.136a.186.186 0 0 0-.186.18"
    "5v1.887c0 .102.084.186.186.186m-2.92 0h2.12a.185.185 0 0 0 .184-.186V6.29a.184"
    ".184 0 0 0-.185-.185h-2.12a.185.185 0 0 0-.184.185v1.887c0 .102.083.186.185.18"
    "6m-2.964.001h2.12a.186.186 0 0 0 .185-.185V6.29a.185.185 0 0 0-.185-.186h-2.12"
    "a.186.186 0 0 0-.186.185v1.888c0 .102.084.185.186.185M23.763 9.89c-.065-.051-."
    "672-.51-1.954-.51-.338.001-.676.03-1.01.087-.248-1.7-1.653-2.53-1.716-2.566l-."
    "344-.199-.226.327c-.284.438-.49.922-.612 1.43-.23.97-.09 1.882.403 2.661-.595."
    "332-1.55.413-1.744.42H.751a.751.751 0 0 0-.75.75c-.003 1.373.148 2.742.45 4.07"
    "2.33 1.437.834 2.494 1.498 3.144.694.68 1.82 1.068 3.16 1.068 1.285.003 2.56-."
    "235 3.759-.706 1.097-.44 2.1-1.09 2.945-1.918.818.75 1.798 1.295 2.865 1.592."
    "82.226 1.672.343 2.528.345.013.001.025.001.038.001h.057c.745 0 1.488-.083 2.21"
    "4-.247 1.048-.247 1.958-.72 2.69-1.393.608-.552 1.105-1.22 1.462-1.963.283-.59"
    "6.5-1.218.645-1.856.045-.186.083-.377.116-.567.095-.518.116-.851.119-.878a.748"
    ".748 0 0 0-.258-.621z"
)


def generate(desc: str, stars: int, out_path: str = "featured-openclaw.svg") -> None:
    WRAP = 50
    START_Y = 63
    DY = 22

    lines = textwrap.wrap(desc, WRAP) if desc.strip() else ["(no description)"]
    lines = lines[:4]  # cap at 4 lines to keep card compact
    n = len(lines)

    last_y = START_Y + (n - 1) * DY
    BY = last_y + 21   # badge row y
    H  = BY + 22 + 18  # SVG total height

    # build description tspans
    tspans = [f'    <tspan x="22" y="{START_Y}">{lines[0]}</tspan>']
    for line in lines[1:]:
        tspans.append(f'    <tspan x="22" dy="{DY}">{line}</tspan>')
    desc_block = "\n".join(tspans)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="440" height="{H}" viewBox="0 0 440 {H}">

  <style>
    .title {{ fill: #1f2328; }}
    .desc  {{ fill: #636c76; }}
    .icon  {{ fill: #0969da; }}
    .meta  {{ fill: #636c76; }}
    .border {{ stroke: #d0d7de; }}
    @media (prefers-color-scheme: dark) {{
      .title {{ fill: #e6edf3; }}
      .desc  {{ fill: #8b949e; }}
      .icon  {{ fill: #58a6ff; }}
      .meta  {{ fill: #8b949e; }}
      .border {{ stroke: #30363d; }}
    }}
  </style>

  <rect width="440" height="{H}" rx="16" fill="none" class="border" stroke-width="1"/>

  <g transform="translate(22,23)" class="icon">
    <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"/>
  </g>

  <text x="44" y="37"
        font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"
        font-size="18" font-weight="600" class="title">openclaw-discord-multiagent</text>

  <text font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"
        font-size="14" class="desc">
{desc_block}
  </text>

  <g transform="translate(22,{BY}) scale(0.875)" class="meta">
    <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.873 6.052a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/>
  </g>
  <text x="40" y="{BY + 13}"
        font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"
        font-size="14" class="meta">{stars}</text>

  <!-- OpenClaw badge -->
  <rect x="60" y="{BY}" width="84" height="22" rx="3" fill="#CC2233"/>
  <image x="65" y="{BY + 4}" width="14" height="14"
         href="data:image/png;base64,{OPENCLAW_ICON_B64}"/>
  <text x="82" y="{BY + 15}"
        font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"
        font-size="12" font-weight="500" fill="white">OpenClaw</text>

  <!-- Discord badge -->
  <rect x="151" y="{BY}" width="78" height="22" rx="3" fill="#5865F2"/>
  <g transform="translate(156,{BY + 4}) scale(0.5)" fill="white">
    <path d="{DISCORD_PATH}"/>
  </g>
  <text x="172" y="{BY + 15}"
        font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"
        font-size="12" font-weight="500" fill="white">Discord</text>

  <!-- Docker badge -->
  <rect x="236" y="{BY}" width="72" height="22" rx="3" fill="#2496ED"/>
  <g transform="translate(241,{BY + 4}) scale(0.5)" fill="white">
    <path d="{DOCKER_PATH}"/>
  </g>
  <text x="257" y="{BY + 15}"
        font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"
        font-size="12" font-weight="500" fill="white">Docker</text>

</svg>
"""
    pathlib.Path(out_path).write_text(svg)
    print(f"Generated {out_path} ({n} desc lines, height={H})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: gen_featured.py <description> <stars>")
        sys.exit(1)
    generate(sys.argv[1], int(sys.argv[2]))
