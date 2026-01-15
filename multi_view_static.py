import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create meshgrid (optimized for speed)
print("Creating meshgrid...")
x1_vector = np.arange(-12, 12.05, 0.05)
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
print(".4f")

# Different viewing angles
views = [
    (30, 45, "Front View"),
    (30, 135, "Side View (90° rotated)"),
    (60, 45, "Elevated Front"),
    (30, 225, "Rear View"),
    (10, 135, "Low Angle Side")
]

print("Generating multiple static views...")
for elev, azim, title in views:
    print(f"Creating {title}...")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(X, Y, Z,
                          cmap='viridis',
                          alpha=0.8,
                          antialiased=True,
                          rstride=3,  # Reduced stride for performance
                          cstride=3,
                          shade=True,
                          lightsource=plt.matplotlib.colors.LightSource(azdeg=azim, altdeg=60))

    # Set labels and title
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title(f'Two Gaussian Curves Surface - {title}')

    # Set view angle
    ax.view_init(elev=elev, azim=azim)

    # Add colorbar
    cbar = fig.colorbar(surf, ax=ax, shrink=0.6, aspect=15)
    cbar.set_label('Surface Value')

    plt.tight_layout()

    # Save with descriptive filename
    filename = f"gaussian_surface_{title.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('°', 'deg')}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved: {filename}")
    plt.close()

print("All views generated successfully!")