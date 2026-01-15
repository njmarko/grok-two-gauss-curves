import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource, hsv_to_rgb

# Generate the grid with reasonable resolution to avoid memory issues
step = 0.5  # Even larger step for manageable polygon count
x_vector = np.arange(-12, 12 + step, step)
y_vector = np.arange(-12, 12 + step, step)
x, y = np.meshgrid(x_vector, y_vector)

# Compute r using the formula (translated to Python with np.exp for efficiency)
r = (1 * np.exp(-(((x + 4)**2 + (y + 4)**2)**2) / 1000) +
     1 * np.exp(-(((x - 4)**2 + (y - 4)**2)**2) / 1000) +
     0.1 * np.exp(-(((x + 4)**2 + (y + 4)**2)**2) / 1) +
     0.1 * np.exp(-(((x - 4)**2 + (y - 4)**2)**2) / 1))

# Set up the figure and 3D axis
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('3D Mesh Plot of the Formula')

# Normalize r for coloring (base color mapping)
norm = colors.Normalize(r.min(), r.max())

# Function to compute shaded colors with multiple lights
def get_shaded_colors(r, azim):
    # Simulate two light sources: one at 0 deg elevation 65, another at 180 deg elevation 45
    ls1 = LightSource(azdeg=0 + azim, altdeg=65)  # Rotate light with view for dynamic effect
    ls2 = LightSource(azdeg=180 + azim, altdeg=45)
    
    # Get shaded intensity from each (blended additively, clamped to 1)
    rgb1 = ls1.shade(r, cmap=plt.cm.viridis, norm=norm, blend_mode='overlay')
    rgb2 = ls2.shade(r, cmap=plt.cm.viridis, norm=norm, blend_mode='overlay')
    blended_rgb = np.clip(rgb1 + rgb2 * 0.7, 0, 1)  # Blend with weight on second light
    
    # Apply color cycling: Convert to HSV, shift hue by frame (azim/360), convert back
    hsv = colors.rgb_to_hsv(blended_rgb[..., :3])
    hsv[..., 0] = (hsv[..., 0] + azim / 360) % 1.0  # Cycle hue
    cycled_rgb = hsv_to_rgb(hsv)
    return np.dstack((cycled_rgb, blended_rgb[..., 3]))  # Re-add alpha if present

# Initial plot (will be updated in animation)
surf = ax.plot_surface(x, y, r, facecolors=get_shaded_colors(r, 0), rstride=1, cstride=1, antialiased=True, shade=False)

# Set axis limits and labels
ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_zlim(0, r.max() * 1.1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('R')

# Animation update function: Rotate view, update colors for cycling and shading
def update(num):
    ax.view_init(elev=30, azim=num)  # Fixed elevation, rotating azimuth for orbit
    surf.set_facecolors(get_shaded_colors(r, num).reshape(-1, 4))  # Update colors
    return surf,

# Create smooth 360-frame animation (one frame per degree)
ani = animation.FuncAnimation(fig, update, frames=360, interval=20, blit=False)

# Save as GIF (requires Pillow; adjust fps if needed)
ani.save('formula_plot_animation.gif', writer='pillow', fps=30)

# Alternatively, uncomment to view interactively (no save)
# plt.show()