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

# Store results for the loop
results = []  # Initialize empty list to store all results

# Ask if user wants to solve for a specific angle as well
solve_specific = input("Do you also want to solve for a specific angle? (y/n): ").strip().lower()  # Ask user if they want a specific angle
specific_angle = None  
if solve_specific == 'y': 
    specific_angle = float(input("Enter the specific input angle deg2 in degrees: "))

# Degree-based trig helpers
def cosd(x):  # Cosine function that accepts degrees input
    return math.cos(math.radians(x))  # Convert degrees to radians and return cosine

def sind(x):  # Sine function that accepts degrees input
    return math.sin(math.radians(x))  # Convert degrees to radians and return sine

def atand(x):  # Inverse tangent function that returns degrees
    return math.degrees(math.atan(x))  # Return inverse result in degrees

# Function to draw the linkage
def draw_linkage(a, b, c, d, deg2, deg3, deg4, config_name):  # Define function to visualize 4-bar linkage
    # Joint A at origin
    A = np.array([0, 0])  # Place joint A at origin (0, 0)
    
    # Joint B - end of link a (input crank)
    B = np.array([a * cosd(deg2), a * sind(deg2)])  # Calculate joint B position from link a and angle deg2
    
    # Joint D - fixed at distance d from A
    D = np.array([d, 0])  # Place joint D on x-axis at distance d
    
    # Joint C - intersection of circles from B (radius b) and D (radius c)
    # Using the calculated deg3 and deg4
    C = np.array([D[0] + c * cosd(deg3), c * sind(deg3)])  # Calculate joint C position from D and angle deg3
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))  # Create 8x8 figure and axes for plotting
    
    # Plot links
    ax.plot([A[0], B[0]], [A[1], B[1]], 'b-', linewidth=3, label='Link a (crank)')  # Plot link a (crank) in blue
    ax.plot([B[0], C[0]], [B[1], C[1]], 'r-', linewidth=3, label='Link b (coupler)')  # Plot link b (coupler) in red
    ax.plot([C[0], D[0]], [C[1], D[1]], 'g-', linewidth=3, label='Link c (rocker)')  # Plot link c (rocker) in green
    ax.plot([A[0], D[0]], [A[1], D[1]], 'k-', linewidth=4, label='Link d (ground)')  # Plot link d (ground) in black
    
    # Plot joints
    ax.plot(*A, 'ko', markersize=10)  # Plot joint A as black circle
    ax.plot(*B, 'bo', markersize=10)  # Plot joint B as blue circle
    ax.plot(*C, 'go', markersize=10)  # Plot joint C as green circle
    ax.plot(*D, 'ko', markersize=10)  # Plot joint D as black circle
    
    # Label joints
    ax.text(A[0]-5, A[1]-5, 'A', fontsize=12, fontweight='bold')  # Label joint A
    ax.text(B[0]+3, B[1]+3, 'B', fontsize=12, fontweight='bold')  # Label joint B
    ax.text(C[0]+3, C[1]+3, 'C', fontsize=12, fontweight='bold')  # Label joint C
    ax.text(D[0]+3, D[1]-5, 'D', fontsize=12, fontweight='bold')  # Label joint D
    
    # Set equal aspect ratio and add grid
    ax.set_aspect('equal')  # Set axes to equal scale for proper linkage visualization
    ax.grid(True, alpha=0.3)  # Enable grid with transparency
    ax.axhline(y=0, color='k', linewidth=0.5)  # Draw horizontal axis
    ax.axvline(x=0, color='k', linewidth=0.5)  # Draw vertical axis
        
    # Labels and title
    ax.set_xlabel('Distance (mm)', fontsize=12)  # Set x-axis label
    ax.set_ylabel('Distance (mm)', fontsize=12)  # Set y-axis label
    ax.set_title(f'4-Bar Linkage - {config_name}\n(deg2={deg2:.2f}°, deg3={deg3:.2f}°, deg4={deg4:.2f}°)', fontsize=14)  # Set title with angles
    ax.legend(loc='upper left', fontsize=10)  # Add legend in upper left corner
        
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    return fig  # Return the figure object

# K Ratios
K1 = d / a  
K2 = d / c  
K3 = (a**2 - b**2 + c**2 + d**2) / (2 * a * c)  
K4 = d / b 
K5 = (c**2 - d**2 - a**2 - b**2) / (2 * a * b) 

# Display K values
print("K VALUES (Ratios):")  # Print section title
print("="*75) 
print(f"K1 = d/a = {K1:.6f}")
print(f"K2 = d/c = {K2:.6f}")
print(f"K3 = (a² - b² + c² + d²) / (2ac) = {K3:.6f}")
print(f"K4 = d/b = {K4:.6f}")
print(f"K5 = (c² - d² - a² - b²) / (2ab) = {K5:.6f}")

