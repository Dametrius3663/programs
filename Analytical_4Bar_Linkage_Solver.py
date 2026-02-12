import math
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# Ask for Link Lengths (mm)
a = float(input("Enter the length of link a in mm: "))
b = float(input("Enter the length of link b in mm: "))
c = float(input("Enter the length of link c in mm: "))
d = float(input("Enter the length of link d in mm: "))

# Ask user for input angle
deg2 = float(input("Enter the input angle deg2 in degrees: "))

# Degree-based trig helpers
def cosd(x):
    return math.cos(math.radians(x))

def sind(x):
    return math.sin(math.radians(x))

def atand(x):
    return math.degrees(math.atan(x))

# Function to draw the linkage
def draw_linkage(a, b, c, d, deg2, deg3, deg4, config_name):
    # Joint A at origin
    A = np.array([0, 0])
    
    # Joint B - end of link a (input crank)
    B = np.array([a * cosd(deg2), a * sind(deg2)])
    
    # Joint D - fixed at distance d from A
    D = np.array([d, 0])
    
    # Joint C - intersection of circles from B (radius b) and D (radius c)
    # Using the calculated deg3 and deg4
    C = np.array([D[0] + c * cosd(deg3), c * sind(deg3)])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot links
    ax.plot([A[0], B[0]], [A[1], B[1]], 'b-', linewidth=3, label='Link a (crank)')
    ax.plot([B[0], C[0]], [B[1], C[1]], 'r-', linewidth=3, label='Link b (coupler)')
    ax.plot([C[0], D[0]], [C[1], D[1]], 'g-', linewidth=3, label='Link c (rocker)')
    ax.plot([A[0], D[0]], [A[1], D[1]], 'k-', linewidth=4, label='Link d (ground)')
    
    # Plot joints
    ax.plot(*A, 'ko', markersize=10)
    ax.plot(*B, 'bo', markersize=10)
    ax.plot(*C, 'go', markersize=10)
    ax.plot(*D, 'ko', markersize=10)
    
    # Label joints
    ax.text(A[0]-5, A[1]-5, 'A', fontsize=12, fontweight='bold')
    ax.text(B[0]+3, B[1]+3, 'B', fontsize=12, fontweight='bold')
    ax.text(C[0]+3, C[1]+3, 'C', fontsize=12, fontweight='bold')
    ax.text(D[0]+3, D[1]-5, 'D', fontsize=12, fontweight='bold')
    
    # Set equal aspect ratio and add grid
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
        
    # Labels and title
    ax.set_xlabel('Distance (mm)', fontsize=12)
    ax.set_ylabel('Distance (mm)', fontsize=12)
    ax.set_title(f'4-Bar Linkage - {config_name}\n(deg2={deg2:.2f}°, deg3={deg3:.2f}°, deg4={deg4:.2f}°)', fontsize=14)
    ax.legend(loc='upper left', fontsize=10)
        
    plt.tight_layout()
    return fig

# Ratios
K1 = d / a
K2 = d / c
K3 = (a**2 - b**2 + c**2 + d**2) / (2 * a * c)
K4 = d / b
K5 = (c**2 - d**2 - a**2 - b**2) / (2 * a * b)

# Parameters
A = cosd(deg2) - K1 - K2 * cosd(deg2) + K3
B = -2 * sind(deg2)
C = K1 - (K2 + 1) * cosd(deg2) + K3

D = cosd(deg2) - K1 + K4 * cosd(deg2) + K5
E = -2 * sind(deg2)
F = K1 + (K4 - 1) * cosd(deg2) + K5

# Discriminants
disc4 = B**2 - 4 * A * C
disc3 = E**2 - 4 * D * F

# Is it a Grashoff linkage?
if (a + b) <= (c + d):
    print("\nThis is a Grashoff linkage - at least one link can fully rotate.")
else:
    print("\nThis is a non-Grashoff linkage - no link can fully rotate.")

# Solve for deg4
if disc4 >= 0:
    deg4_open = 2 * atand((-B - math.sqrt(disc4)) / (2 * A))
    deg4_crossed = 2 * atand((-B + math.sqrt(disc4)) / (2 * A))
else:
    deg4_open = float("nan")
    deg4_crossed = float("nan")
    print("No real solution for deg4 at this input angle")

# Solve for deg3
if disc3 >= 0:
    deg3_open = 2 * atand((-E - math.sqrt(disc3)) / (2 * D))
    deg3_crossed = 2 * atand((-E + math.sqrt(disc3)) / (2 * D))
else:
    deg3_open = float("nan")
    deg3_crossed = float("nan")
    print("No real solution for deg3 at this input angle")

# Display results
print(f"\nResults for deg2 = {deg2:.2f} degrees")
print(f"deg4 open   = {deg4_open:.4f} degrees")
print(f"deg4 closed = {deg4_crossed:.4f} degrees")
print(f"deg3 open   = {deg3_open:.4f} degrees")
print(f"deg3 closed = {deg3_crossed:.4f} degrees")

# Draw linkage configurations
if not math.isnan(deg3_open) and not math.isnan(deg4_open):
    fig1 = draw_linkage(a, b, c, d, deg2, deg3_open, deg4_open, "Open Configuration")

if not math.isnan(deg3_crossed) and not math.isnan(deg4_crossed):
    fig2 = draw_linkage(a, b, c, d, deg2, deg3_crossed, deg4_crossed, "Crossed Configuration")

plt.show()

# Export results to CSV
csv_file = "results.csv"
file_exists = os.path.isfile(csv_file)

with open(csv_file, mode='a', newline='') as f:
    writer = csv.writer(f)
    
    # Write header if file is new
    if not file_exists:
        writer.writerow(['Link_a', 'Link_b', 'Link_c', 'Link_d', 'deg2', 'deg4_open', 'deg4_crossed', 'deg3_open', 'deg3_crossed'])
    
    # Write results
    writer.writerow([a, b, c, d, deg2, deg4_open, deg4_crossed, deg3_open, deg3_crossed])

print(f"\nResults exported to {csv_file}")