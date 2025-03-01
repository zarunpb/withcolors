import numpy as np
from .color_data import COLOR_LIST

def euclidean_distance(color1, color2):
    """Calculate the Euclidean distance between two RGB colors."""
    return np.linalg.norm(np.array(color1) - np.array(color2))

def get_color_name(rgb_color):
    """Find the top 3 closest gemstone colors based on RGB values."""
    color_distances = [
        (name, euclidean_distance(rgb_color, stored_rgb))
        for name, stored_rgb in COLOR_LIST.items()
    ]
    
    color_distances.sort(key=lambda x: x[1])  # Sort by closest match
    
    top_3 = color_distances[:3]  # Get top 3 matches
    total_distance = sum(1 / (d[1] + 1e-6) for d in top_3)  # Prevent division by zero
    percentages = {d[0]: round((1 / (d[1] + 1e-6) / total_distance) * 100, 2) for d in top_3}

    return [{'name': name, 'percentage': percentages[name]} for name, _ in top_3]
