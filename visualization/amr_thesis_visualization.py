"""
AMR Wastewater Thesis - Visual Synopsis
========================================
Interactive visualization demonstrating the research framework for:
"Medical Waste Influence on AMR Gene Patterns in Tier-2 Indian City Wastewater"

Author: AMR Wastewater Research Project
Date: January 2026
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import urllib.request
import os
from io import BytesIO
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# Set up custom color palette - Optimized for white background
COLORS = {
    'human': '#E74C3C',       # Warm red
    'animal': '#27AE60',       # Green
    'environment': '#3498DB',  # Blue
    'medical': '#9B59B6',      # Purple
    'municipal': '#F39C12',    # Orange
    'wastewater': '#1ABC9C',   # Teal
    'dark_bg': '#FFFFFF',      # White background
    'light_text': '#2C3E50',   # Dark text for white bg
    'accent': '#E056FD',       # Accent pink
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2',
    'arg': '#FF6B6B',          # ARG color
    'infrastructure': '#7F8C8D',
    'text_dark': '#000000',    # Black text for titles
    'text_secondary': '#666666', # Grey for subtitles
    'black': '#000000',        # Pure black
    'grey': '#666666'          # Grey for subheadings
}

# Icon URLs from free icon sources (using simple, reliable CDN icons)
ICON_URLS = {
    'human': 'https://cdn-icons-png.flaticon.com/128/1077/1077114.png',
    'animal': 'https://cdn-icons-png.flaticon.com/128/616/616408.png',
    'environment': 'https://cdn-icons-png.flaticon.com/128/3137/3137807.png',
    'household': 'https://cdn-icons-png.flaticon.com/128/553/553376.png',
    'hospital': 'https://cdn-icons-png.flaticon.com/128/4320/4320371.png',
    'industry': 'https://cdn-icons-png.flaticon.com/128/2942/2942169.png',
    'water': 'https://cdn-icons-png.flaticon.com/128/606/606795.png',
    'dna': 'https://cdn-icons-png.flaticon.com/128/2784/2784428.png',
    'database': 'https://cdn-icons-png.flaticon.com/128/2906/2906274.png',
    'filter': 'https://cdn-icons-png.flaticon.com/128/7693/7693332.png',
    'bacteria': 'https://cdn-icons-png.flaticon.com/128/3774/3774299.png',
    'chart': 'https://cdn-icons-png.flaticon.com/128/3281/3281307.png',
    'visualization': 'https://cdn-icons-png.flaticon.com/128/1055/1055666.png',
    'report': 'https://cdn-icons-png.flaticon.com/128/3135/3135692.png',
    'target': 'https://cdn-icons-png.flaticon.com/128/3207/3207594.png',
    'medical_waste': 'https://cdn-icons-png.flaticon.com/128/2913/2913477.png',
    'sewage': 'https://cdn-icons-png.flaticon.com/128/3076/3076129.png',
    'amr': 'https://cdn-icons-png.flaticon.com/128/3774/3774299.png',
    'warning': 'https://cdn-icons-png.flaticon.com/128/595/595067.png',
    'checkmark': 'https://cdn-icons-png.flaticon.com/128/5610/5610944.png',
}

# Cache for downloaded icons
icon_cache = {}

def download_icon(name, url, cache_dir):
    """Download an icon from URL and cache it locally."""
    cache_path = os.path.join(cache_dir, f"{name}.png")
    
    # Check if already in memory cache
    if name in icon_cache:
        return icon_cache[name]
    
    # Check if already downloaded
    if os.path.exists(cache_path):
        try:
            img = Image.open(cache_path).convert('RGBA')
            icon_cache[name] = img
            return img
        except:
            pass
    
    # Download from URL
    try:
        print(f"      Downloading icon: {name}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        img_data = response.read()
        img = Image.open(BytesIO(img_data)).convert('RGBA')
        
        # Save to cache
        img.save(cache_path, 'PNG')
        icon_cache[name] = img
        return img
    except Exception as e:
        print(f"      Warning: Could not download {name} icon: {e}")
        return None

def download_all_icons(cache_dir):
    """Download all required icons."""
    os.makedirs(cache_dir, exist_ok=True)
    print("   📥 Downloading icons...")
    
    for name, url in ICON_URLS.items():
        download_icon(name, url, cache_dir)
    
    print("   ✓ Icons ready")

def add_icon_to_plot(ax, icon_name, xy, zoom=0.3, cache_dir=None):
    """Add an icon to the plot at specified coordinates."""
    if cache_dir is None:
        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')
    
    if icon_name not in icon_cache:
        url = ICON_URLS.get(icon_name)
        if url:
            download_icon(icon_name, url, cache_dir)
    
    img = icon_cache.get(icon_name)
    if img is None:
        return None
    
    # Convert PIL image to numpy array
    img_array = np.array(img)
    
    # Create offset image
    imagebox = OffsetImage(img_array, zoom=zoom)
    imagebox.image.axes = ax
    
    # Create annotation box
    ab = AnnotationBbox(imagebox, xy, frameon=False, zorder=10)
    ax.add_artist(ab)
    
    return ab

def create_gradient_background(ax, color1='#FFFFFF', color2='#FFFFFF', color3='#FFFFFF'):
    """Create a solid white background for the plot."""
    ax.set_facecolor('#FFFFFF')

def draw_glow_circle(ax, center, radius, color, alpha=0.3, layers=5):
    """Draw a glowing circle effect."""
    for i in range(layers, 0, -1):
        circle = Circle(center, radius * (1 + i * 0.15), 
                       color=color, alpha=alpha / i, zorder=1)
        ax.add_patch(circle)
    
    main_circle = Circle(center, radius, color=color, alpha=0.9, zorder=2)
    ax.add_patch(main_circle)
    return main_circle

def draw_one_health_framework(ax, cache_dir):
    """Draw the One Health interconnected framework."""
    ax.set_xlim(-2, 12)
    ax.set_ylim(-1, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    
    create_gradient_background(ax)
    
    # Title
    title = ax.text(5, 8.3, 'ONE HEALTH FRAMEWORK', fontsize=16, fontweight='bold',
                   color='black', ha='center', va='center',
                   fontfamily='sans-serif')
    
    # Subtitle
    ax.text(5, 7.7, 'Antimicrobial Resistance as an Interconnected Challenge', 
            fontsize=9, color=COLORS['grey'], ha='center', fontweight='bold')
    
    # Three main circles - Human, Animal, Environment
    centers = [(2, 4.5), (8, 4.5), (5, 1.5)]
    labels = ['HUMAN\nHEALTH', 'ANIMAL\nHEALTH', 'ENVIRONMENTAL\nHEALTH']
    colors = [COLORS['human'], COLORS['animal'], COLORS['environment']]
    icons = ['human', 'animal', 'environment']
    
    for center, label, color, icon in zip(centers, labels, colors, icons):
        draw_glow_circle(ax, center, 1.2, color)
        add_icon_to_plot(ax, icon, (center[0], center[1] + 0.2), zoom=0.35, cache_dir=cache_dir)
        ax.text(center[0], center[1] - 0.7, label, fontsize=8, fontweight='bold',
               color='white', ha='center', va='center', linespacing=1.2)
    
    # Draw connecting arrows (bidirectional flows) - grey for visibility
    # Human <-> Animal
    ax.annotate('', xy=(6.6, 4.5), xytext=(3.4, 4.5),
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2, 
                             connectionstyle='arc3,rad=0.2'))
    ax.annotate('', xy=(3.4, 4.5), xytext=(6.6, 4.5),
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2,
                             connectionstyle='arc3,rad=0.2'))
    ax.text(5, 5.5, 'Zoonotic\nTransfer', fontsize=7, color=COLORS['grey'], 
            ha='center', va='center', linespacing=1.1, fontweight='bold')
    
    # Human <-> Environment
    ax.annotate('', xy=(3.8, 2.2), xytext=(2.5, 3.2),
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2,
                             connectionstyle='arc3,rad=0.2'))
    ax.annotate('', xy=(2.5, 3.2), xytext=(3.8, 2.2),
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2,
                             connectionstyle='arc3,rad=-0.2'))
    ax.text(1.8, 2.5, 'Waste\nDischarge', fontsize=7, color=COLORS['grey'], 
            ha='center', va='center', linespacing=1.1, fontweight='bold')
    
    # Animal <-> Environment
    ax.annotate('', xy=(6.2, 2.2), xytext=(7.5, 3.2),
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2,
                             connectionstyle='arc3,rad=-0.2'))
    ax.annotate('', xy=(7.5, 3.2), xytext=(6.2, 2.2),
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2,
                             connectionstyle='arc3,rad=0.2'))
    ax.text(8.2, 2.5, 'Agricultural\nRunoff', fontsize=7, color=COLORS['grey'], 
            ha='center', va='center', linespacing=1.1, fontweight='bold')
    
    # Central AMR text
    ax.text(5, 3.8, 'AMR', fontsize=14, fontweight='bold', color='white',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E74C3C', 
                     edgecolor='#C0392B', linewidth=2))

def draw_wastewater_sources(ax, cache_dir):
    """Draw the urban wastewater source diagram."""
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis('off')
    
    create_gradient_background(ax)
    
    # Title
    title = ax.text(5, 8.3, 'URBAN WASTEWATER: A Population-Level AMR Matrix', 
                   fontsize=14, fontweight='bold', color='black', ha='center')
    
    ax.text(5, 7.7, 'Tier-2 Indian Cities: Mixed Land Use & Incomplete Infrastructure',
            fontsize=9, color=COLORS['grey'], ha='center', fontweight='bold')
    
    # Source boxes at top
    sources = [
        (1.5, 5.5, 'household', 'Households', COLORS['municipal']),
        (5, 5.5, 'hospital', 'Healthcare\nFacilities', COLORS['medical']),
        (8.5, 5.5, 'industry', 'Industrial\nAreas', COLORS['infrastructure'])
    ]
    
    for x, y, icon, label, color in sources:
        # Glowing box
        for i in range(3, 0, -1):
            rect = FancyBboxPatch((x-0.9-i*0.1, y-0.7-i*0.1), 1.8+i*0.2, 1.4+i*0.2,
                                 boxstyle="round,pad=0.1", 
                                 facecolor=color, alpha=0.1, zorder=1)
            ax.add_patch(rect)
        
        rect = FancyBboxPatch((x-0.9, y-0.7), 1.8, 1.4,
                             boxstyle="round,pad=0.1", 
                             facecolor=color, alpha=0.9, edgecolor='#2C3E50', 
                             linewidth=2, zorder=2)
        ax.add_patch(rect)
        
        # Icon above, text below with proper spacing
        add_icon_to_plot(ax, icon, (x, y+0.25), zoom=0.25, cache_dir=cache_dir)
        ax.text(x, y-0.35, label, fontsize=7, fontweight='bold', color='white',
               ha='center', va='center', zorder=3, linespacing=1.0)
    
    # Arrows flowing down - grey for visibility
    for x in [1.5, 5, 8.5]:
        ax.annotate('', xy=(x, 3.8), xytext=(x, 4.6),
                   arrowprops=dict(arrowstyle='->', color='#555555', lw=2.5))
    
    # Central wastewater collection
    wastewater_box = FancyBboxPatch((1.5, 2.2), 7, 1.5,
                                    boxstyle="round,pad=0.15",
                                    facecolor='#1ABC9C', alpha=0.9,
                                    edgecolor='#16A085', linewidth=3, zorder=2)
    ax.add_patch(wastewater_box)
    
    # Icon on left, text on right to avoid overlap
    add_icon_to_plot(ax, 'water', (2.5, 3.0), zoom=0.3, cache_dir=cache_dir)
    ax.text(5.8, 3.0, 'URBAN WASTEWATER', fontsize=11, fontweight='bold',
           color='white', ha='center', zorder=3)
    
    # Arrow to metagenomic analysis - grey for visibility
    ax.annotate('', xy=(5, 0.9), xytext=(5, 2.0),
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2.5))
    
    # Metagenomic analysis box
    analysis_box = FancyBboxPatch((2, -0.2), 6, 1.2,
                                  boxstyle="round,pad=0.1",
                                  facecolor='#E056FD', alpha=0.9,
                                  edgecolor='#9B59B6', linewidth=2, zorder=2)
    ax.add_patch(analysis_box)
    
    # Icon on left side, text on right to avoid overlap
    add_icon_to_plot(ax, 'dna', (2.7, 0.4), zoom=0.22, cache_dir=cache_dir)
    ax.text(5.8, 0.55, 'METAGENOMIC ANALYSIS', fontsize=10, fontweight='bold',
           color='white', ha='center', zorder=3)
    ax.text(5.8, 0.1, 'ARG Profiling & Resistome Characterization', fontsize=7,
           color='white', ha='center', zorder=3, alpha=0.9)

def draw_comparison_framework(ax, cache_dir):
    """Draw the medical vs non-medical wastewater comparison."""
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis('off')
    
    create_gradient_background(ax)
    
    # Title
    title = ax.text(5, 8.3, 'COMPARATIVE ANALYSIS FRAMEWORK',
                   fontsize=14, fontweight='bold', color='black', ha='center')
    
    ax.text(5, 7.7, 'Medical-Influenced vs Non-Medical Wastewater',
            fontsize=10, color=COLORS['grey'], ha='center', fontweight='bold')
    
    # Left side - Medical
    medical_box = FancyBboxPatch((0.5, 3), 4, 4,
                                 boxstyle="round,pad=0.2",
                                 facecolor=COLORS['medical'], alpha=0.15,
                                 edgecolor=COLORS['medical'], linewidth=3)
    ax.add_patch(medical_box)
    
    # Icon at top of box, text below with proper spacing
    add_icon_to_plot(ax, 'medical_waste', (2.5, 6.6), zoom=0.35, cache_dir=cache_dir)
    ax.text(2.5, 5.85, 'MEDICAL', fontsize=11, fontweight='bold',
           color='black', ha='center')
    ax.text(2.5, 5.5, 'WASTEWATER', fontsize=11, fontweight='bold',
           color='black', ha='center')
    
    medical_items = [
        '• Hospital effluents',
        '• Antibiotic residues',
        '• Clinical waste streams',
        '• High ARG concentration'
    ]
    for i, item in enumerate(medical_items):
        ax.text(2.5, 4.9 - i*0.45, item, fontsize=8, color='black', 
               ha='center')
    
    # Right side - Non-Medical
    municipal_box = FancyBboxPatch((5.5, 3), 4, 4,
                                   boxstyle="round,pad=0.2",
                                   facecolor=COLORS['municipal'], alpha=0.15,
                                   edgecolor=COLORS['municipal'], linewidth=3)
    ax.add_patch(municipal_box)
    
    # Icon at top of box, text below with proper spacing
    add_icon_to_plot(ax, 'sewage', (7.5, 6.6), zoom=0.35, cache_dir=cache_dir)
    ax.text(7.5, 5.85, 'NON-MEDICAL', fontsize=11, fontweight='bold',
           color='black', ha='center')
    ax.text(7.5, 5.5, 'WASTEWATER', fontsize=11, fontweight='bold',
           color='black', ha='center')
    
    municipal_items = [
        '• Household sewage',
        '• Community waste',
        '• Agricultural runoff',
        '• Baseline ARG levels'
    ]
    for i, item in enumerate(municipal_items):
        ax.text(7.5, 4.9 - i*0.45, item, fontsize=8, color='black',
               ha='center')
    
    # VS symbol
    vs_circle = Circle((5, 5.2), 0.5, facecolor='#E74C3C', 
                       edgecolor='#C0392B', linewidth=2, zorder=10)
    ax.add_patch(vs_circle)
    ax.text(5, 5.2, 'VS', fontsize=10, fontweight='bold', color='white',
           ha='center', va='center', zorder=11)
    
    # Bottom analysis output
    output_box = FancyBboxPatch((1, 0.2), 8, 2.2,
                                boxstyle="round,pad=0.15",
                                facecolor='#ECF0F1', alpha=1.0,
                                edgecolor='#1ABC9C', linewidth=2)
    ax.add_patch(output_box)
    
    # Icon on left side, text on right to avoid overlap
    add_icon_to_plot(ax, 'chart', (1.7, 1.3), zoom=0.28, cache_dir=cache_dir)
    ax.text(5.5, 1.95, 'ANALYSIS OUTPUTS', fontsize=10, fontweight='bold',
           color='#1ABC9C', ha='center')
    
    outputs = [
        '• Differential ARG abundance profiles',
        '• Resistance gene diversity metrics',
        '• Ecological population-level patterns'
    ]
    for i, out in enumerate(outputs):
        ax.text(5.5, 1.4 - i*0.35, out, fontsize=8, color='black', ha='center')

def draw_analysis_pipeline(ax, cache_dir):
    """Draw the bioinformatics analysis pipeline."""
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis('off')
    
    create_gradient_background(ax)
    
    # Title
    title = ax.text(5, 8.3, 'BIOINFORMATICS ANALYSIS PIPELINE',
                   fontsize=14, fontweight='bold', color='black', ha='center')
    
    ax.text(5, 7.7, 'Reproducible Computational Framework for Wastewater AMR Analysis',
            fontsize=9, color=COLORS['grey'], ha='center', fontweight='bold')
    
    # Pipeline steps
    steps = [
        (1.5, 6, 'database', 'PUBLIC\nDATASETS', '#3498DB', 'Metagenomic\nsequences'),
        (5, 6, 'filter', 'QUALITY\nCONTROL', '#9B59B6', 'Filtering &\nPreprocessing'),
        (8.5, 6, 'bacteria', 'ARG\nPROFILING', '#E74C3C', 'Resistance gene\nidentification'),
        (1.5, 2.5, 'chart', 'STATISTICAL\nANALYSIS', '#27AE60', 'Comparative\nmetrics'),
        (5, 2.5, 'visualization', 'VISUALIZATION', '#F39C12', 'Interactive\nplots'),
        (8.5, 2.5, 'report', 'INTERPRETATION', '#1ABC9C', 'One Health\ncontext')
    ]
    
    for x, y, icon, label, color, desc in steps:
        # Glowing effect
        for i in range(3, 0, -1):
            circle = Circle((x, y), 1.1 + i*0.1, facecolor=color, alpha=0.1)
            ax.add_patch(circle)
        
        circle = Circle((x, y), 1.1, facecolor=color, alpha=0.9,
                        edgecolor='#2C3E50', linewidth=2)
        ax.add_patch(circle)
        
        # Icon centered, text below icon inside circle
        add_icon_to_plot(ax, icon, (x, y+0.35), zoom=0.25, cache_dir=cache_dir)
        ax.text(x, y-0.45, label, fontsize=7, fontweight='bold', color='white',
               ha='center', va='center', linespacing=0.9)
        
        # Only show description text for top row (y=6), not bottom row to avoid overlap
        if y > 4:
            ax.text(x, y-1.5, desc, fontsize=5, color=COLORS['grey'],
                   ha='center', va='center', linespacing=0.9, fontweight='bold')
    
    # Arrows between steps - using grey color for visibility on white bg
    arrow_props = dict(arrowstyle='->', color='#555555', lw=2, 
                      mutation_scale=15)
    
    # Top row - left to right (adjusted for larger circles)
    ax.annotate('', xy=(3.8, 6), xytext=(2.7, 6), arrowprops=arrow_props)
    ax.annotate('', xy=(7.3, 6), xytext=(6.2, 6), arrowprops=arrow_props)
    
    # Down arrow from ARG Profiling to Interpretation - on right side
    ax.annotate('', xy=(9.5, 3.7), xytext=(9.5, 4.9), 
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2,
                             connectionstyle='arc3,rad=0'))
    
    # Bottom row - right to left (adjusted for larger circles)
    ax.annotate('', xy=(6.2, 2.5), xytext=(7.3, 2.5), arrowprops=arrow_props)
    ax.annotate('', xy=(2.7, 2.5), xytext=(3.8, 2.5), arrowprops=arrow_props)
    
    # Arrows from bottom row to Framework box - positioned on sides to avoid overlap
    # Left arrow from Statistical Analysis
    ax.annotate('', xy=(2.2, 0.65), xytext=(1.5, 1.3),
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2))
    # Right arrow from Interpretation
    ax.annotate('', xy=(7.8, 0.65), xytext=(8.5, 1.3),
               arrowprops=dict(arrowstyle='->', color='#555555', lw=2))
    
    # Final Framework Output Box
    framework_box = FancyBboxPatch((1.8, -0.3), 6.4, 0.9,
                                   boxstyle="round,pad=0.1",
                                   facecolor='#667eea', alpha=0.95,
                                   edgecolor='#4834d4', linewidth=2)
    ax.add_patch(framework_box)
    
    ax.text(5, 0.15, 'REPRODUCIBLE AMR SURVEILLANCE FRAMEWORK', fontsize=8, fontweight='bold',
           color='white', ha='center')
    
    # Key features as a simple text line at bottom
    ax.text(5, -0.6, 'Reproducible • Open Data • Ecological Focus • One Health Context',
           fontsize=7, color=COLORS['grey'], ha='center', fontweight='bold')

def create_full_visualization(cache_dir):
    """Create the complete 4-panel visualization."""
    fig = plt.figure(figsize=(16, 14))
    fig.patch.set_facecolor('#FFFFFF')
    
    # Main title
    fig.suptitle('AMR Surveillance Using Wastewater Metagenomics', 
                 fontsize=22, fontweight='bold', color='black', y=0.98)
    fig.text(0.5, 0.95, 'Visual Synopsis: Medical Waste Influence on ARG Patterns in Tier-2 Indian Cities',
             fontsize=12, color=COLORS['grey'], ha='center', fontweight='bold')
    
    # Create 2x2 grid
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    
    # Draw each panel
    draw_one_health_framework(ax1, cache_dir)
    draw_wastewater_sources(ax2, cache_dir)
    draw_comparison_framework(ax3, cache_dir)
    draw_analysis_pipeline(ax4, cache_dir)
    
    # Add panel labels
    panels = [(ax1, 'A'), (ax2, 'B'), (ax3, 'C'), (ax4, 'D')]
    for ax, label in panels:
        ax.text(-0.02, 0.98, label, transform=ax.transAxes, fontsize=16,
               fontweight='bold', color='#667eea', va='top',
               bbox=dict(boxstyle='circle,pad=0.3', facecolor='#ECF0F1', 
                        edgecolor='#667eea', linewidth=2))
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.93])
    
    return fig

def create_arg_heatmap_concept():
    """Create a conceptual ARG heatmap visualization."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # Simulated ARG data
    np.random.seed(42)
    
    arg_classes = [
        'Beta-lactamase', 'Aminoglycoside', 'Tetracycline', 
        'Fluoroquinolone', 'Macrolide', 'Sulfonamide',
        'Multidrug efflux', 'Vancomycin', 'Colistin', 'Carbapenem'
    ]
    
    sample_types = ['Hospital\nSite 1', 'Hospital\nSite 2', 'Hospital\nSite 3',
                   'Municipal\nSite 1', 'Municipal\nSite 2', 'Municipal\nSite 3']
    
    # Generate data (higher values for hospital samples)
    medical_data = np.random.uniform(0.5, 1.0, (10, 3))
    municipal_data = np.random.uniform(0.0, 0.5, (10, 3))
    data = np.hstack([medical_data, municipal_data])
    
    # Create custom colormap
    colors = ['#1a1a2e', '#3a3a5e', '#667eea', '#E056FD', '#FF6B6B']
    cmap = LinearSegmentedColormap.from_list('amr', colors)
    
    # Plot heatmap
    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    
    # Configure axes
    ax.set_xticks(range(6))
    ax.set_xticklabels(sample_types, fontsize=10, color='black')
    ax.set_yticks(range(10))
    ax.set_yticklabels(arg_classes, fontsize=10, color='black')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Relative ARG Abundance', color='black', fontsize=11)
    cbar.ax.yaxis.set_tick_params(color='black')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='black')
    
    # Add dividing line between medical and municipal
    ax.axvline(x=2.5, color='#FFD93D', linewidth=3, linestyle='--')
    
    # Labels for regions - positioned at top of heatmap
    ax.text(1, -0.8, 'MEDICAL-INFLUENCED', fontsize=10, fontweight='bold',
           color=COLORS['medical'], ha='center')
    ax.text(4, -0.8, 'NON-MEDICAL', fontsize=10, fontweight='bold',
           color=COLORS['municipal'], ha='center')
    
    # Title - with more padding
    ax.set_title('Conceptual ARG Abundance Heatmap', fontsize=16, 
                fontweight='bold', color='black', pad=40)
    ax.text(2.5, 10.8, 'Expected differential pattern between wastewater types',
           fontsize=10, color=COLORS['grey'], ha='center', fontweight='bold')
    
    # Add grid
    ax.set_xticks(np.arange(-0.5, 6, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 10, 1), minor=True)
    ax.grid(which='minor', color='#BDC3C7', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    return fig

def create_study_design_flowchart(cache_dir):
    """Create a study design flowchart."""
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    title = ax.text(7, 9.5, 'STUDY DESIGN OVERVIEW', fontsize=18, fontweight='bold',
                   color='black', ha='center')
    
    # Research Question Box
    rq_box = FancyBboxPatch((2, 7.8), 10, 1.2, boxstyle="round,pad=0.15",
                            facecolor='#E74C3C', alpha=0.9,
                            edgecolor='#C0392B', linewidth=2)
    ax.add_patch(rq_box)
    add_icon_to_plot(ax, 'target', (2.8, 8.4), zoom=0.22, cache_dir=cache_dir)
    ax.text(7.2, 8.55, 'RESEARCH QUESTION', fontsize=11, fontweight='bold',
           color='white', ha='center')
    ax.text(7.2, 8.1, 'How does medical waste influence ARG patterns in Tier-2 Indian city wastewater?',
           fontsize=9, color='white', ha='center')
    
    # Arrow down
    ax.annotate('', xy=(7, 7.1), xytext=(7, 7.65),
               arrowprops=dict(arrowstyle='->', color='#FFD93D', lw=3))
    
    # Data Sources
    data_box = FancyBboxPatch((2, 5.8), 10, 1.4, boxstyle="round,pad=0.15",
                              facecolor='#3498DB', alpha=0.9,
                              edgecolor='#2980B9', linewidth=2)
    ax.add_patch(data_box)
    add_icon_to_plot(ax, 'database', (2.8, 6.5), zoom=0.22, cache_dir=cache_dir)
    ax.text(7.2, 6.95, 'DATA SOURCES', fontsize=11, fontweight='bold',
           color='white', ha='center')
    ax.text(7.2, 6.55, 'Publicly available metagenomic datasets from Indian wastewater studies',
           fontsize=9, color='white', ha='center')
    ax.text(7.2, 6.15, 'Medical-influenced sites  |  Non-medical municipal sites',
           fontsize=8, color='white', ha='center', alpha=0.9)
    
    # Arrow down
    ax.annotate('', xy=(7, 5.1), xytext=(7, 5.65),
               arrowprops=dict(arrowstyle='->', color='#FFD93D', lw=3))
    
    # Analysis Methods - Split into two boxes
    method1_box = FancyBboxPatch((1.5, 3.6), 5.5, 1.6, boxstyle="round,pad=0.15",
                                 facecolor='#9B59B6', alpha=0.9,
                                 edgecolor='#8E44AD', linewidth=2)
    ax.add_patch(method1_box)
    add_icon_to_plot(ax, 'dna', (2.2, 4.75), zoom=0.2, cache_dir=cache_dir)
    ax.text(4.5, 4.95, 'BIOINFORMATICS', fontsize=10, fontweight='bold',
           color='white', ha='center')
    ax.text(4.25, 4.55, '• Quality control & filtering', fontsize=8, color='white', ha='center')
    ax.text(4.25, 4.2, '• ARG identification (ResFinder/CARD)', fontsize=8, color='white', ha='center')
    ax.text(4.25, 3.85, '• Taxonomic profiling', fontsize=8, color='white', ha='center')
    
    method2_box = FancyBboxPatch((7, 3.6), 5.5, 1.6, boxstyle="round,pad=0.15",
                                 facecolor='#27AE60', alpha=0.9,
                                 edgecolor='#1E8449', linewidth=2)
    ax.add_patch(method2_box)
    add_icon_to_plot(ax, 'chart', (7.7, 4.75), zoom=0.2, cache_dir=cache_dir)
    ax.text(10, 4.95, 'STATISTICS', fontsize=10, fontweight='bold',
           color='white', ha='center')
    ax.text(9.75, 4.55, '• Comparative abundance analysis', fontsize=8, color='white', ha='center')
    ax.text(9.75, 4.2, '• Diversity metrics (alpha/beta)', fontsize=8, color='white', ha='center')
    ax.text(9.75, 3.85, '• Differential abundance testing', fontsize=8, color='white', ha='center')
    
    # Arrows down
    ax.annotate('', xy=(7, 2.9), xytext=(4.25, 3.45),
               arrowprops=dict(arrowstyle='->', color='#FFD93D', lw=2))
    ax.annotate('', xy=(7, 2.9), xytext=(9.75, 3.45),
               arrowprops=dict(arrowstyle='->', color='#FFD93D', lw=2))
    
    # Expected Outcomes
    outcome_box = FancyBboxPatch((2, 1.3), 10, 1.7, boxstyle="round,pad=0.15",
                                 facecolor='#1ABC9C', alpha=0.9,
                                 edgecolor='#16A085', linewidth=2)
    ax.add_patch(outcome_box)
    add_icon_to_plot(ax, 'checkmark', (2.8, 2.3), zoom=0.22, cache_dir=cache_dir)
    ax.text(7.2, 2.75, 'EXPECTED OUTCOMES', fontsize=11, fontweight='bold',
           color='white', ha='center')
    ax.text(7, 2.35, 'Characterization of ARG profiles in medical vs non-medical wastewater',
           fontsize=8, color='white', ha='center')
    ax.text(7, 1.95, 'Reproducible analytical framework for wastewater AMR surveillance',
           fontsize=8, color='white', ha='center')
    ax.text(7, 1.55, 'Insights into ecological patterns within One Health context',
           fontsize=8, color='white', ha='center')
    
    # Disclaimer box
    disclaimer_box = FancyBboxPatch((3, 0.2), 8, 0.8, boxstyle="round,pad=0.1",
                                    facecolor='#ECF0F1', alpha=1.0,
                                    edgecolor='#F39C12', linewidth=2)
    ax.add_patch(disclaimer_box)
    add_icon_to_plot(ax, 'warning', (3.6, 0.6), zoom=0.18, cache_dir=cache_dir)
    ax.text(7.2, 0.65, 'SCOPE LIMITATION', fontsize=9, fontweight='bold',
           color='#E67E22', ha='center')
    ax.text(7.2, 0.35, 'Ecological & population-level analysis only. No clinical, causal, or transmission inference.',
           fontsize=8, color='black', ha='center')
    
    plt.tight_layout()
    return fig


if __name__ == '__main__':
    print("=" * 60)
    print("AMR WASTEWATER THESIS - VISUAL SYNOPSIS GENERATOR")
    print("=" * 60)
    print("\nInitializing...")
    
    # Create output directory
    output_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(output_dir, 'icons')
    
    # Download icons first
    print("\n[0/3] Preparing icons...")
    download_all_icons(icons_dir)
    
    # Generate main visualization
    print("\n[1/3] Creating main 4-panel synopsis visualization...")
    fig1 = create_full_visualization(icons_dir)
    fig1.savefig(os.path.join(output_dir, 'amr_thesis_synopsis.png'), 
                 dpi=300, facecolor='#FFFFFF', edgecolor='none', 
                 bbox_inches='tight', pad_inches=0.3)
    print("      ✓ Saved: amr_thesis_synopsis.png")
    
    # Generate heatmap concept
    print("\n[2/3] Creating conceptual ARG heatmap...")
    fig2 = create_arg_heatmap_concept()
    fig2.savefig(os.path.join(output_dir, 'arg_heatmap_concept.png'),
                 dpi=300, facecolor='#FFFFFF', edgecolor='none',
                 bbox_inches='tight', pad_inches=0.3)
    print("      ✓ Saved: arg_heatmap_concept.png")
    
    # Generate study design flowchart
    print("\n[3/3] Creating study design flowchart...")
    fig3 = create_study_design_flowchart(icons_dir)
    fig3.savefig(os.path.join(output_dir, 'study_design_flowchart.png'),
                 dpi=300, facecolor='#FFFFFF', edgecolor='none',
                 bbox_inches='tight', pad_inches=0.3)
    print("      ✓ Saved: study_design_flowchart.png")
    
    print("\n" + "=" * 60)
    print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nOutput location: {output_dir}")
    print("\nGenerated files:")
    print("  📊 amr_thesis_synopsis.png     - Main 4-panel overview")
    print("  📈 arg_heatmap_concept.png     - Conceptual ARG comparison")
    print("  📋 study_design_flowchart.png  - Study methodology flow")
    print(f"\n  📁 icons/                      - Cached icon files ({len(icon_cache)} icons)")
    print("\n💡 Tip: Run with 'python amr_thesis_visualization.py' to regenerate")
    
    # Note: plt.show() removed - using non-interactive backend for automated generation
    print("\n🖼️  To view interactively, open the PNG files or run in Jupyter notebook")
