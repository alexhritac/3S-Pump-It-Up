import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

def plot_surface_from_excel(file_path, sheet_name="Spectrum", y_ticks_skip=10):
    # Read Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Extract X, Y, and Z data
    X = df.iloc[:, 2]  # X-axis is the third column
    Y = df.columns[3:]  # Y-axis is the first row starting from the 4th column
    Z = df.iloc[:, 3:].values.T  # Z-axis is the data from the 4th column onwards, transposed for proper orientation

    # Create a meshgrid for X and Y using NumPy
    X, Y = np.meshgrid(X, range(len(Y)))

    # Plot the surface
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # Extract the directory of the Excel file from the file path
    excel_dir = os.path.dirname(file_path)

    # Extract the name of the Excel file without the sheet name
    excel_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    excel_name = os.path.splitext(excel_name_without_extension)[0]

    # Add labels and title
    ax.set_xlabel(df.columns[2])
    ax.set_ylabel("Wavelengts")  # Set y-axis label to "Absorption"
    ax.set_zlabel("Absorption")  # You might want to replace this with the actual label from your data
    ax.set_title(f"Surface Plot from {excel_name}")

    # Add color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

    # Set x-axis limits in reverse order to invert the x-axis
    ax.set_xlim(X.max(), X.min())

    # Set y-axis limits in reverse order to invert the y-axis
    ax.set_ylim(0, len(Y) - 1)

    # Set specific values on the y-axis corresponding to the first row starting at column 4
    y_ticks = range(len(Y))
    ax.set_yticks(y_ticks[::y_ticks_skip])
    ax.set_yticklabels(df.columns[3::y_ticks_skip])

    # Save the plot in the same folder as the Excel sheet: "surface_plot_[excel_name].png"
    plot_path= 'C:/Users/Reactorkunde/Desktop/Plots/' + excel_name + 'surface_plot_' + '.png'
    plt.savefig(plot_path)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Open a file dialog to select the Excel file
    Tk().withdraw()  # Hide the main window
    file_path = askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx;*.xls")])

    if file_path:
        # Call the function to plot the surface
        plot_surface_from_excel(file_path, y_ticks_skip=10)  # Show every 10th value on the y-axis
    else:
        print("No file selected.")