# Is it a Grashoff linkage?
if (a + b) <= (c + d):  # Check Grashoff condition sum of shortest and longest links
    print("\nThis is a Grashoff linkage - at least one link can fully rotate.")
else:  # If Grashoff condition not met
    print("\nThis is a non-Grashoff linkage - no link can fully rotate.")

# Loop through deg2 from 0 to 360 degrees at 10-degree intervals (only if no specific angle)
if specific_angle is None:  # Only run loop if user didn't specify a single angle
    print("\nCalculating open configuration angles for deg2 = 0 to 360 degrees...")  # Display calculation message

    for deg2 in range(0, 361, 10):  # Loop through 0, 10, 20, ..., 360 degrees
        # Parameters
        A = cosd(deg2) - K1 - K2 * cosd(deg2) + K3
        B = -2 * sind(deg2)
        C = K1 - (K2 + 1) * cosd(deg2) + K3
        
        D = cosd(deg2) - K1 + K4 * cosd(deg2) + K5
        E = -2 * sind(deg2)
        F = K1 + (K4 - 1) * cosd(deg2) + K5
        
        # Discriminants used to determine if real solutions exist
        disc4 = B**2 - 4 * A * C
        disc3 = E**2 - 4 * D * F
        
        # Solve for deg4 open and closed configurations
        if disc4 >= 0 and A != 0:  # Check if discriminant is non-negative and denominator is non-zero
            try:  # Attempt to calculate deg4 values
                deg4_open = 2 * atand((-B - math.sqrt(disc4)) / (2 * A))  # Calculate open configuration angle
                deg4_closed = 2 * atand((-B + math.sqrt(disc4)) / (2 * A))  # Calculate closed configuration angle
            except (ZeroDivisionError, ValueError):  # Catch any division by zero or value errors
                deg4_open = float("nan")  # Set to NaN if error occurs
                deg4_closed = float("nan")  # Set to NaN if error occurs
        else:  # If no real solution exists
            deg4_open = float("nan")  # Set open configuration to NaN
            deg4_closed = float("nan")  # Set closed configuration to NaN
        
        # Solve for deg3 open and closed configurations
        if disc3 >= 0 and D != 0:  # Check if discriminant is non-negative and denominator is non-zero
            try:  # Attempt to calculate deg3 values
                deg3_open = 2 * atand((-E - math.sqrt(disc3)) / (2 * D))  # Calculate open configuration angle
                deg3_closed = 2 * atand((-E + math.sqrt(disc3)) / (2 * D))  # Calculate closed configuration angle
            except (ZeroDivisionError, ValueError):  # Catch any division by zero or value errors
                deg3_open = float("nan")  # Set to NaN if error occurs
                deg3_closed = float("nan")  # Set to NaN if error occurs
        else:  # If no real solution exists
            deg3_open = float("nan")  # Set open configuration to NaN
            deg3_closed = float("nan")  # Set closed configuration to NaN
        
        # Store results for current iteration
        results.append({  # Add current results dictionary to results list
            'deg2': deg2,
            'deg3_open': deg3_open,
            'deg3_closed': deg3_closed, 
            'deg4_open': deg4_open,
            'deg4_closed': deg4_closed ,
        })

    # Display results as a table
    print(f"\n{'deg2 (°)':<12} {'deg3_open (°)':<18} {'deg3_closed (°)':<18} {'deg4_open (°)':<18} {'deg4_closed (°)':<18}")  # Print table headers
    
    for result in results:  # Iterate through all calculated results
        deg3_open_str = f"{result['deg3_open']:.4f}" if not math.isnan(result['deg3_open']) else "Not possible"  # Format deg3_open or mark as impossible
        deg3_closed_str = f"{result['deg3_closed']:.4f}" if not math.isnan(result['deg3_closed']) else "Not possible"  
        deg4_open_str = f"{result['deg4_open']:.4f}" if not math.isnan(result['deg4_open']) else "Not possible"
        deg4_closed_str = f"{result['deg4_closed']:.4f}" if not math.isnan(result['deg4_closed']) else "Not possible"  
        print(f"{result['deg2']:<12.0f} {deg3_open_str:<18} {deg3_closed_str:<18} {deg4_open_str:<18} {deg4_closed_str:<18}")  # Print table row with all values


