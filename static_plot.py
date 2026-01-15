import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create meshgrid (optimized for speed)
print("Creating meshgrid...")
x1_vector = np.arange(-12, 12.05, 0.05)  # Balanced resolution for speed
x2_vector = np.arange(-12, 12.05, 0.05)

X, Y = np.meshgrid(x1_vector, x2_vector)
print(f"Meshgrid created with shape: {X.shape}")

# Calculate the surface using the formula
print("Calculating surface...")
term1 = 1 * np.exp(-np.power(np.power(X + 4, 2) + np.power(Y + 4, 2), 2) / 1000)
term2 = 1 * np.exp(-np.power(np.power(X - 4, 2) + np.power(Y - 4, 2), 2) / 1000)
term3 = 0.1 * np.exp(-np.power(np.power(X + 4, 2) + np.power(Y + 4, 2), 2) / 1)
term4 = 0.1 * np.exp(-np.power(np.power(X - 4, 2) + np.power(Y - 4, 2), 2) / 1)

Z = term1 + term2 + term3 + term4
print(f"Surface calculated. Max value: {np.max(Z):.4f}, Min value: {np.min(Z):.4f}")

# Create figure with 3D subplot
print("Creating plot...")
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface with enhanced visualization
surf = ax.plot_surface(X, Y, Z,
                      cmap='viridis',
                      alpha=0.8,
                      antialiased=True,
                      rstride=2,  # Reduced stride for performance
                      cstride=2,
                      shade=True,
                      lightsource=plt.matplotlib.colors.LightSource(azdeg=45, altdeg=60))

# Set labels and title
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Two Gaussian Curves Surface')

# Add colorbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('Surface Value')

# Set view angle (rotated 90 degrees)
ax.view_init(elev=30, azim=135)

plt.tight_layout()
plt.savefig('gaussian_surface.png', dpi=150, bbox_inches='tight')
print("Static plot saved as 'gaussian_surface.png'")

# Save a higher quality version
plt.savefig('gaussian_surface_high_quality.png', dpi=300, bbox_inches='tight')
print("High quality plot saved as 'gaussian_surface_high_quality.png'")
plt.close()

print("Plot generation complete!")