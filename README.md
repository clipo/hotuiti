# Hotuiti - Moai Center of Mass Analysis

A scientific analysis project that calculates and visualizes the center of mass of a Rapa Nui moai (Easter Island statue) to determine its stability and balance characteristics. This analysis provides insights into how these massive statues could have been transported and erected.

## 🎯 Project Overview

This project performs physics-based analysis on a 3D model of a moai statue to determine:
- **3D Center of Mass Location**: Precise calculation of the COM position
- **Stability Analysis**: Whether the statue would stand upright or tip over
- **Lean Measurements**: Forward/backward and left/right tilt angles
- **Base Contact Analysis**: How the COM relates to the base footprint
- **Scientific Visualizations**: Publication-quality figures showing the analysis

## 📊 Key Findings

Our analysis reveals that the moai design is inherently stable:

| Metric | Value | Significance |
|--------|-------|--------------|
| **COM Height** | 40.6% of total height (2.98m from base on 7.35m statue) | Low COM ensures stability |
| **Stability** | ✅ Stable | COM falls within base footprint |
| **Front Edge Distance** | 28.4cm | Safe margin from tipping forward |
| **Backward Lean** | 6.9cm (0.5°) | Slight backward tilt |
| **Lateral Offset** | 4.7cm left | Minor asymmetry |
| **Base Dimensions** | 2.64m × 2.10m | D-shaped footprint |

## 📁 Repository Structure

```
hotuiti/
├── SimplifiedMoai.obj              # 3D model (5,150 vertices, 10,296 faces)
├── README.md                       # This file
├── CLAUDE.md                       # AI assistant guidance
├── requirements.txt                # Python dependencies
├── figure_caption.txt              # Scientific figure caption
│
├── Analysis Scripts/
│   ├── moai_analyzer.py            # Original analysis implementation
│   ├── moai_analyzer_corrected.py  # Improved with proper coordinate system
│   ├── moai_analyzer_enhanced.py   # Enhanced with surface rendering
│   ├── moai_analyzer_final.py      # Final version with all features
│   ├── moai_analyzer_headless.py   # Server-friendly (no display required)
│   ├── moai_analyzer_plotly.py     # Interactive 3D visualization
│   ├── moai_analyzer_plotly_simple.py # Simplified Plotly version
│   ├── calculate_lean_angle.py     # Lean angle calculations
│   └── test_base_outline.py        # Base outline verification
│
└── Output Files/
    ├── moai_analysis_corrected_600dpi.png    # High-res raster image
    ├── moai_analysis_final_600dpi.png        # Final analysis visualization
    ├── moai_analysis_enhanced_600dpi.png     # Enhanced rendering
    ├── moai_analysis_corrected.svg           # Vector graphics
    ├── moai_analysis_final.svg               # Final vector output
    ├── moai_analysis_enhanced.svg            # Enhanced vector
    └── moai_analysis_3d_interactive.html     # Interactive 3D view
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/clipo/hotuiti.git
cd hotuiti
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Dependencies
- **trimesh** ≥ 4.0.0 - 3D mesh processing
- **numpy** ≥ 1.20.0 - Numerical computations
- **matplotlib** ≥ 3.5.0 - 2D/3D plotting
- **scipy** ≥ 1.7.0 - Scientific computing
- **plotly** (optional) - Interactive visualizations

## 💻 Usage

### Basic Analysis
Run the standard analysis with 2D visualizations:
```bash
python moai_analyzer_final.py
```

This will:
1. Load the 3D mesh model
2. Calculate center of mass using triangle centroids
3. Analyze stability metrics
4. Generate high-quality visualizations (PNG & SVG)
5. Print detailed measurements to console

### Interactive 3D Visualization
Create an interactive HTML visualization:
```bash
python moai_analyzer_plotly.py
```
Open `moai_analysis_3d_interactive.html` in your browser to explore the 3D model.

### Headless Mode (No Display)
For server environments or automated pipelines:
```bash
python moai_analyzer_headless.py
```

### Calculate Lean Angles
For detailed tilt analysis:
```bash
python calculate_lean_angle.py
```

## 📈 Understanding the Output

### Console Output Example
```
=== Moai Mesh Analysis ===
Mesh bounds:
  X: -1.32m to 1.32m (width: 2.64m)
  Y: 0.00m to 1.50m (height: 1.50m)
  Z: -1.38m to 0.73m (depth: 2.10m)

