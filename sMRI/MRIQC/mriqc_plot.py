# ------------------------------------------------------------------------------
# Script to overlay a swarm plot over a violin plot in Seaborn for data visualization.
# The script reads MRIQC metrics from an Excel file and creates a combined plot.
#
# Steps:
# 1. Import necessary Python libraries for data manipulation and visualization.
# 2. Load MRIQC metrics data from an Excel file into a pandas DataFrame.
# 3. Preprocess the data by selecting specific columns and capping values.
# 4. Melt the DataFrame for compatibility with Seaborn's violinplot and swarmplot.
# 5. Define colors for different variables in the plot.
# 6. Create a figure and axis for plotting.
# 7. Plot violins for the distribution of the data and overlay swarm plots for individual data points.
# 8. Customize the plot's appearance, including spine width and save the figure.
# 9. Display the final plot.
#
# Parameters:
# - path: The file path to the Excel file containing MRIQC metrics data.
# - data: A pandas DataFrame containing the selected metrics.
# - data_long: A melted version of the DataFrame for plotting.
# - colors: A dictionary mapping variable names to colors.
#
# Output:
# - A combined violin and swarm plot saved as 'fMRI_EFC.png'.
#
# Notes:
# - Ensure the Excel file is in the correct path and contains the required sheet.
# - Adjust the color dictionary and other plot parameters as needed.
# ------------------------------------------------------------------------------
# Import required libraries
import pandas as pd  # For data manipulation and analysis
import matplotlib.pyplot as plt  # For plotting
import seaborn as sns  # For advanced data visualization
import numpy as np  # For numerical operations
from scipy import stats  # For statistical calculations

# Load MRIQC metrics data from an Excel file into a pandas DataFrame
path = r"C:\Users\zhuyt12023\Desktop\scidata\mriqc\mriqc_metrics.xlsx"  # Path to the Excel file
data = pd.read_excel(path, sheet_name=0)  # Load the first sheet (anat); other sheets include func and dwi

# Preprocess the data by selecting specific columns of interest
data = data[['CQAT_EFC', 'HCP-D_EFC']]  # Select columns for CQAT_EFC and HCP-D_EFC metrics

# Reshape the DataFrame into a long format for compatibility with Seaborn
data_long = pd.melt(data)  # Converts wide-form DataFrame to long-form for visualization

# Create a figure for plotting and set the size
plt.figure(figsize=(6, 10))  # Set figure dimensions (width=6, height=10)

# Define colors for different variables
violin_color = ['#ffffff', '#ffffff']  # Set violin plot colors (white for both groups)
dot_color = ['#EA8811', '#0631FD']  # Define colors for dots (orange and blue)

# Plot violin plots for the data distribution
sns.violinplot(
    x='variable', y='value', data=data_long, 
    hue='variable',  # Group by the 'variable' column
    legend=False,  # Disable legend
    edgecolor='black', linewidth=2,  # Set edge color and line width
    palette=violin_color,  # Apply the color palette
    inner=None  # Do not display internal data points or statistics
)

# Overlay scatter points for each group
for idx, group in enumerate(data_long['variable'].unique()):  # Loop through each variable
    # Extract data for the current group, removing NaN and infinite values
    group_data = data_long[data_long['variable'] == group]['value']
    group_data = group_data.dropna()
    group_data = group_data[np.isfinite(group_data)]
    
    if len(group_data) > 0:  # If there are valid data points
        y_values = group_data.values  # Get the y-values for the current group
        
        # Calculate violin width using Kernel Density Estimation (KDE)
        kde = stats.gaussian_kde(group_data)
        y_range = np.linspace(min(y_values), max(y_values), 100)  # Generate range of y-values
        violin_width = kde(y_range)  # Compute KDE values
        violin_width = violin_width / np.max(violin_width) * 0.4  # Normalize and scale violin width
        
        # Interpolate maximum offsets for scatter points based on violin width
        max_offsets = np.interp(y_values, y_range, violin_width)
        
        # Generate random horizontal offsets within the violin shape
        spread_factors = np.random.uniform(0, 1, size=len(y_values))  # Random spread factors
        spread_factors = np.power(spread_factors, 1.5)  # Adjust distribution for smoother scatter
        directions = np.random.choice([-1, 1], size=len(y_values))  # Randomly assign left/right direction
        
        # Compute final x-positions for scatter points
        x_offset = max_offsets * spread_factors * directions
        x_positions = idx + x_offset  # Add offsets to the index (group position)
        
        # Plot scatter points
        plt.scatter(
            x_positions, y_values,  # Use computed x-positions and original y-values
            c=dot_color[idx],  # Assign group-specific dot color
            s=150,  # Set dot size
            alpha=0.8,  # Set transparency
            edgecolor='black',  # Add black edge around dots
            linewidth=0.8  # Set edge line width
        )

# Set y-axis range
plt.ylim(0.55, 0.92)  # Set y-axis range for better visualization

# Customize plot appearance
ax = plt.gca()  # Get the current axis

# Adjust the appearance of the plot's spines (borders)
for spine in plt.gca().spines.values():
    spine.set_linewidth(3)  # Set spine thickness

# Customize tick appearance
ax.tick_params(
    axis='both',  # Apply to both x and y axes
    which='major',  # Major ticks only
    width=4,  # Set tick width
    length=6,  # Set tick length
    labelsize=14  # Set tick label font size
)

# Save the figure to a file
plt.savefig('s_EFC.png', dpi=600, bbox_inches='tight')  # Save as PNG with high resolution and tight layout

# Display the final plot
plt.show()  # Render the plot


