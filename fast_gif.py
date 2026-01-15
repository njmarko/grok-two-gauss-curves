import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

# Create LOW resolution meshgrid for FAST rendering
print("Creating low-res meshgrid for speed...")
x1_vector = np.arange(-12, 12.05, 0.3)  # Low resolution: 0.3 step for speed
x2_vector = np.arange(-12, 12.05, 0.3)

X, Y = np.meshgrid(x1_vector, x2_vector)
print(f"Meshgrid created with shape: {X.shape}")

# Calculate the surface using the formula
print("Calculating surface...")
term1 = 1 * np.exp(-np.power(np.power(X + 4, 2) + np.power(Y + 4, 2), 2) / 1000)
term2 = 1 * np.exp(-np.power(np.power(X - 4, 2) + np.power(Y - 4, 2), 2) / 1000)
term3 = 0.1 * np.exp(-np.power(np.power(X + 4, 2) + np.power(Y + 4, 2), 2) / 1)
term4 = 0.1 * np.exp(-np.power(np.power(X - 4, 2) + np.power(Y - 4, 2), 2) / 1)

Z = term1 + term2 + term3 + term4

# Create figure with 3D subplot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Set up the plot
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, antialiased=False, rstride=1, cstride=1)

# Set initial view (rotated 90 degrees)
ax.view_init(elev=30, azim=135)

# Animation function for smooth rotation with color cycling
def animate(frame):
    # Rotate the view (360 degrees over 30 frames for speed)
    azim = 135 + frame * 12  # 12 degrees per frame for 30 frames = 360 degrees
    ax.view_init(elev=30 + 10*np.sin(frame*np.pi/15), azim=azim)  # Smooth elevation change

    # Color cycling - change colormap based on frame
    colors = ['viridis', 'plasma', 'inferno', 'magma']
    color_idx = frame % len(colors)  # Change color every frame for variety

    # Remove old surface
    ax.clear()

    # Re-plot with new color and lighting
    surf = ax.plot_surface(X, Y, Z,
                          cmap=colors[color_idx],
                          alpha=0.8,
                          antialiased=False,  # Disabled for speed
                          rstride=1,
                          cstride=1,
                          shade=True,
                          lightsource=plt.matplotlib.colors.LightSource(azdeg=azim, altdeg=60))

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('.1f')

    # Set axis limits to keep consistent scale
    ax.set_xlim([-12, 12])
    ax.set_ylim([-12, 12])
    ax.set_zlim([0, 2.2])

    return surf,

# Create FAST animation
print("Creating fast 30-frame animation...")
anim = FuncAnimation(fig, animate, frames=30, interval=200, blit=False)  # 30 frames, 200ms each

# Save the animation as low-res GIF for speed
anim.save('fast_gaussian_animation.gif', writer='pillow', fps=5, dpi=72)  # Low DPI, 5 fps
print("Fast animation saved as 'fast_gaussian_animation.gif'")

# Also save a static low-res version
fig_static = plt.figure(figsize=(8, 6))
ax_static = fig_static.add_subplot(111, projection='3d')

surf_static = ax_static.plot_surface(X, Y, Z,
                                   cmap='viridis',
                                   alpha=0.8,
                                   antialiased=False,
                                   rstride=1,
                                   cstride=1,
                                   shade=True,
                                   lightsource=plt.matplotlib.colors.LightSource(azdeg=135, altdeg=60))

ax_static.set_xlabel('X')
ax_static.set_ylabel('Y')
ax_static.set_zlabel('Z')
ax_static.set_title('Two Gaussian Curves Surface (Low-Res)')
ax_static.view_init(elev=30, azim=135)

plt.tight_layout()
plt.savefig('fast_gaussian_static.png', dpi=100, bbox_inches='tight')
print("Fast static image saved as 'fast_gaussian_static.png'")
plt.close(fig_static)

print("Fast GIF generation complete!")