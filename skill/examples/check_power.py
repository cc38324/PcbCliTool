"""核对显示供电器件距 J6 的位置，以及全板电源的连续线宽检查。"""
import argparse
import csv
import io
import json
import math
from pathlib import Path
import re
import subprocess
import sys
try:
    import tomllib
except ModuleNotFoundError:
    raise SystemExit('电源规则检查需要 Python 3.11 或更新版本。')

POWER_NETS = {
    '3V3', '5V_VIN', 'GND', 'LCD_1V8', 'NetL1_1', 'NetL2_1', 'NetL3_1',
    'NetL4_1', 'NetL5_1', 'OLED_BOOT', 'OLED_SW', 'OLED_VBAT', 'OLED_VCI_EN',
    'TP_2V8', 'VBUS_HOST', 'VDD', 'VDDA', 'VDDA_1V8', 'VDDA_PHY',
    'VDD_CORE', 'VDD_DDR', 'VDD_USB', 'VREF+', 'VREF_DDR', 'VTT_DDR',
    'WL_LDO_SW', 'WL_VIN_LDO',
    'NetC43_2', 'NetC68_2', 'NetC69_2', 'NetC70_2', 'NetC82_2', 'NetR43_1',
    'PHY_VDDCR',
}


def approved_bga_escape(issue, pads):
    """用户确认保留的唯一参考板 BGA 短出线；不能按整个 GND 网络豁免。"""
    if issue['kind'] != 'width_neck' or issue['net'] != 'GND' or issue['layer'] != 1:
        return False
    lands = {pin: next(p for p in pads if p['part'] == 'U5' and p['num'] == pin)
             for pin in ('N2', 'P2', 'P3')}
    if (lands['N2']['net'] != 'GND' or lands['P2']['net'].strip('-')
            or lands['P3']['net'] != 'VDD'):
        return False
    if any(p['layer'] != '1' for p in lands.values()):
        return False
    n, upper, lower = [lands[p] for p in ('N2', 'P2', 'P3')]
    if abs(float(n['x'])-float(upper['x'])-.5) > .002:
        return False
    if (abs(float(n['y'])-float(upper['y'])) > .002
            or abs(float(upper['x'])-float(lower['x'])) > .002):
        return False
    if abs(float(upper['y'])-float(lower['y'])-.5) > .002:
        return False
    # P2 / P3 的焊盘之间，扣除两边各 0.09 mm 的间距，最多只剩约 0.09 mm。
    gap = float(upper['y'])-float(upper['h'])/2-float(lower['y'])-float(lower['h'])/2
    available = gap-2*.09
    centre = [float(upper['x']), (float(upper['y'])+float(lower['y']))/2]
    narrow = re.search(r'最窄\s+([\d.]+)', issue['note'])
    return (.088 <= available <= .092 and math.dist(issue['at'], centre) <= .005
            and issue['length'] <= .51 and narrow is not None
            and abs(float(narrow.group(1))-available) <= .002)


def check(project, tool, rules, report):
    cfg = tomllib.loads(rules.read_text(encoding='utf-8'))
    quality = cfg['drc']['quality']
    assert POWER_NETS <= set(cfg['nets']['power']), '电源加粗名单缺少电源网络'
    assert POWER_NETS <= set(quality['width_neck_nets']), '细颈检查没有覆盖全部电源网络'
    assert quality.get('enabled', True), '不能关闭布线质量检查'
    assert cfg['power_track'] >= .6, '电源主干目标宽度不能小于 0.6 mm'
    assert 0 < quality['width_neck'] <= .1, '细颈须从 0.1 mm 起查，不能漏掉 0.2 / 0.3 mm 分支'
    assert 0 < quality['width_neck_min_length'] <= .1, '不能放宽细颈检查的长度'
    assert quality['width_neck_through_contacts'], '必须跨焊盘、过孔检查电源细颈'

    native = subprocess.check_output([tool, 'pads', str(project)], encoding='utf-8')
    pads = list(csv.DictReader(io.StringIO(native)))
    connector = [p for p in pads if p['part'] == 'J6']
    assert len(connector) == 30, 'J6 应有 30 个焊盘'
    xs, ys = [[float(p[k]) for p in connector] for k in ('x', 'y')]
    box = (min(xs), min(ys), max(xs), max(ys))

    def distance(p):
        x, y = float(p['x']), float(p['y'])
        return math.hypot(max(box[0]-x, 0, x-box[2]), max(box[1]-y, 0, y-box[3]))

    for ref in ('U18', 'U16', 'U17', 'U28', 'L102'):
        lands = [p for p in pads if p['part'] == ref]
        assert lands and all(p['layer'] == '2' for p in lands), f'{ref} 应位于 J6 附近的底面'
        gap = min(map(distance, lands))
        assert gap <= (1.0 if ref == 'L102' else 10.1), f'{ref} 距 J6 太远：{gap:.2f} mm'
        print(f'{ref} 距 J6 焊盘范围 {gap:.2f} mm。')

    data = json.loads(report.read_text(encoding='utf-8'))
    for kind in ('violations', 'edge', 'keepout', 'split_nets', 'dangling'):
        assert not data[kind], f'必须先消除 {kind}：{len(data[kind])} 处'
    all_necks = [q for q in data['routing_quality']
                 if q['kind'] in ('width_neck', 'width_neck_contact') and q['net'] in POWER_NETS]
    allowed = [q for q in all_necks if approved_bga_escape(q, pads)]
    assert len(allowed) <= 1, 'BGA 短出线例外不能扩大到多处'
    necks = [q for q in all_necks if q not in allowed]
    assert not necks, f'电源仍有 {len(necks)} 处细颈：' + ', '.join(
        f"{q['net']}@{q['at']}" for q in necks)
    if allowed:
        print(f"按确认保留 U5.N2 的必要 BGA 出线：约 0.09 mm 宽、{allowed[0]['length']:.3f} mm 长。")
    suffix = '除上述 BGA 短出线外，' if allowed else ''
    print(f'全板 {len(POWER_NETS)} 个电源网络：{suffix}跨焊盘、过孔的中段细颈 0 处；显示供电位置检查通过。')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--tool', default='easyedatool')
    parser.add_argument('--rules', required=True, type=Path)
    parser.add_argument('--drc-json', required=True, type=Path)
    args = parser.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    check(args.project, args.tool, args.rules, args.drc_json)


if __name__ == '__main__':
    main()
