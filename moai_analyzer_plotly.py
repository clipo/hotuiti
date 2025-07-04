import numpy as np
import trimesh
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_and_analyze_moai(obj_file):
    """Load the moai mesh and analyze its center of mass"""
    
    # Load the mesh
    mesh = trimesh.load(obj_file)
    print(f"Loaded mesh with {len(mesh.vertices)} vertices and {len(mesh.faces)} faces")
    
    # Get mesh properties
    bounds = mesh.bounds
    print(f"\nMesh bounds:")
    print(f"  X: {bounds[0][0]:.3f} to {bounds[1][0]:.3f}")
    print(f"  Y: {bounds[0][1]:.3f} to {bounds[1][1]:.3f} (vertical axis)")
    print(f"  Z: {bounds[0][2]:.3f} to {bounds[1][2]:.3f}")
    
    # Calculate center of mass
    center_of_mass = mesh.center_mass
    
    print(f"\nCenter of mass: ({center_of_mass[0]:.3f}, {center_of_mass[1]:.3f}, {center_of_mass[2]:.3f})")
    
    # Calculate height from base
    base_y = bounds[0][1]
    height_from_base = center_of_mass[1] - base_y
    total_height = bounds[1][1] - bounds[0][1]
    height_percentage = (height_from_base / total_height) * 100
    
    print(f"\nHeight analysis:")
    print(f"  Base Y coordinate: {base_y:.3f}")
    print(f"  Center of mass height from base: {height_from_base:.3f}")
    print(f"  Total height: {total_height:.3f}")
    print(f"  Center of mass at {height_percentage:.1f}% of total height")
    
    # Find the base vertices
    base_threshold = base_y + 0.05
    base_vertices = mesh.vertices[mesh.vertices[:, 1] < base_threshold]
    
    if len(base_vertices) > 0:
        base_x_min = base_vertices[:, 0].min()
        base_x_max = base_vertices[:, 0].max()
        base_z_min = base_vertices[:, 2].min()
        base_z_max = base_vertices[:, 2].max()
        
        print(f"\nBase dimensions:")
        print(f"  X range: {base_x_min:.3f} to {base_x_max:.3f} (width: {base_x_max - base_x_min:.3f})")
        print(f"  Z range: {base_z_min:.3f} to {base_z_max:.3f} (depth: {base_z_max - base_z_min:.3f})")
        
        com_within_base_x = base_x_min <= center_of_mass[0] <= base_x_max
        com_within_base_z = base_z_min <= center_of_mass[2] <= base_z_max
        
        print(f"\nStability analysis:")
        print(f"  Center of mass X: {center_of_mass[0]:.3f} ({'within' if com_within_base_x else 'outside'} base X range)")
        print(f"  Center of mass Z: {center_of_mass[2]:.3f} ({'within' if com_within_base_z else 'outside'} base Z range)")
        
        base_center_x = (base_x_min + base_x_max) / 2
        base_center_z = (base_z_min + base_z_max) / 2
        
        offset_x = center_of_mass[0] - base_center_x
        offset_z = center_of_mass[2] - base_center_z
        
        print(f"\nCenter of mass offset from base center:")
        print(f"  X offset: {offset_x:.3f} ({'forward' if offset_x > 0 else 'backward'})")
        print(f"  Z offset: {offset_z:.3f} ({'right' if offset_z > 0 else 'left'})")
    
    return mesh, center_of_mass

