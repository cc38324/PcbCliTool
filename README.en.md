# EasyEdaTool

[中文](README.md)

Offline command-line tool for EasyEDA Pro folder projects. It builds the schematic and PCB from a design file, autoroutes, pours copper with the EDA rules, runs DRC and a pin-by-pin net check, and exports a schematic PDF, netlist, BOM, Gerber, drill files, and a pick-and-place file. It does not need a browser or the EDA client.

## Install

The current version is **0.2.1**. Download it from [GitHub Release v0.2.1](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.1), and see the [release notes](CHANGELOG.md). This repository contains installation instructions, the AI manual, and examples; it does not contain the tool's source code.

| System | 0.2.1 package | PCB / schematic viewer |
|---|---|---|
| Windows x64 | [ZIP](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.1/easyedatool-0.2.1-windows-x64.zip) / [installer](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.1/easyedatool-0.2.1-windows-x64-setup.exe) | Included |
| macOS (Apple silicon) | [Full ZIP](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.1/easyedatool-0.2.1-macos-arm64.zip) | Included |
| macOS (Apple silicon), CLI | [CLI tar.gz](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.1/easyedatool-0.2.1-macos-arm64.tar.gz) / Homebrew | Not included |
| Ubuntu / Debian amd64 | [DEB](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.1/easyedatool_0.2.1-1_amd64.deb) | Included |
| Intel Mac / HarmonyOS PC | No package in this version | — |

Full packages include the CLI and desktop viewer; run `easyedatool view <project>` to open a board. Track widths, clearances, via sizes, and length constraints come from the design or rules file. Upgrading does not establish electrical correctness or manufacturing readiness for a project.

### Windows

Download the installer, or extract the ZIP and run:

```powershell
.\easyedatool\bin\easyedatool.exe --version
.\easyedatool\bin\easyedatool.exe view <project>
```

The installer defaults to `%USERPROFILE%\.claude\skills\easyedatool`. It is unsigned, so Windows may display a SmartScreen prompt. **Availability of 0.2.1 in the official winget source has not been confirmed.** Use the Release downloads above; winget is not listed as a verified installation channel for this version.

### macOS (Apple silicon)

For the desktop viewer, download the full ZIP, extract it, and run:

```bash
./easyedatool/bin/easyedatool --version
./easyedatool/bin/easyedatool view <project>
```

The viewer is `easyedatool/viewer/easyeda_view.app`; preserve its relative location next to `bin/`. The package is not notarized by Apple. If macOS blocks it, verify its source and checksum before allowing it in the system security settings.

For the CLI only, use Homebrew:

```bash
brew tap cc38324/pcbclitool https://github.com/cc38324/PcbCliTool.git
brew update
brew install cc38324/pcbclitool/easyedatool
easyedatool --version
```

For an existing installation, run `brew upgrade cc38324/pcbclitool/easyedatool`. The [formula](Formula/easyedatool.rb) installs only the CLI; confirm the version with `easyedatool --version`. For a manual CLI installation, extract the tar.gz: its top-level `easyedatool` file is the executable.

### Ubuntu / Debian

Download the DEB and install it from your download directory. `apt` resolves the viewer's system dependencies:

```bash
sudo apt install ./easyedatool_0.2.1-1_amd64.deb
easyedatool --version
easyedatool view <project>
```

The DEB targets amd64 Ubuntu / Debian systems. The viewer needs a graphical desktop; the CLI also works without one. See the [release notes](CHANGELOG.md) for the actual platform validation scope.

The existing APT source is also available. It may update after GitHub Release, so inspect its available versions first:

```bash
sudo mkdir -p /usr/share/keyrings
curl -fsSL https://www.miyue.asia/apt/miyue.gpg | sudo tee /usr/share/keyrings/miyue.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/miyue.gpg] https://www.miyue.asia/apt stable main" | sudo tee /etc/apt/sources.list.d/miyue.list
sudo apt-get update
apt-cache policy easyedatool
sudo apt-get install easyedatool=0.2.1-1
easyedatool --version
```

If `0.2.1-1` is not listed, use the Release DEB. Successfully installing an older package does not confirm that this release is available through APT.

## Example: STM32MP157

Paths below are relative to this repository's root. Full ZIPs place the contents of `skill/` directly inside the extracted `easyedatool/` directory. When running from that directory, omit the `skill/` prefix; for example, `easyedatool gen examples/mp157demo.toml --out MP157Demo`.

The example is an STM32MP157 single-board computer, 100 × 80 mm, four layers, stack-up `JLC04161H-3313`. The generated board has about 238 parts (130 on top, 108 on the bottom), 1307 pads, 851 vias, and 210 nets.

| File | Contents |
|---|---|
| `skill/examples/mp157demo.toml` | Design file. `easyedatool gen` builds the project from it |
| `skill/examples/mp157demo.rules.toml` | Rules for routing, DRC, and the net check |
| `skill/examples/mp157demo.constraints.toml` | Differential pairs (USB, MIPI DSI, Ethernet, DDR) |

The design names 23 library parts, placed 30 times (`part = "STM32MP157DAB1"` and the rest). Each one has its LCSC number (`lcsc = "C1236721"` and the rest). Symbols and footprints are in `skill/examples/lib` (23 symbols, 21 footprints; some parts share a footprint). `skill/examples/easyedatool.toml` points at that library.

The core layout copied by `[[reuse]]` is `skill/build/st/board.PcbDoc`. It is the Altium board `STM32MP15XXAB/STM32MP15XXAB_1DDR3Lx16` from ST's AN5122 package `stm32mp15x-series-ddr-memory-routing-guidelines-examples.zip`, saved under this name. The design file points at it with `../build/st/board.PcbDoc`.

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
