# EasyEdaTool

[中文](README.md)

Offline command-line tool for EasyEDA Pro folder projects. It builds the schematic and PCB from a design file, autoroutes, pours copper with the EDA rules, runs DRC and a pin-by-pin net check, and exports a schematic PDF, netlist, BOM, Gerber, drill files, and a pick-and-place file. EasyEDA projects and exported PADS ASCII files need neither a browser nor an EDA client. Native PADS binary `.pcb` import requires Windows and a locally licensed PADS Layout installation.

Version 0.2.3 includes native PADS `.pcb` import, mixed metric/imperial footprint fixes, and real mounting-hole and slot cutouts. PNG, GLB and STL share the same geometry; the Flutter viewer exports both model formats. Complete body silkscreen and conflict checks remain required.

## Install

The current version is **0.2.3**. Download it from [GitHub Release v0.2.3](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.3), and see the [release notes](https://github.com/cc38324/PcbCliTool/blob/main/CHANGELOG.md). This repository contains installation instructions, the AI manual, and examples; it does not contain the tool's source code.

| System | 0.2.3 package | PCB / schematic viewer |
|---|---|---|
| Windows x64 | [ZIP](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool-0.2.3-windows-x64.zip) / [installer](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool-0.2.3-windows-x64-setup.exe) | Included |
| macOS (Apple silicon) | [Full ZIP](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool-0.2.3-macos-arm64.zip) | Included |
| macOS (Apple silicon), CLI | [CLI tar.gz](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool-0.2.3-macos-arm64.tar.gz) / Homebrew | Not included |
| Ubuntu / Debian amd64 | [DEB](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool_0.2.3-1_amd64.deb) | Included |
| Intel Mac / HarmonyOS PC | No package in this version | — |

Full packages include the CLI and desktop viewer; run `easyedatool view <project>` to open a board. Track widths, clearances, via sizes, and length constraints come from the design or rules file. Upgrading does not establish electrical correctness or manufacturing readiness for a project.

### Windows

Download the installer, or extract the ZIP and run:

```powershell
.\easyedatool\bin\easyedatool.exe --version
.\easyedatool\bin\easyedatool.exe view <project>
```

The installer defaults to `%USERPROFILE%\.claude\skills\easyedatool`. It is unsigned, so Windows may display a SmartScreen prompt. **After refreshing the official source on 2026-10-28, `Miyue.PcbCliTool` was not found.** The [0.2.0 submission, #452460](https://github.com/microsoft/winget-pkgs/pull/452460), passed automated validation and still awaits maintainer approval. The [0.2.3 manifests](winget/README.md) pass local schema validation; this does not establish official source availability. Use the Release downloads.

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

For an existing installation, run `brew upgrade cc38324/pcbclitool/easyedatool`. The [formula](https://github.com/cc38324/PcbCliTool/blob/main/Formula/easyedatool.rb) installs only the CLI; confirm the version with `easyedatool --version`. For a manual CLI installation, extract the tar.gz: its top-level `easyedatool` file is the executable.

### Ubuntu / Debian

Download the DEB and install it from your download directory. `apt` resolves the viewer's system dependencies:

```bash
sudo apt install ./easyedatool_0.2.3-1_amd64.deb
easyedatool --version
easyedatool view <project>
```

The DEB targets amd64 Ubuntu / Debian systems. The viewer needs a graphical desktop; the CLI also works without one. See the [release notes](https://github.com/cc38324/PcbCliTool/blob/main/CHANGELOG.md) for the actual platform validation scope.

The existing APT source is also available. It may update after GitHub Release, so inspect its available versions first:

```bash
sudo mkdir -p /usr/share/keyrings
curl -fsSL https://www.miyue.asia/apt/miyue.gpg | sudo tee /usr/share/keyrings/miyue.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/miyue.gpg] https://www.miyue.asia/apt stable main" | sudo tee /etc/apt/sources.list.d/miyue.list
sudo apt-get update
apt-cache policy easyedatool
sudo apt-get install easyedatool=0.2.3-1
easyedatool --version
```

If `0.2.3-1` is not listed, use the Release DEB. Successfully installing an older package does not confirm that this release is available through APT.

## 0.2.3: component silkscreen, placement and board 3D

New layouts and footprint changes must preserve component body outlines, pin-1 marks and diode/LED polarity marks. Inventory every component first. Resolve conflicts by moving or rotating parts and reconnecting affected copper; do not delete or trim outlines or hide layers to suppress findings. Check silkscreen and component spacing, then inspect the actual top/bottom Gerbers and current preview. Reference text may be hidden when the user permits it; body and orientation marks remain, and the BOM, placement file and assembly drawing keep every reference. See the [silkscreen workflow](skill/references/silkscreen.md).

`render3d <project> -o board.glb` exports a self-contained coloured model, `-o board.stl` exports colourless millimetre STL geometry (import as mm), and `-o board.png` exports an image. `view <project> --3d` opens the viewer's 3D tab. Real models and estimated shapes are identified separately. Model alignment never moves PCB copper. There is no model-collision check, and estimates cannot validate enclosure dimensions. Add `--download-models` to fetch library models, then reuse the cache offline.

The release also includes mounting holes, complete outline/orientation checks, power-neck checks across pads and vias, preservation of native record identities, project-specific preview checks and configurable routing search budgets. Board dimensions and routing/process parameters remain in project design and rule files.

## Example: STM32MP157

A 100×80 mm, four-layer `JLC04161H-3313` example with 289 components and eight schematic pages, preserving ST's DDR and power core. It uses the selected **AM319M262928ZS 3.19-inch 262×928 AMOLED**, CO6300 display driver, CST3530 touch and **DF40C-30DS-0.4V(51), C424642**, 30-pin receptacle. The MP157 uses one DSI data lane; no LED backlight circuit is needed.

The [display notes](skill/examples/docs/display/README.md) include the original panel PDF, all pin assignments and pin-1 orientation. On the board top view, J6 pin 1 is at the lower right and connects to ground. The panel drawing's rear view must not be copied as a board top view. Controlled 3.7V, 1.8V, 2.8V and VCI_EN 3.3V outputs and 1.8V touch/reset/TE translation are included.

From the repository root, using a CLI with `body_silk.pin1.at` support:

```powershell
python skill/examples/build_mp157.py --tool easyedatool --out MP157Demo --export
easyedatool view MP157Demo
```

In the full package, omit `skill/` and point `--tool` to `bin/easyedatool.exe`. Keep the design, routed layout, rules, constraints, labels, local library and build/check scripts together. The build restores copper, runs schematic/PCB, ERC, constraints, display-specific and DRC checks, then exports documentation and manufacturing files.

All 1262 connected pins match the PCB, and eight pages pass the layout audit. Display checks cover all 30 pins, unused D1/ID/VPP and the original PDF hash. Clock PCB P/N lengths are 52.285 / 51.463 mm; D0 lengths are 56.341 / 55.560 mm. These compensate the LFBGA354 package's 0.822 / 0.781 mm differences, leaving less than 0.001 mm electrical skew; average clock/data length difference is 4.077 mm. Eleven pair constraints are checked.

The dense ST core retains conventional mask-cleared silk as requested; peripherals keep complete frames and orientation marks. Inner layer 1 remains the ground reference except for one approximately 15 mm PA10 connection. Fabrication warnings and routing-quality notices remain in the DRC JSON, and generic BOM entries still need procurement selections.

The original ST AN5122 reference remains at `skill/build/st/board.PcbDoc`, referenced relatively. No physical panel test is claimed. CO6300 initialization, CST3530 software, touch coordinates, module power sequencing, load, ripple, EMI and RF validation remain necessary.

## For an AI assistant

The instructions are in `skill/SKILL.md`. Command, design-file, and rules-file details are in `skill/references/`.
