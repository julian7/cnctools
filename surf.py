#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Generate gcode for spoilboard surfacing.')
parser.add_argument('--centered', '-c', default=False, action='store_true', help='Zero is at the center of stock')
parser.add_argument('--x-max', '-x', type=int, required=True, help='X working width')
parser.add_argument('--y-max', '-y', type=int, required=True, help='Y working width')
parser.add_argument('--stepover', '-p', type=int, required=True, help='Pitch of passes/step over')
parser.add_argument('--speed', '-s', type=int, required=True, help='Rotation speed (RPM)')
parser.add_argument('--feed', '-f', type=int, required=True, help='Horizontal feed')
parser.add_argument('--lead-in', '-l', type=int, default=0, help='lead-in plunge (Y direction)')
parser.add_argument('--z-depth', '-z', type=float, default=0, help='Z depth to cut (0)')
parser.add_argument('--safe-height', '-H', type=float, default=15, help='Safe Z height (15)')
args = parser.parse_args()
v = vars(args)

feed = v['feed']
stepover = v['stepover']
if v['centered']:
    xmax = v['x_max']/2
    xmin = -xmax
    ymax = v['y_max']/2
    ymin = -ymax
else:
    xmax = v['x_max']
    ymax = v['y_min']
    xmin = ymin = 0

print("G17 G90")
print("G21")
print(f"M3 S{v['speed']}")
print("G54")
print(f"G0 Z{v['safe_height']}")
print(f"G0 X{xmin} Y{ymin-v['lead_in']}")
print(f"G1 Z{v['z_depth']} F{feed}")

def step(x):
    last = False
    x += stepover
    if x > xmax:
        x = xmax
        last = True
    return (x, last)
x = xmin
last = False
while x < xmax:
    print(f"G1 Y{ymax} F{feed}")
    if last:
        break
    x, last = step(x)
    print(f"G1 X{x} F{feed}")
    print(f"G1 Y{ymin} F{feed}")
    if last:
        break
    x, last = step(x)
    print(f"G1 X{x} F{feed}")

print(f"G0 Z{v['safe_height']}")
print(f"G0 X{xmax} Y{ymax}")
print("M5")
print("G17 G90")
print("M2")
