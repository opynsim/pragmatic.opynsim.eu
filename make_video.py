#!/usr/bin/env python3

# dependencies (install these): imageio opynsim pandas pyarrow matplotlib

import opynsim as opyn            # musculoskeletal modelling
import opynsim.graphics           # musculoskeletal modelling (3D visualization)
import imageio                    # video encoding
import numpy as np                # numerics (unit conversion, pixel combining)
import pandas as pd               # data manipulation
import matplotlib.pyplot as plt   # 2D plotting/visualization

print("--- loading model + motion ---")
model = opyn.read_osim("InnoTreat_SSM.osim").compile()
mot = opyn.read_mot("Healthy_mean_head_right_rep_1.mot")
mot = model.convert_data_frame_to_radians(mot)  # Pandas doesn't keep track of MOT files' "inDegrees"

print("--- resampling motion with pandas at 60FPS for video rendering ---")
df = mot.to_pandas()
df = df.set_index(pd.to_timedelta(df.pop("time"), unit="s"))
df = df.resample(pd.Timedelta(seconds=1/60)).mean().interpolate()
df.index = df.index.total_seconds()
#df = df.loc[:1.0]  # take the first second <-------- USE THIS WHEN DEVELOPING (faster)

print("--- converting motion data into a ModelState series ---")
states = model.states_from_data_frame(opyn.DataFrame(df), realized_to=opyn.STAGE_REPORT)

print("--- collecting relevant output data from states ---")
ts = []
ld_forces = []
ds_forces = []
se_angle = []
for state in states:
    ts.append(state.time)
    ld_forces.append(model.get_output_value(state, "/forceset/LatissimusDorsi_S[fiber_force]"))
    ds_forces.append(model.get_output_value(state, "/forceset/DeltoideusSpinae_med[fiber_force]"))
    val_rad = model.get_output_value(state, "/jointset/GlenoHumeral/shoulder_elv[value]")
    se_angle.append(np.degrees(val_rad))

print("--- creating matplotlib plots of the data ---")
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(4.5, 4.8), dpi=100, sharex=True)

ax1.plot(ts, ld_forces, color="royalblue", linewidth=2, label="LD Force")
ax1.set_ylabel("Force (N)")
ax1.set_title("Latissimus Dorsi Fiber Force", fontsize=10)
ax1.grid(True, linestyle="--", alpha=0.6)

ax2.plot(ts, ds_forces, color="crimson", linewidth=2, label="DS Force")
ax2.set_ylabel("Force (N)")
ax2.set_title("Deltoideus Spinae Fiber Force", fontsize=10)
ax2.grid(True, linestyle="--", alpha=0.6)

ax3.plot(ts, se_angle, color="forestgreen", linewidth=2, label="Elevation")
ax3.set_xlabel("Time (s)")  # Bottom plot has the X (rest are aligned by sharex=True)
ax3.set_ylabel("Angle (°)")
ax3.set_title("Shoulder Elevation Angle", fontsize=10)
ax3.grid(True, linestyle="--", alpha=0.6)

# Create dynamic vertical "time cursor" lines for all 3 axes
cursor1 = ax1.axvline(x=ts[0], color='black', linestyle='--', linewidth=1.5)
cursor2 = ax2.axvline(x=ts[0], color='black', linestyle='--', linewidth=1.5)
cursor3 = ax3.axvline(x=ts[0], color='black', linestyle='--', linewidth=1.5)

# Tighten spacing layout adjustments (slightly tucked the margins to fit 3 titles comfortably)
plt.subplots_adjust(left=0.18, right=0.95, top=0.94, bottom=0.10, hspace=0.45)

print("--- rendering video frames ---")

# Figure out initial camera polar coordinates (as an example).
initial_pos = np.array([0.05, -0.1, 0.8])
camera_target = np.array([0.0, 0.0, 0.0])
radius = np.sqrt(initial_pos[0]**2 + initial_pos[2]**2)
initial_theta = np.arctan2(initial_pos[2], initial_pos[0])
angle_per_frame = (2. * np.pi) / len(states)

# Initialize a scene camera (updated every frame)
camera = opyn.graphics.Camera()
rendering_params = {
    "scene_cache": opyn.graphics.SceneCache(),
    "background_color": opyn.graphics.Color.white,
    "camera": camera,
    "dimensions": (300, 480),
}
with imageio.get_writer("output.mp4", fps=60) as writer:
    for idx, state in enumerate(states):
        print(f"t={state.time}")

        theta = initial_theta + (idx * angle_per_frame)

        # Update camera
        camera.position = np.array([radius * np.cos(theta), initial_pos[1], radius * np.sin(theta)])
        camera.direction = camera_target - camera.position
        camera.direction = camera.direction / np.linalg.norm(camera.direction)  # normalize
        camera.up = np.array([0.0, 1.0, 0.0])

        # Render 3D scene to pixels.
        frame = opyn.graphics.render_model_in_state(model, state, **rendering_params)
        render_pixels = frame.pixels_rgb24()

        # Update X line on plots, then redraw the plot so the lines are shown.
        cursor1.set_xdata([state.time])
        cursor2.set_xdata([state.time])
        cursor3.set_xdata([state.time])
        fig.canvas.draw()

        # Extract the plot's pixels as RGB
        plot_pixels = np.asarray(fig.canvas.buffer_rgba())[..., :3]

        # Composite the raw pixel data in-memory using numpy
        composite_frame = np.hstack((render_pixels, plot_pixels))

        # Write the composite to the video file
        writer.append_data(composite_frame)

