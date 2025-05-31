import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class CubeDomain:
    def __init__(self):
        # Initialize 4x4x4 big cubes
        self.big_cubes = np.zeros((4, 4, 4), dtype=object)
        self.cube_colors = np.full((4, 4, 4), 'lightblue', dtype=object)
        
        # Initialize each big cube with 2x2x2 cells
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    self.big_cubes[i, j, k] = {
                        'values': np.random.rand(2, 2, 2),  # Random values for demonstration
                        'colors': np.full((2, 2, 2), None, dtype=object)  # None means no color set
                    }
    
    def set_cube_color(self, i, j, k, color):
        """Set color for a big cube at position (i, j, k)"""
        self.cube_colors[i, j, k] = color
    
    def set_cell_color(self, cube_i, cube_j, cube_k, cell_i, cell_j, cell_k, color):
        """Set color for a specific cell within a big cube"""
        self.big_cubes[cube_i, cube_j, cube_k]['colors'][cell_i, cell_j, cell_k] = color
    
    def create_cube_vertices(self, x, y, z, size):
        """Create vertices for a cube at position (x, y, z) with given size"""
        vertices = []
        for dx in [0, size]:
            for dy in [0, size]:
                for dz in [0, size]:
                    vertices.append([x + dx, y + dy, z + dz])
        return np.array(vertices)
    
    def plot_wireframe(self, show_cells=True, show_cubes=True, alpha=0.6):
        """Plot the 3D domain with wireframe"""
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot big cubes
        if show_cubes:
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        # Big cube position and size
                        x, y, z = i * 2, j * 2, k * 2
                        vertices = self.create_cube_vertices(x, y, z, 2)
                        
                        # Draw wireframe for big cube
                        edges = [
                            [0, 1], [1, 3], [3, 2], [2, 0],  # bottom face
                            [4, 5], [5, 7], [7, 6], [6, 4],  # top face
                            [0, 4], [1, 5], [2, 6], [3, 7]   # vertical edges
                        ]
                        
                        for edge in edges:
                            points = vertices[edge]
                            ax.plot3D(*points.T, color=self.cube_colors[i, j, k], linewidth=2)
        
        # Plot cells within each big cube
        if show_cells:
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        cube_data = self.big_cubes[i, j, k]
                        
                        for ci in range(2):
                            for cj in range(2):
                                for ck in range(2):
                                    cell_color = cube_data['colors'][ci, cj, ck]
                                    
                                    # Only draw cell if color is explicitly set
                                    if cell_color is not None:
                                        # Cell position within the big cube (scaled to fit in 4x4x4 space)
                                        x = i * 2 + ci
                                        y = j * 2 + cj
                                        z = k * 2 + ck
                                        
                                        vertices = self.create_cube_vertices(x, y, z, 1)
                                        
                                        # Draw wireframe for cell
                                        edges = [
                                            [0, 1], [1, 3], [3, 2], [2, 0],
                                            [4, 5], [5, 7], [7, 6], [6, 4],
                                            [0, 4], [1, 5], [2, 6], [3, 7]
                                        ]
                                        
                                        for edge in edges:
                                            points = vertices[edge]
                                            ax.plot3D(*points.T, color=cell_color, linewidth=1.5, alpha=alpha)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Domain: 8x8x8 Domain across 4 ranks')
        plt.show()