def create_plotly_visualization(mesh, center_of_mass):
    """Create interactive 3D visualization using Plotly"""
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.55, 0.45],
        specs=[[{'type': 'mesh3d'}, {'type': 'scatter'}]],
        subplot_titles=('3D Moai with Center of Mass', 'Top View: Base vs Center of Mass'),
        horizontal_spacing=0.15  # Add more space between subplots
    )
    
    # Prepare mesh data
    vertices = mesh.vertices
    faces = mesh.faces
    
    # Get vertex coordinates
    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    
    # Get face indices (Plotly uses vertex indices for faces)
    i, j, k = faces[:, 0], faces[:, 1], faces[:, 2]
    
    # Calculate vertex colors based on height
    vertex_heights = y
    vertex_colors = (vertex_heights - vertex_heights.min()) / (vertex_heights.max() - vertex_heights.min())
    
    # Add mesh to 3D subplot with transparency
    fig.add_trace(
        go.Mesh3d(
            x=x, y=y, z=z,
            i=i, j=j, k=k,
            intensity=vertex_colors,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title="Height",
                x=0.55,
                thickness=15
            ),
            opacity=0.5,  # Make mesh semi-transparent
            flatshading=True,
            lighting=dict(
                ambient=0.6,  # Increase ambient light for better visibility
                diffuse=0.8,
                roughness=0.5,
                specular=0.2,
                fresnel=0.2
            ),
            lightposition=dict(
                x=100,
                y=200,
                z=100
            ),
            name='Moai Mesh',
            hoverinfo='none'  # Disable hover for cleaner interaction
        ),
        row=1, col=1
    )
    
    # Add center of mass point
    fig.add_trace(
        go.Scatter3d(
            x=[center_of_mass[0]],
            y=[center_of_mass[1]],
            z=[center_of_mass[2]],
            mode='markers',
            marker=dict(
                size=20,  # Larger size for better visibility
                color='red',
                line=dict(color='darkred', width=3),
                symbol='diamond'  # Different shape for distinction
            ),
            name='Center of Mass',
            showlegend=True,
            text=[f'COM: ({center_of_mass[0]:.3f}, {center_of_mass[1]:.3f}, {center_of_mass[2]:.3f})'],
            hoverinfo='text'
        ),
        row=1, col=1
    )
    
    # Add COM projection on base
    base_y = mesh.bounds[0][1]
    fig.add_trace(
        go.Scatter3d(
            x=[center_of_mass[0]],
            y=[base_y],
            z=[center_of_mass[2]],
            mode='markers',
            marker=dict(
                size=10,
                color='red',
                symbol='x',
                line=dict(color='darkred', width=2)
            ),
            name='COM Ground Projection',
            showlegend=True
        ),
        row=1, col=1
    )
    
    # Add vertical line from base to COM
    fig.add_trace(
        go.Scatter3d(
            x=[center_of_mass[0], center_of_mass[0]],
            y=[base_y, center_of_mass[1]],
            z=[center_of_mass[2], center_of_mass[2]],
            mode='lines+markers',
            line=dict(color='red', width=8, dash='dash'),
            marker=dict(size=5, color='red'),
            name='COM Height',
            showlegend=False,
            hoverinfo='none'
        ),
        row=1, col=1
    )
    
    # Add vertical reference line from base center
    base_center_x = (mesh.bounds[0][0] + mesh.bounds[1][0]) / 2
    base_center_z = (mesh.bounds[0][2] + mesh.bounds[1][2]) / 2
    
    fig.add_trace(
        go.Scatter3d(
            x=[base_center_x, base_center_x],
            y=[base_y, mesh.bounds[1][1]],
            z=[base_center_z, base_center_z],
            mode='lines',
            line=dict(color='black', width=4, dash='dot'),
            name='Vertical Reference',
            showlegend=True,
            hoverinfo='none'
        ),
        row=1, col=1
    )
    
    # Calculate lean angle
    # Note: front is at MIN Z, so negative z_offset means forward lean
    z_offset = center_of_mass[2] - base_center_z
    y_offset = center_of_mass[1] - base_y
    lean_angle = np.degrees(np.arctan2(abs(z_offset), y_offset))
    
    # Add text showing lean angle at top of 3D plot
    fig.add_annotation(
        x=0.25,
        y=0.98,
        xref="paper",
        yref="paper",
        text=f"<b>Forward lean: {lean_angle:.1f}°</b>",
        showarrow=False,
        bgcolor="wheat",
        bordercolor="black",
        borderwidth=1,
        font=dict(size=14, color="black"),
        xanchor="center",
        yanchor="top"
    )
    
    # Top view (2D scatter plot)
    base_threshold = base_y + 0.05
    base_vertices = mesh.vertices[mesh.vertices[:, 1] < base_threshold]
    
    # Get slice at 10cm above base for cleaner outline
    slice_height = base_y + 0.10
    slice_tolerance = 0.01
    slice_vertices = mesh.vertices[
        (mesh.vertices[:, 1] > slice_height - slice_tolerance) & 
        (mesh.vertices[:, 1] < slice_height + slice_tolerance)
    ]
    print(f"Found {len(slice_vertices)} vertices at slice height {slice_height:.3f}")
    
    if len(base_vertices) > 0:
        # Add base points (no legend)
        fig.add_trace(
            go.Scatter(
                x=base_vertices[:, 0],
                y=base_vertices[:, 2],
                mode='markers',
                marker=dict(size=1, color='lightgray', opacity=0.2),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Always show base bounds first
        base_x_min, base_x_max = base_vertices[:, 0].min(), base_vertices[:, 0].max()
        base_z_min, base_z_max = base_vertices[:, 2].min(), base_vertices[:, 2].max()
        
        # Create base outline from slice vertices
        if len(slice_vertices) > 10:
            print(f"Creating base outline from {len(slice_vertices)} slice vertices")
            # Use scipy to create a smoother outline
            from scipy.spatial import ConvexHull
            from scipy.interpolate import splprep, splev
            
            # Get 2D points from slice
            slice_points = slice_vertices[:, [0, 2]]
            
            try:
                # Create convex hull as starting point
                hull = ConvexHull(slice_points)
                hull_points = slice_points[hull.vertices]
                
                # Close the loop
                hull_points = np.vstack([hull_points, hull_points[0]])
                
                # Try to smooth the hull using splines
                try:
                    tck, u = splprep([hull_points[:, 0], hull_points[:, 1]], s=0.001, per=True)
                    u_new = np.linspace(0, 1, 100)
                    smooth_points = splev(u_new, tck)
                    
                    fig.add_trace(
                        go.Scatter(
                            x=smooth_points[0],
                            y=smooth_points[1],
                            mode='lines',
                            line=dict(color='blue', width=4),
                            fill='toself',
                            fillcolor='rgba(173, 216, 230, 0.4)',
                            name='Base Outline',
                            showlegend=True
                        ),
                        row=1, col=2
                    )
                    print("Successfully created smoothed base outline")
                except Exception as e:
                    print(f"Spline smoothing failed: {e}, using hull directly")
                    # Fallback to simple hull if smoothing fails
                    fig.add_trace(
                        go.Scatter(
                            x=hull_points[:, 0],
                            y=hull_points[:, 1],
                            mode='lines',
                            line=dict(color='blue', width=4),
                            fill='toself',
                            fillcolor='rgba(173, 216, 230, 0.4)',
                            name='Base Outline',
                            showlegend=True
                        ),
                        row=1, col=2
                    )
            except Exception as e:
                print(f"Convex hull failed: {e}")
                # If hull fails, just draw a rectangle
                from matplotlib.patches import Rectangle
                base_x_min, base_x_max = slice_points[:, 0].min(), slice_points[:, 0].max()
                base_z_min, base_z_max = slice_points[:, 1].min(), slice_points[:, 1].max()
                
                fig.add_trace(
                    go.Scatter(
                        x=[base_x_min, base_x_max, base_x_max, base_x_min, base_x_min],
                        y=[base_z_min, base_z_min, base_z_max, base_z_max, base_z_min],
                        mode='lines',
                        line=dict(color='blue', width=4),
                        fill='toself',
                        fillcolor='rgba(173, 216, 230, 0.4)',
                        name='Base Outline',
                        showlegend=True
                    ),
                    row=1, col=2
                )
        else:
            print(f"Not enough slice vertices ({len(slice_vertices)}), using base vertices")
            # Use all base vertices if not enough slice vertices
            base_x_min, base_x_max = base_vertices[:, 0].min(), base_vertices[:, 0].max()
            base_z_min, base_z_max = base_vertices[:, 2].min(), base_vertices[:, 2].max()
            
            fig.add_trace(
                go.Scatter(
                    x=[base_x_min, base_x_max, base_x_max, base_x_min, base_x_min],
                    y=[base_z_min, base_z_min, base_z_max, base_z_max, base_z_min],
                    mode='lines',
                    line=dict(color='blue', width=4, dash='dash'),
                    fill='toself',
                    fillcolor='rgba(173, 216, 230, 0.4)',
                    name='Base Bounds',
                    showlegend=True
                ),
                row=1, col=2
            )
        
        
        # Add base center
        base_center_x = (base_x_min + base_x_max) / 2
        base_center_z = (base_z_min + base_z_max) / 2
        
        fig.add_trace(
            go.Scatter(
                x=[base_center_x],
                y=[base_center_z],
                mode='markers',
                marker=dict(size=15, color='blue', symbol='cross'),
                name='Base Center'
            ),
            row=1, col=2
        )
    
    # Add center of mass to top view
    fig.add_trace(
        go.Scatter(
            x=[center_of_mass[0]],
            y=[center_of_mass[2]],
            mode='markers',
            marker=dict(size=20, color='red', line=dict(color='darkred', width=2)),
            name='Center of Mass'
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title_text="Moai Center of Mass Analysis",
        title_font_size=20,
        height=800,
        width=1400,  # Set explicit width
        showlegend=True,
        legend=dict(
            x=0.99,  # Place legend at far right
            y=0.5,   # Center vertically
            xanchor='right',
            yanchor='middle',
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='black',
            borderwidth=1,
            orientation='v'
        ),
        margin=dict(l=50, r=150, t=100, b=50)  # Add right margin for legend
    )
    
    # Update 3D scene
    fig.update_scenes(
        xaxis_title="X (width)",
        yaxis_title="Y (height)",
        zaxis_title="Z (depth)",
        aspectmode='data',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    )
    
    # Update 2D subplot - ensure we have the bounds defined
    if len(base_vertices) > 0:
        base_bounds_x = [base_vertices[:, 0].min() - 0.05, base_vertices[:, 0].max() + 0.05]
        base_bounds_z = [base_vertices[:, 2].min() - 0.05, base_vertices[:, 2].max() + 0.05]
        fig.update_xaxes(title_text="X (width)", row=1, col=2, range=base_bounds_x)
        fig.update_yaxes(title_text="Z (depth)", row=1, col=2, 
                         scaleanchor="x", scaleratio=1, range=base_bounds_z)
    else:
        fig.update_xaxes(title_text="X (width)", row=1, col=2)
        fig.update_yaxes(title_text="Z (depth)", row=1, col=2, scaleanchor="x", scaleratio=1)
    
    # Add annotations to 2D plot (Front is at min Z)
    fig.add_annotation(
        x=0.95, y=0.05,
        xref="paper", yref="paper",
        text="Front (Face)",
        showarrow=False,
        font=dict(size=12, style="italic"),
        xanchor="right", yanchor="bottom",
        row=1, col=2
    )
    fig.add_annotation(
        x=0.95, y=0.95,
        xref="paper", yref="paper",
        text="Back",
        showarrow=False,
        font=dict(size=12, style="italic"),
        xanchor="right", yanchor="top",
        row=1, col=2
    )
    
    # Add lean direction arrow in 2D view (from base center toward COM)
    if len(base_vertices) > 0:
        # Calculate normalized direction
        dx = center_of_mass[0] - base_center_x
        dz = center_of_mass[2] - base_center_z
        length = np.sqrt(dx**2 + dz**2)
        dx_norm = dx / length
        dz_norm = dz / length
        
        # Arrow scale
        arrow_scale = 0.1
        
        fig.add_annotation(
            x=base_center_x + dx_norm * arrow_scale,
            y=base_center_z + dz_norm * arrow_scale,
            ax=base_center_x,
            ay=base_center_z,
            xref="x2", yref="y2",
            axref="x2", ayref="y2",
            arrowhead=3,
            arrowsize=2,
            arrowwidth=3,
            arrowcolor="darkgreen",
            row=1, col=2
        )
        fig.add_annotation(
            x=base_center_x + dx_norm * 0.06,
            y=base_center_z + dz_norm * 0.06 + 0.02,
            text="Lean<br>direction",
            xref="x2", yref="y2",
            showarrow=False,
            font=dict(size=10, color="darkgreen"),
            align="center",
            row=1, col=2
        )
    
    # Save as HTML
    html_file = 'moai_analysis_interactive.html'
    fig.write_html(html_file)
    print(f"\n✓ Saved interactive HTML: {html_file}")
    
    # Save static images
    try:
        # High resolution PNG
        fig.write_image("moai_analysis_plotly_600dpi.png", width=1800, height=1000, scale=2)
        print("✓ Saved high-resolution PNG: moai_analysis_plotly_600dpi.png")
        
        # SVG
        fig.write_image("moai_analysis_plotly.svg", width=1800, height=1000)
        print("✓ Saved SVG: moai_analysis_plotly.svg")
    except Exception as e:
        print(f"Note: Could not save static images. Install kaleido for static export: pip install kaleido")
        print(f"Error: {e}")
    
    # Show the figure
    fig.show()

def main():
    obj_file = "SimplifiedMoai.obj"
    
    print("Plotly-based Moai Analysis")
    print("=" * 50)
    
    try:
        # Check if plotly is installed
        try:
            import plotly
        except ImportError:
            print("Installing plotly...")
            import subprocess
            subprocess.check_call(["pip", "install", "plotly"])
            print("Plotly installed successfully!")
        
        mesh, center_of_mass = load_and_analyze_moai(obj_file)
        
        print("\n" + "=" * 50)
        print("Creating interactive visualization...")
        create_plotly_visualization(mesh, center_of_mass)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()