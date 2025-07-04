# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains 3D model assets, specifically a simplified Moai (Easter Island statue) model in Wavefront OBJ format.

## Key Files

- `SimplifiedMoai.obj` - 3D model file containing:
  - 5,150 vertices
  - 10,296 faces
  - Vertex normals for lighting
  - Generated using Meshlab software
  - References a missing material file: `SimplifiedMoai.obj.mtl`

## Working with OBJ Files

OBJ is a text-based 3D model format. The file structure includes:
- `v` lines: vertex positions (x, y, z coordinates)
- `vn` lines: vertex normals for lighting calculations
- `f` lines: face definitions linking vertices

## Common Tasks

### Viewing the Model
- Use 3D viewers like Blender, MeshLab, or online OBJ viewers
- The model can be loaded without the material file, but will appear with default shading

### Processing the Model
- Python libraries: `trimesh`, `pywavefront`, `numpy-stl`
- JavaScript: `three.js` for web-based rendering
- C++: `assimp` library for loading and processing

### Analyzing Model Properties
To analyze the model programmatically:
```python
# Example using trimesh
import trimesh
mesh = trimesh.load('SimplifiedMoai.obj')
print(f"Vertices: {len(mesh.vertices)}")
print(f"Faces: {len(mesh.faces)}")
print(f"Bounding box: {mesh.bounds}")
```

## Notes
- The missing `.mtl` file means material/texture information is not available
- Line endings are CRLF (Windows-style)
- This is a simplified/decimated model, likely optimized for performance