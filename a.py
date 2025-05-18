import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation

# Load background image
bg_img = mpimg.imread('olaf bg.png')

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_aspect('equal')
ax.imshow(bg_img, extent=[-15, 15, -15, 15], zorder=0)
plt.grid(False)
plt.xticks([])
plt.yticks([])

# --- Olaf Outline Coordinates ---
x_coord = [2, 4, 4, 0, -3, -3, -4, -4, -3, 0, 2]
y_coord = [-2, -1, 6, 10, 8, 6, 5, 4, 2, -1, -2]

# Create an empty line for outline
outline_line, = ax.plot([], [], color='black', linewidth=2)
outline_fill = None

# Containers for features to be revealed later
features = []

# Add patches but make them invisible initially
eye1 = patches.Circle((-1.5, 6.5), radius=1, edgecolor='black', facecolor='white', visible=False)
eye2 = patches.Circle((0, 7), radius=1, edgecolor='black', facecolor='white', visible=False)
pupil1 = patches.Circle((-1.5, 6.5), radius=0.3, edgecolor='black', facecolor='black', visible=False)
pupil2 = patches.Circle((0, 7), radius=0.3, edgecolor='black', facecolor='black', visible=False)

features += [eye1, eye2, pupil1, pupil2]
for f in features:
    ax.add_patch(f)

# Nose
x_nose = [0, -1, -2, -3]
y_nose = [5, 6, 6, 3]
nose = plt.Polygon(np.column_stack([x_nose, y_nose]), closed=True,
                   facecolor='#FD6A02', edgecolor='black', linewidth=2, visible=False)
ax.add_patch(nose)

# Smile
x_smile = [-3, 0, 2, 3, 2, 1, 0, -1]
y_smile = [2, 2, 4, 6, 1, 0, 0, 0]
smile = plt.Polygon(np.column_stack([x_smile, y_smile]), closed=True,
                    facecolor='#3e5a69', edgecolor='black', linewidth=2, visible=False)
ax.add_patch(smile)

# Teeth
x_teeth = [-2, -1, 1, 1, 0]
y_teeth = [2, 1.2, 2, 2.8, 2]
teeth = plt.Polygon(np.column_stack([x_teeth, y_teeth]), closed=True,
                    facecolor='#f0f8ff', edgecolor='black', linewidth=2, visible=False)
ax.add_patch(teeth)

# Hair
hair_lines = []
hair_color = '#4B2E2B'
hair_coords = [
    ([0, 0], [10, 13]),
    ([0, -1], [10, 13]),
    ([0, 1], [10, 13])
]
for x, y in hair_coords:
    line, = ax.plot(x, y, color=hair_color, linewidth=2, visible=False)
    hair_lines.append(line)

# Body segments
x_body = [0, 0, 3, 5, 6, 5, 4, 2]
y_body = [-1, -4, -6, -6, -5, -2, -1, -2]
body2 = plt.Polygon(np.column_stack([x_body, y_body]), closed=True,
                    facecolor='#f0f8ff', edgecolor='black', linewidth=2, visible=False)
ax.add_patch(body2)

x_lower_body = [5, 7, 7, 6, 4, 4, 2]
y_lower_body = [-6, -7, -9, -11, -11, -10, -9]
body3 = plt.Polygon(np.column_stack([x_lower_body, y_lower_body]), closed=True,
                    facecolor='#f0f8ff', edgecolor='black', linewidth=2, visible=False)
ax.add_patch(body3)

# --- Update Function for Animation ---
def update(frame):
    if frame < len(x_coord):
        # Update outline drawing
        outline_line.set_data(x_coord[:frame+1], y_coord[:frame+1])
    elif frame == len(x_coord):
        # Close the outline and fill
        outline_line.set_data(x_coord, y_coord)
        global outline_fill
        outline_fill = plt.Polygon(np.column_stack([x_coord, y_coord]), closed=True,
                                   facecolor='#f0f8ff', edgecolor='black', linewidth=2)
        ax.add_patch(outline_fill)
    elif frame == len(x_coord) + 5:
        for eye in features:
            eye.set_visible(True)
    elif frame == len(x_coord) + 10:
        nose.set_visible(True)
    elif frame == len(x_coord) + 15:
        smile.set_visible(True)
    elif frame == len(x_coord) + 20:
        teeth.set_visible(True)
    elif frame == len(x_coord) + 25:
        for hair in hair_lines:
            hair.set_visible(True)
    elif frame == len(x_coord) + 30:
        body2.set_visible(True)
    elif frame == len(x_coord) + 35:
        body3.set_visible(True)
    
    elif len(x_coord) < frame <= len(x_coord) + 5:
    # Animate eyes growing
        scale = (frame - len(x_coord)) / 5  # from 0 to 1
        eye1.set_radius(1 * scale)
        eye2.set_radius(1 * scale)
        pupil1.set_radius(0.3 * scale)
        pupil2.set_radius(0.3 * scale)
        for e in [eye1, eye2, pupil1, pupil2]:
            e.set_visible(True)

    elif len(x_coord) + 5 < frame <= len(x_coord) + 10:
    # Animate nose sliding in
        progress = (frame - (len(x_coord) + 5)) / 5
        x_nose_slide = [x * progress for x in [0, -1, -2, -3]]
        nose.set_xy(np.column_stack([x_nose_slide, y_nose]))
        nose.set_visible(True)


# Total frames: enough for drawing and revealing features
total_frames = len(x_coord) + 40

ani = FuncAnimation(fig, update, frames=total_frames, interval=100)

plt.show()
