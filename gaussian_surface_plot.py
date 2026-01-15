import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

# Create higher resolution meshgrid for smoother surface
x1_vector = np.arange(-12, 12.05, 0.1)  # Higher resolution: 0.02 instead of 0.05
x2_vector = np.arange(-12, 12.05, 0.1)

X, Y = np.meshgrid(x1_vector, x2_vector)

# Calculate the surface using the formula
# r = 1*exp^(-((x+4)^2 + (y+4)^2)^2/1000) + 1*exp^(-((x-4)^2 + (y-4)^2)^2/1000)
#   + 0.1*exp^(-((x+4)^2 + (y+4)^2)^2/1) + 0.1*exp^(-((x-4)^2 + (y-4)^2)^2/1)

term1 = 1 * np.exp(-np.power(np.power(X + 4, 2) + np.power(Y + 4, 2), 2) / 1000)
term2 = 1 * np.exp(-np.power(np.power(X - 4, 2) + np.power(Y - 4, 2), 2) / 1000)
term3 = 0.1 * np.exp(-np.power(np.power(X + 4, 2) + np.power(Y + 4, 2), 2) / 1)
term4 = 0.1 * np.exp(-np.power(np.power(X - 4, 2) + np.power(Y - 4, 2), 2) / 1)

Z = term1 + term2 + term3 + term4

# Create figure with 3D subplot
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Set up the plot
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, antialiased=True, rstride=1, cstride=1)

# Add multiple light sources by adjusting lighting
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Two Gaussian Curves Surface with Enhanced Visualization')

# Add colorbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('Surface Value')

# Set initial view (rotated 90 degrees)
ax.view_init(elev=30, azim=135)

# Animation function for 360-degree rotation with color cycling
def animate(frame):
    # Rotate the view (360 degrees over 360 frames)
    azim = frame * 1  # 1 degree per frame for smooth 360 rotation
    ax.view_init(elev=30 + 10*np.sin(frame*np.pi/180), azim=azim)

    # Color cycling - change colormap based on frame
    colors = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'coolwarm', 'seismic']
    color_idx = (frame // 50) % len(colors)  # Change color every 50 frames

    # Remove old surface
    ax.clear()

    # Re-plot with new color and lighting
    surf = ax.plot_surface(X, Y, Z,
                          cmap=colors[color_idx],
                          alpha=0.8,
                          antialiased=True,
                          rstride=1,
                          cstride=1,
                          shade=True,  # Enable shading
                          lightsource=plt.matplotlib.colors.LightSource(azdeg=azim, altdeg=60))  # Dynamic lighting

    # Set labels and title
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title(f'Two Gaussian Curves Surface - Frame {frame}')

    # Set axis limits to keep consistent scale
    ax.set_xlim([-12, 12])
    ax.set_ylim([-12, 12])
    ax.set_zlim([0, 2.2])

    return surf,

# Create animation and save it (reduced frames for faster execution)
anim = FuncAnimation(fig, animate, frames=60, interval=100, blit=False)  # Reduced to 60 frames

# Save the animation as GIF
print("Creating 60-frame animation...")
anim.save('gaussian_surface_animation.gif', writer='pillow', fps=10, dpi=80)  # Lower quality for speed
print("Animation saved as 'gaussian_surface_animation.gif'")

# Also save a static high-quality image
fig_static = plt.figure(figsize=(12, 9))
ax_static = fig_static.add_subplot(111, projection='3d')

# Plot static high-quality version
surf_static = ax_static.plot_surface(X, Y, Z,
                                   cmap='viridis',
                                   alpha=0.8,
                                   antialiased=True,
                                   rstride=1,
                                   cstride=1,
                                   shade=True,
                                   lightsource=plt.matplotlib.colors.LightSource(azdeg=45, altdeg=60))

ax_static.set_xlabel('X axis')
ax_static.set_ylabel('Y axis')
ax_static.set_zlabel('Z axis')
ax_static.set_title('Two Gaussian Curves Surface (Static View)')
ax_static.view_init(elev=30, azim=45)

# Add colorbar to static plot
cbar_static = fig_static.colorbar(surf_static, ax=ax_static, shrink=0.5, aspect=10)
cbar_static.set_label('Surface Value')

plt.tight_layout()
plt.savefig('gaussian_surface_static.png', dpi=300, bbox_inches='tight')
print("Static image saved as 'gaussian_surface_static.png'")
plt.close(fig_static)