Center of Mass: (-0.047, 0.609, -0.069) meters
Height from base: 0.609m (40.6% of total height)

=== Stability Analysis ===
Base dimensions: 2.64m x 2.10m
Center of mass is 0.284m from the front edge
✓ STABLE: Center of mass is within the base footprint
```

### Generated Visualizations

#### 📊 2D Analysis (PNG/SVG files)
**Left Panel - 3D View:**
- Moai mesh with height-based coloring (blue=low, red=high)
- Red sphere marking center of mass
- Dashed line showing COM projection to base
- Coordinate axes for orientation

**Right Panel - Top View:**
- D-shaped base outline (actual footprint)
- Red dot: COM ground projection
- Blue cross: Geometric center of base
- Green line: Front edge reference
- Cardinal directions labeled

#### 🌐 3D Interactive (HTML file)
- Fully rotatable 3D model
- Zoom and pan controls
- Toggle visibility of COM markers
- Export views as images

## 🔬 Technical Details

### Coordinate System
```
Y (Height)
│
│   Z (Depth)
│  /
│ /
└────── X (Width)
```
- **Origin**: Center of base at ground level
- **X-axis**: Left-right (facing moai)
- **Y-axis**: Vertical (base to head)
- **Z-axis**: Back-front depth

### Physics Calculations

#### Center of Mass
The COM is calculated using the weighted average of all triangle centroids:
```python
COM = Σ(centroid_i × area_i) / Σ(area_i)
```

#### Stability Criterion
A moai is stable if its center of mass ground projection falls within the convex hull of the base contact points. We use a D-shaped approximation of the actual base outline.

#### Lean Angle
Calculated as the angle between the vertical axis and the line from base center to COM:
```python
lean_angle = arctan(horizontal_offset / height)
```

### Model Specifications
- **Format**: Wavefront OBJ (text-based)
- **Vertices**: 5,150
- **Faces**: 10,296 triangles
- **Scale**: 1 unit = 4.9 meters (real moai height: 7.35m)
- **Processing**: Simplified mesh via MeshLab

## 🔧 Troubleshooting

### Common Issues

1. **ImportError: No module named 'trimesh'**
   - Solution: Ensure you've run `pip install -r requirements.txt`

2. **Matplotlib backend issues**
   - Solution: Use `moai_analyzer_headless.py` or set backend:
   ```python
   import matplotlib
   matplotlib.use('Agg')
   ```

3. **Memory errors with large meshes**
   - Solution: Use the simplified mesh provided or decimate in MeshLab

4. **Plotly visualizations not showing**
   - Solution: Ensure plotly is installed: `pip install plotly`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/hotuiti.git

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python -m pytest tests/  # If tests are added

# Submit a pull request
```

## 📚 References

- [Easter Island Statue Project](http://www.eisp.org/) - Archaeological data
- [Trimesh Documentation](https://trimesh.org/) - 3D mesh processing
- [The Walking Moai](https://www.nationalgeographic.com/adventure/article/how-easter-island-statues-walked) - Transport theories

## 📝 Citation

If you use this analysis in your research, please cite:
```bibtex
@software{hotuiti2024,
  title = {Hotuiti: Moai Center of Mass Analysis},
  author = {Lipo, Carl},
  year = {2024},
  url = {https://github.com/clipo/hotuiti}
}
```

## 📄 License

This project is open source and available under the MIT License. The 3D model was processed using MeshLab.

## 👤 Author

Created by Carl Lipo for analyzing the engineering and transport of Rapa Nui moai statues.

---

*For questions or collaborations, please open an issue on GitHub.*