# EasyEdaTool

[中文](README.md)

Offline command-line tool for EasyEDA Pro folder projects. It builds the schematic and PCB from a design file, autoroutes, pours copper with the EDA rules, runs DRC and a pin-by-pin net check, and exports a schematic PDF, netlist, BOM, Gerber, drill files, and a pick-and-place file. It does not need a browser or the EDA client.

## Install

The repository is [cc38324/PcbCliTool](https://github.com/cc38324/PcbCliTool). After installation the command is `easyedatool` on every system. Release files for this version are at `https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.0`.

| System | 0.2.0 |
|---|---|
| Windows | `winget install --id Miyue.PcbCliTool --version 0.2.0` |
| macOS (Apple silicon) | `brew install cc38324/pcbclitool/easyedatool` |
| Ubuntu 22.04 / 24.04 / 26.04 | Add the `www.miyue.asia` source, then `sudo apt-get install easyedatool` |
| Debian 12 / 13 | The same source and the same commands as Ubuntu |
| HarmonyOS PC | No HarmonyOS build in 0.2.0 |

### Windows

After the manifest is in the winget source:

```powershell
winget install --id Miyue.PcbCliTool --version 0.2.0
easyedatool --version
```

Until then, download `easyedatool-0.2.0-windows-x64.zip` from the Release and run `easyedatool\bin\easyedatool.exe`. `easyedatool-0.2.0-windows-x64-setup.exe` installs into `%USERPROFILE%\.claude\skills\easyedatool`. The installer is unsigned; Windows may ask for More info, then Run anyway.

### macOS (Apple silicon)

```bash
brew tap cc38324/pcbclitool https://github.com/cc38324/PcbCliTool.git
brew install cc38324/pcbclitool/easyedatool
easyedatool --version
```

The formula is `Formula/easyedatool.rb`. It downloads `easyedatool-0.2.0-macos-arm64.tar.gz`. SHA256: `70f2eff5ff7128aacb2eee2653167b967632004df2680625ce76d1449b475e38`. There is no Intel build in this version.

### Ubuntu

22.04, 24.04, and 26.04, amd64. The binary uses glibc symbols up to 2.35. The source is `https://www.miyue.asia/apt`, the same one used by rtsp-ai. Add it once:

```bash
sudo mkdir -p /usr/share/keyrings
curl -fsSL https://www.miyue.asia/apt/miyue.gpg | sudo tee /usr/share/keyrings/miyue.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/miyue.gpg] https://www.miyue.asia/apt stable main" | sudo tee /etc/apt/sources.list.d/miyue.list
sudo apt-get update
sudo apt-get install easyedatool
easyedatool --version
```

If that source is already configured, only the last two commands are needed. The program is at `/usr/bin/easyedatool`. Upgrades are `sudo apt-get update && sudo apt-get install easyedatool`.

### Debian

Debian 12 and 13, amd64. Same deb and the same source as Ubuntu. Add it once:

```bash
sudo mkdir -p /usr/share/keyrings
curl -fsSL https://www.miyue.asia/apt/miyue.gpg | sudo tee /usr/share/keyrings/miyue.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/miyue.gpg] https://www.miyue.asia/apt stable main" | sudo tee /etc/apt/sources.list.d/miyue.list
sudo apt-get update
sudo apt-get install easyedatool
easyedatool --version
```

If that source is already configured, run `sudo apt-get update && sudo apt-get install easyedatool`.

### HarmonyOS PC

0.2.0 has no binary that runs in HiShell, so this does not install yet. When a HarmonyOS build exists, install [Harmonybrew](https://harmonybrew.atomgit.com), then:

```bash
brew install easyedatool
```

## Example: STM32MP157

The example is an STM32MP157 single-board computer, 100 × 80 mm, four layers, stack-up `JLC04161H-3313`. The generated board has about 238 parts (130 on top, 108 on the bottom), 1307 pads, 851 vias, and 210 nets.

| File | Contents |
|---|---|
| `skill/examples/mp157demo.toml` | Design file. `easyedatool gen` builds the project from it |
| `skill/examples/mp157demo.rules.toml` | Rules for routing, DRC, and the net check |
| `skill/examples/mp157demo.constraints.toml` | Differential pairs (USB, MIPI DSI, Ethernet, DDR) |

The design names 23 library parts, placed 30 times (`part = "STM32MP157DAB1"` and the rest). Each one has its LCSC number (`lcsc = "C1236721"` and the rest). Symbols and footprints are in `skill/examples/lib` (23 symbols, 21 footprints; some parts share a footprint). `skill/examples/easyedatool.toml` points at that library.

`<project>` below is the project folder. `route` rewrites the board. This rules file sets `keep = ["*"]`, so existing tracks stay and only open connections are added. Commit first, and roll back with git if the result is wrong. If EasyEDA has this project open, close the PCB page before a command that writes the board, then open it again.

```bash
easyedatool gen skill/examples/mp157demo.toml --out MP157Demo

easyedatool info   <project>
easyedatool render <project> --view top -o MP157_top.png
easyedatool render <project> --view layers -o MP157_layers.png
easyedatool render <project> --view sch -o MP157_sch.png

easyedatool check <project> --rules skill/examples/mp157demo.rules.toml
easyedatool erc   <project>
easyedatool drc   <project> --rules skill/examples/mp157demo.rules.toml

easyedatool route <project> --rules skill/examples/mp157demo.rules.toml
easyedatool constraints <project> --from skill/examples/mp157demo.constraints.toml
easyedatool pair  <project> --pair USBH
easyedatool pour  <project>

easyedatool pdf     <project> -o MP157_sch.pdf
easyedatool netlist <project> -o MP157.net
easyedatool bom     <project> -o MP157_bom.csv
easyedatool fab     <project> -o MP157_fab
easyedatool view    <project>
```

`drc`, `check`, and `erc` exit with code 1 when they find problems. That is the check result. Add `--help` to any command for the full option list. Command help is in Chinese.

## For an AI assistant

The instructions are in `skill/SKILL.md`. Command, design-file, and rules-file details are in `skill/references/`.
