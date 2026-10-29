"""核对 AM319 的 30 针接口、1 脚方向及计入 MPU 封装的 MIPI 长度。"""
import argparse
import csv
import hashlib
import io
from pathlib import Path
import re
import subprocess
import sys

EXPECTED = {str(i): 'GND' for i in (1, 2, 6, 7, 10, 13, 16, 19, 20, 25, 30)}
EXPECTED.update({
    '3': 'DSI_CK_N', '4': 'OLED_VCI_EN', '5': 'DSI_CK_P', '8': 'LCD_1V8',
    '9': '', '11': '', '12': 'PANEL_RST_1V8', '14': '', '15': 'DSI_D0_N',
    '17': 'DSI_D0_P', '18': 'TP_2V8', '21': 'PANEL_TE_1V8', '22': 'TP_RST_1V8',
    '23': '', '24': 'TP_INT_1V8', '26': 'TP_SDA_1V8', '27': 'OLED_VBAT',
    '28': 'TP_SCL_1V8', '29': 'OLED_VBAT',
})
PACKAGE_N_MINUS_P = {'DSI_CK': .822, 'DSI_D0': .781}
PDF_SHA256 = 'c94b5bda46b1fdf471e12b4840590b968ddd37d65f538ae16e0be53876fd53bb'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--tool', default='easyedatool')
    args = parser.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    def run(*cmd):
        return subprocess.check_output([args.tool, *map(str, cmd)], encoding='utf-8')

    rows = list(csv.DictReader(io.StringIO(run('pads', args.project))))
    pads = {(p['part'], p['num']): p for p in rows}
    actual = {pin: pads[('J6', pin)]['net'].strip('-') for pin in EXPECTED}
    assert actual == EXPECTED, f'J6 引脚不一致：{actual}'
    for pin, xy in {'1': (35.8, 75.81), '2': (35.8, 78.19), '29': (30.2, 75.81)}.items():
        p = pads[('J6', pin)]
        assert p['layer'] == '1', f'J6.{pin} 没在顶层'
        assert all(abs(float(p[k])-v) <= .002 for k, v in zip(('x', 'y'), xy)), f'J6.{pin} 的方向变了'
    for pin in ('A15', 'B15'):
        assert not pads[('U1', pin)]['net'].strip('-'), f'MPU 未使用的 D1 {pin} 仍有网络'
    print('AM319 接口：30 脚逐个一致，1 脚在顶层东南角，D1 / ID / VPP 悬空。')

    report = run('constraints', args.project)
    means = []
    for pair, compensation in PACKAGE_N_MINUS_P.items():
        line = next(s for s in report.splitlines() if s.strip().startswith(pair+' '))
        found = re.search(r'走线\s+([\d.]+)\s*/\s*([\d.]+)', line)
        assert found, f'未读到 {pair} 的长度：{line}'
        p, n = map(float, found.groups())
        assert min(p, n) > 20, f'{pair} 尚未布通'
        error = p-n-compensation
        assert abs(error) <= .127, f'{pair} 计入封装后超差：{error:.3f} mm'
        means.append((p+n)/2)
        print(f'{pair}：PCB P/N={p:.3f}/{n:.3f} mm，封装补偿 {compensation:.3f}，电气长度差 {error:+.3f} mm。')
    delta = abs(means[0]-means[1])
    assert delta <= 5.08, f'时钟与数据通道平均长度差 {delta:.3f} mm 超过 5.08 mm'
    print(f'时钟 / D0 平均长度差 {delta:.3f} mm，通过。')
    here = Path(__file__).resolve().parent
    pdf = here.parent/'docs/display/AM-319-M262928-ZS.pdf'
    if not pdf.exists():
        pdf = here/'docs/display/AM-319-M262928-ZS.pdf'
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == PDF_SHA256, '原始屏 PDF 的字节改变了'
    print('原始屏 PDF SHA-256 一致；显示接口专项检查通过。')


if __name__ == '__main__':
    main()
