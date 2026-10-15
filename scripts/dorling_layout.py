"""Dorling cartogram layout for js/4a_dorling_live_release.vg.json.

Each state becomes a circle whose AREA is proportional to the dogs and cats its RSPCA
received in 2024-25. Circles start at each state's approximate centre (longitude/latitude
mapped to pixels) and are pushed apart until none overlap, with a weak pull back towards
their home position so the arrangement still resembles the map of Australia.

The printed px/py values are pasted into the spec (scaled by 0.88 to fit the page column);
the spec uses the same radius formula: r = 54.5 * sqrt(dogs_cats / 14420)  (= 62 * 0.88).
"""
import math

W, H = 520, 430          # layout canvas (pixels)
RMAX, VMAX = 62, 14420   # largest circle (QLD) radius and value

# state: (dogs + cats received 2024-25, centroid latitude, centroid longitude)
states = {
    "ACT": (2530, -35.47, 149.01), "NSW": (463, -32.17, 147.02),
    "NT": (9941, -19.49, 132.55),  "QLD": (14420, -22.58, 144.08),
    "SA": (5318, -30.06, 135.78),  "TAS": (1079, -42.02, 146.59),
    "VIC": (5845, -36.85, 144.28), "WA": (1895, -25.33, 122.30),
}

pos = {}
for s, (v, lat, lon) in states.items():
    x = 40 + (lon - 113) / (154 - 113) * (W - 80)
    y = 30 + (-11 - lat) / (44 - 11) * (H - 60)
    pos[s] = [x, y, math.sqrt(v / VMAX) * RMAX, x, y]   # x, y, r, home_x, home_y

for _ in range(3000):
    for a in pos:                       # push overlapping pairs apart
        for b in pos:
            if a >= b:
                continue
            A, B = pos[a], pos[b]
            dx, dy = B[0] - A[0], B[1] - A[1]
            dist = math.hypot(dx, dy) or 0.01
            need = A[2] + B[2] + 6      # 6 px gap
            if dist < need:
                m = (need - dist) / 2
                A[0] -= dx / dist * m; A[1] -= dy / dist * m
                B[0] += dx / dist * m; B[1] += dy / dist * m
    for p in pos.values():              # gentle pull home + keep inside canvas
        p[0] += (p[3] - p[0]) * 0.01
        p[1] += (p[4] - p[1]) * 0.01
        p[0] = min(max(p[0], p[2] + 4), W - p[2] - 4)
        p[1] = min(max(p[1], p[2] + 4), H - p[2] - 24)

for s, p in sorted(pos.items()):
    print(f'{s}: px={round(p[0] * 0.88)}, py={round(p[1] * 0.88)}')
