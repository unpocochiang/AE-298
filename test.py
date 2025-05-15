import matplotlib.pyplot as plt

sections = [{'y': 4.8-4.8, 'x': 11.03-11.03, 'z': 0, 'chord': 5.68},
            {'y': 9.57-4.8, 'x': 13.36-11.03, 'z': 0, 'chord': 3.36},
            {'y': 17.5-4.8, 'x': 17.5-11.03, 'z': 0, 'chord': 1.42},
            {'y': 19.29-4.8, 'x': 19.19-11.03, 'z': 0, 'chord': 0.462}]

# Leading and trailing edge points
x_le = [s["x"] for s in sections]
y_le = [s["y"] for s in sections]
x_te = [s["x"] + s["chord"] for s in sections]
y_te = y_le

# 90-degree clockwise rotation: (x, y) → (y, -x)
rot_x_le = y_le
rot_y_le = [-x for x in x_le]
rot_x_te = y_te
rot_y_te = [-x for x in x_te]

# Combine for filled shape
x_outline = rot_x_le + rot_x_te[::-1] + [rot_x_le[0]]
y_outline = rot_y_le + rot_y_te[::-1] + [rot_y_le[0]]

# Determine consistent limits
all_x = rot_x_le + rot_x_te
all_y = rot_y_le + rot_y_te
x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)
padding_x = (x_max - x_min) * 0.1
padding_y = (y_max - y_min) * 0.1

# Plot
fig, ax = plt.subplots()
ax.fill(x_outline, y_outline, color="skyblue", edgecolor="black", alpha=0.6)
ax.plot(x_outline, y_outline, "k-")

ax.set_title("Wing Geometry (Right side)")
ax.set_xlabel("Y (ft)")
ax.set_ylabel("X (ft)")
ax.set_aspect("equal")
ax.set_xlim(x_min - padding_x, x_max + padding_x)
ax.set_ylim(y_min - padding_y, y_max + padding_y)
ax.grid(True)
plt.show()

print(sections)