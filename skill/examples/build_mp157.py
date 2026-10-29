"""重建 STM32MP157 示例并执行检查；--export 仅在全部检查通过后导出图纸及生产文件。"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def main():
    here = Path(__file__).resolve().parent
    default_design = here / "mp157demo.toml"
    if not default_design.exists():
        default_design = here.parent / "design" / "mp157demo.toml"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", default="easyedatool", help="easyedatool 程序路径")
    parser.add_argument("--design", type=Path, default=default_design, help="设计文件路径")
    parser.add_argument("--out", required=True, type=Path, help="生成的工程目录")
    parser.add_argument("--export", action="store_true", help="同时导出 PDF、BOM、网表、效果图及生产文件")
    args = parser.parse_args()
    design = args.design.resolve()
    project = args.out.resolve()
    tool = shutil.which(args.tool) or str(Path(args.tool).resolve())
    rules_dir = design.parent
    if not (rules_dir / "mp157demo.rules.toml").exists():
        rules_dir = design.parent.parent / "rules"
    if not design.with_suffix(".layout.toml").exists():
        parser.error("缺少 mp157demo.layout.toml：完成版的走线和铺铜保存在此文件中")

    def run(*command):
        print("$", " ".join(map(str, command)), flush=True)
        subprocess.run([tool, *map(str, command)], check=True)

    # gen 恢复布局与铜；差分约束和可读丝印须在每次 gen 后重新写入。
    run("gen", design, "--out", project, "--no-drc")
    run("constraints", project, "--from", rules_dir / "mp157demo.constraints.toml", "--write", "--no-drc")
    run("label", project, "--from", rules_dir / "mp157demo.labels.toml", "--write", "--no-drc")
    run("layout", project, "--save")
    output = project / "output"
    output.mkdir(exist_ok=True)
    run("check", project, "--rules", rules_dir / "mp157demo.rules.toml")
    run("erc", project, "--json", output / "MP157Demo_erc.json")
    run("constraints", project)
    subprocess.run([sys.executable, str(here / "check_display.py"), str(project), "--tool", tool], check=True)
    run("drc", project, "--rules", rules_dir / "mp157demo.rules.toml", "--json", output / "MP157Demo_drc.json")
    if args.export:
        for view in ("top", "bottom", "layers", "sch"):
            run("render", project, "--view", view, "-o", output / f"MP157Demo_{view}.png")
        run("pdf", project, "-o", output / "MP157Demo_sch.pdf")
        run("bom", project, "-o", output / "MP157Demo_bom.csv")
        run("netlist", project, "-o", output / "MP157Demo.net")
        run("fab", project, "--files", "-o", output / "MP157Demo_fab")
    print("工程已重建，核对、ERC、差分约束和 DRC 已通过；屏型号及实物验证状态仍以 README 为准。")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
