# Hotuiti - Moai Center of Mass Analysis

This project analyzes the center of mass of a 3D model of a Rapa Nui moai (Easter Island statue) to determine its stability and balance characteristics.

## Overview

The project uses a simplified 3D mesh model (`SimplifiedMoai.obj`) to calculate and visualize:
- The center of mass location in 3D space
- Height of center of mass from the base
- Whether the center of mass falls within the base footprint
- Distance from the front edge to determine tipping risk

## Key Findings

- **Center of Mass Height**: 40.6% of total height (0.609m from base)
- **Stability**: Center of mass is within the base footprint - the moai is stable
- **Position**: COM is 28.4cm behind the front edge of the base
- **Offset**: Slight backward lean (6.9cm) and left offset (4.7cm) from base center

## Files

### 3D Model
- `SimplifiedMoai.obj` - Wavefront OBJ format 3D mesh (5,150 vertices, 10,296 faces)

### Analysis Scripts
- `moai_analyzer.py` - Original analysis script with basic visualization
- `moai_analyzer_corrected.py` - Corrected version with proper orientation and base outline
- `moai_analyzer_headless.py` - Non-interactive version for generating images
- `moai_analyzer_enhanced.py` - Enhanced visualization with surface rendering
- `moai_analyzer_plotly.py` - Interactive 3D visualization using Plotly

### Output Files
- `moai_analysis_corrected_600dpi.png` - High-resolution visualization (600 DPI)
- `moai_analysis_corrected.svg` - Scalable vector graphics version
- `moai_analysis_interactive.html` - Interactive 3D visualization (if using Plotly version)

## Installation

```bash
# Clone the repository
git clone https://github.com/clipo/hotuiti.git
cd hotuiti

# Install required packages
pip install -r requirements.txt
```

### Requirements
- Python 3.7+
- trimesh >= 4.0.0
- numpy >= 1.20.0
- matplotlib >= 3.5.0
- scipy >= 1.7.0
- plotly (optional, for interactive visualization)

## Usage

### Basic Analysis
```bash
python moai_analyzer_corrected.py
```

This will:
1. Load the 3D mesh
2. Calculate the center of mass
3. Analyze stability metrics
4. Generate visualization images (PNG and SVG)

### Interactive Visualization
```bash
python moai_analyzer_plotly.py
```

Creates an interactive HTML file that can be opened in a web browser.

## Understanding the Output

### Console Output
The script provides detailed measurements including:
- Mesh dimensions and bounds
- Center of mass coordinates
- Height analysis (percentage from base)
- Base dimensions
- Stability analysis (whether COM is within base)
- Distance from front edge

### Visualizations

#### 3D View (Left Panel)
- Shows the moai mesh colored by height
- Red sphere indicates center of mass
- Red X marks the ground projection of COM
- Dashed line shows vertical drop from COM to base

#### Top-Down View (Right Panel)
- Shows the actual D-shaped base outline
- Red dot indicates center of mass position
- Blue cross marks base geometric center
- Green line indicates front edge
- Directional labels (Front, Back, Left, Right)

## Technical Details

### Coordinate System
- **X-axis**: Width (left-right when facing moai)
- **Y-axis**: Height (vertical, base to head)
- **Z-axis**: Depth (back to front)

### Center of Mass Calculation
The center of mass is calculated assuming uniform density throughout the mesh, using the weighted average of triangle centroids weighted by their areas.

### Stability Analysis
A moai is considered stable if its center of mass projects within the base footprint when viewed from above. The analysis also measures the distance from the COM to the front edge to assess tipping risk.

## License

This project is open source. The 3D model was created using MeshLab.

## Author

Created for analyzing the stability of Rapa Nui moai statues.