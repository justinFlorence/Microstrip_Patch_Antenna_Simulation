import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------------------------------------------------
# User Configurable Settings
# ---------------------------------------------------------
data_file = 'far_field_pattern.csv'  # Your exported CSV file
theta_col = 'Theta[deg]'
phi_col = 'Phi[deg]'
gain_col = 'GainTotal'
#freq_of_interest = 28.0  # GHz (only if you have multiple frequencies in your data)
#freq_col = 'Freq [GHz]'  # If multiple frequencies are present; adjust if needed

# ---------------------------------------------------------
# Load the Data
# ---------------------------------------------------------
data = pd.read_csv(data_file)

# If multiple frequencies exist, filter for the desired one
#if freq_col in data.columns:
    #data = data[data[freq_col] == freq_of_interest]

# Extract unique angles
thetas = np.sort(data[theta_col].unique())
phis = np.sort(data[phi_col].unique())

# Create a mesh grid for Theta and Phi
Theta, Phi = np.meshgrid(thetas, phis)

# We need to create a matrix of gain values corresponding to each (Phi, Theta) pair
# Pivot the data to form a 2D matrix
gain_matrix = data.pivot(index=phi_col, columns=theta_col, values=gain_col)

# Ensure the gain_matrix aligns with the mesh grid
# gain_matrix: rows are phi, columns are theta
# After pivot, the order of phis and thetas should match the sorted arrays above.
gain_matrix = gain_matrix.reindex(index=phis, columns=thetas)

# Convert angles to radians for spherical to Cartesian conversion
Theta_rad = np.deg2rad(Theta)
Phi_rad = np.deg2rad(Phi)

# Convert gain (dBi) to a linear scale if desired, or keep as is. 
# For visualization, we can use dBi directly as a radius.
# But often just use the dBi value as "r". Higher dBi = longer radius.
r = gain_matrix.values

# Spherical to Cartesian conversion:
# X = r*sin(Theta)*cos(Phi)
# Y = r*sin(Theta)*sin(Phi)
# Z = r*cos(Theta)
X = r * np.sin(Theta_rad) * np.cos(Phi_rad)
Y = r * np.sin(Theta_rad) * np.sin(Phi_rad)
Z = r * np.cos(Theta_rad)

# ---------------------------------------------------------
# Plot the 3D Radiation Pattern
# ---------------------------------------------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
# Plot a surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

ax.set_title(f'3D Radiation Pattern')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
fig.colorbar(surf, ax=ax, label='Gain (dBi)')

# To make it more like a radiation pattern, you might want to set equal aspect ratio:
max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0
mean_x = (X.max()+X.min()) * 0.5
mean_y = (Y.max()+Y.min()) * 0.5
mean_z = (Z.max()+Z.min()) * 0.5
ax.set_xlim(mean_x - max_range, mean_x + max_range)
ax.set_ylim(mean_y - max_range, mean_y + max_range)
ax.set_zlim(mean_z - max_range, mean_z + max_range)

plt.tight_layout()
plt.savefig('radiation_pattern_3D.png', dpi=300)
plt.show()