# Solve for specific angle if requested
if specific_angle is not None:  # If user provided a specific angle
    print(f"\nSolving for specific angle: deg2 = {specific_angle:.2f} degrees")  # Display the angle being solved
   
    
    deg2 = specific_angle  # Set deg2 to the specific angle provided
    
    # Parameters
    A = cosd(deg2) - K1 - K2 * cosd(deg2) + K3 
    B = -2 * sind(deg2) 
    C = K1 - (K2 + 1) * cosd(deg2) + K3 
    
    D = cosd(deg2) - K1 + K4 * cosd(deg2) + K5 
    E = -2 * sind(deg2) 
    F = K1 + (K4 - 1) * cosd(deg2) + K5 
    
    # Display A-F parameters
    print("\nA-F PARAMETERS:")  # Print section header
    print(f"A = cos(deg2) - K1 - K2·cos(deg2) + K3 = {A:.6f}")
    print(f"B = -2·sin(deg2) = {B:.6f}")
    print(f"C = K1 - (K2 + 1)·cos(deg2) + K3 = {C:.6f}")
    print(f"D = cos(deg2) - K1 + K4·cos(deg2) + K5 = {D:.6f}")
    print(f"E = -2·sin(deg2) = {E:.6f}")
    print(f"F = K1 + (K4 - 1)·cos(deg2) + K5 = {F:.6f}")
    
    # Discriminants
    disc4 = B**2 - 4 * A * C 
    disc3 = E**2 - 4 * D * F 
    
    # Solve for deg4 open and closed configurations
    if disc4 >= 0:  # Check if real solutions exist for deg4
        deg4_open = 2 * atand((-B - math.sqrt(disc4)) / (2 * A))  
        deg4_crossed = 2 * atand((-B + math.sqrt(disc4)) / (2 * A))
    else:  # If discriminant is negative
        deg4_open = float("nan")  
        deg4_crossed = float("nan") 
        print("No real solution for deg4 at this input angle")
    
    # Solve for deg3 
    if disc3 >= 0:  # Check if real solutions exist for deg3
        deg3_open = 2 * atand((-E - math.sqrt(disc3)) / (2 * D))
        deg3_crossed = 2 * atand((-E + math.sqrt(disc3)) / (2 * D)) 
    else:  # If discriminant is negative
        deg3_open = float("nan")  # Set to NaN (no real solution)
        deg3_crossed = float("nan")
        print("No real solution for deg3 at this input angle") 
    
    # Display results
    print(f"\nResults for deg2 = {deg2:.2f} degrees") 
    print(f"deg4 open   = {deg4_open:.4f} degrees")  
    print(f"deg4 closed = {deg4_crossed:.4f} degrees") 
    print(f"deg3 open   = {deg3_open:.4f} degrees") 
    print(f"deg3 closed = {deg3_crossed:.4f} degrees")  
    
    # Draw linkage configurations
    if not math.isnan(deg3_open) and not math.isnan(deg4_open):  # If valid open configuration exists
        fig1 = draw_linkage(a, b, c, d, deg2, deg3_open, deg4_open, "Open Configuration")  # Draw open configuration
    
    if not math.isnan(deg3_crossed) and not math.isnan(deg4_crossed):  # If valid closed configuration exists
        fig2 = draw_linkage(a, b, c, d, deg2, deg3_crossed, deg4_crossed, "Crossed Configuration")  # Draw closed configuration
    
    plt.show()  # Display all figures

# Export results to CSV file
csv_file = "results.csv"  # Define CSV output filename

with open(csv_file, mode='w', newline='') as f:  # Open CSV file for writing
    writer = csv.writer(f)  # Create CSV writer object
    
    # Write header row
    writer.writerow(['deg2 (°)', 'deg3_open (°)', 'deg3_closed (°)', 'deg4_open (°)', 'deg4_closed (°)'])  # Write table headers
    
    # Write data rows from results list
    for result in results:  # Iterate through all result dictionaries
        deg3_open_str = f"{result['deg3_open']:.4f}" if not math.isnan(result['deg3_open']) else "Not possible"  # Format or mark impossible
        deg3_closed_str = f"{result['deg3_closed']:.4f}" if not math.isnan(result['deg3_closed']) else "Not possible"
        deg4_open_str = f"{result['deg4_open']:.4f}" if not math.isnan(result['deg4_open']) else "Not possible"
        deg4_closed_str = f"{result['deg4_closed']:.4f}" if not math.isnan(result['deg4_closed']) else "Not possible"
        writer.writerow([result['deg2'], deg3_open_str, deg3_closed_str, deg4_open_str, deg4_closed_str])  # Write data row to CSV

print(f"\nResults exported to {csv_file}")  # Notify user that CSV has been saved

print(f"\nResults exported to {csv_file}")