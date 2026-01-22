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

# Academic-grade color palette
COLORS = {
    'medical': '#76448A',          # Muted Purple (Human/Healthcare)
    'wastewater': '#16A085',       # Teal/Blue (Environmental Matrix)
    'non_medical': '#7D8E7D',      # Muted Gray-Green (Community Inputs)
    'neutral': '#566573',         # Gray for processes
    'neutral_light': '#F2F4F4',   # Light gray for backgrounds
    'text_dark': '#17202A',        # Near black for text
    'text_grey': '#566573',        # Gray for secondary text
    'border': '#2C3E50',           # Dark border
    'white': '#FFFFFF'
}

# Standard font settings for publication quality (Nature/PLOS style)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.labelweight'] = 'normal'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['text.color'] = COLORS['text_dark']

def create_gradient_background(ax):
    """Create a solid white background for the plot."""
    ax.set_facecolor(COLORS['white'])

def draw_scientific_symbol(ax, symbol_type, xy, size=0.4, color='black'):
    """Draw abstract scientific symbols instead of icons."""
    x, y = xy
    if symbol_type == 'metagenomics':
        # Abstract DNA helix
        t = np.linspace(0, 4*np.pi, 20)
        xs = np.sin(t) * 0.1 * size
        ys = np.linspace(-0.5, 0.5, 20) * size
        ax.plot(x + xs, y + ys, color=color, lw=1.5)
        ax.plot(x - xs, y + ys, color=color, lw=1.5)
        for i in range(0, 20, 2):
            ax.plot([x - xs[i], x + xs[i]], [y + ys[i], y + ys[i]], color=color, lw=1)
    elif symbol_type == 'wastewater':
        # Fluid flow symbol
        for i in range(3):
            t = np.linspace(0, 1, 10)
            xs = (t - 0.5) * size
            ys = np.sin(t * 10 + i) * 0.05 * size
            ax.plot(x + xs, y + ys + (i-1)*0.1*size, color=color, lw=1.5)
    elif symbol_type == 'comparison':
        # Scales/Balance
        ax.plot([x - 0.3*size, x + 0.3*size], [y, y], color=color, lw=1.5)
        ax.plot([x, x], [y, y - 0.4*size], color=color, lw=1.5)
        ax.add_patch(mpatches.Circle((x-0.3*size, y-0.1*size), 0.1*size, color=color))
        ax.add_patch(mpatches.Circle((x+0.3*size, y+0.1*size), 0.1*size, color=color))
    elif symbol_type == 'domain':
        # Simple circle for domain
        ax.add_patch(mpatches.Circle((x, y), 0.3*size, color=color, fill=False, lw=1.5))


def draw_glow_circle(ax, center, radius, color, alpha=0.3, layers=5):
    """Draw a glowing circle effect."""
    for i in range(layers, 0, -1):
        circle = Circle(center, radius * (1 + i * 0.15), 
                       color=color, alpha=alpha / i, zorder=1)
        ax.add_patch(circle)
    
    main_circle = Circle(center, radius, color=color, alpha=0.9, zorder=2)
    ax.add_patch(main_circle)
    return main_circle

def draw_one_health_framework(ax, font_scale=1.0):
    """Figure 1: One Health Context of Antimicrobial Resistance."""
    ax.set_xlim(0, 10)
    ax.set_ylim(0.2, 8.3)
    ax.set_aspect('equal')
    ax.axis('off')
    
    create_gradient_background(ax)
    
    # Title - Title Case
    ax.text(5, 7.9, 'One Health Context of Antimicrobial Resistance', fontsize=17*font_scale, fontweight='bold',
            color=COLORS['text_dark'], ha='center', va='center')
    
    # Subtitle - No quotes, lighter grey
    ax.text(5, 7.4, 'Wastewater integrates resistance signals across human, animal, and environmental systems', 
            fontsize=11*font_scale, color=COLORS['text_grey'], ha='center', style='italic', alpha=0.85)
    
    # Domain Centers - Perfect equilateral triangle, shifted up
    H_center = (2.5, 5.0)
    A_center = (7.5, 5.0)
    E_center = (5.0, 2.3)
    radius = 1.3
    
    centers = [H_center, A_center, E_center]
    labels = ['Human\nHealth', 'Animal\nHealth', 'Environmental\nHealth']
    
    for center, label in zip(centers, labels):
        ax.add_patch(Circle(center, radius, color=COLORS['neutral_light'], ec=COLORS['border'], lw=1.0, zorder=2))
        ax.text(center[0], center[1], label, fontsize=13*font_scale, fontweight='normal',
               color=COLORS['text_dark'], ha='center', va='center', zorder=3)
    
    # Central Wastewater - Reduced opacity
    W_center = (5.0, 4.1)
    W_radius = 1.5
    ax.add_patch(Circle(W_center, W_radius, color=COLORS['wastewater'], alpha=0.08, ec=COLORS['wastewater'], lw=1.5, linestyle='--', zorder=1))
    ax.text(W_center[0], W_center[1], 'Urban\nWastewater\nInterface', fontsize=12.5*font_scale, fontweight='bold',
            color=COLORS['wastewater'], ha='center', va='center', zorder=4)
    
    # Connectors - arrows don't touch circles
    arrow_props = dict(arrowstyle='<->', color=COLORS['neutral'], lw=1.0, mutation_scale=10)
    ax.annotate('', xy=(A_center[0]-radius-0.1, A_center[1]), xytext=(H_center[0]+radius+0.1, H_center[1]), arrowprops=arrow_props)
    
    h_to_e_v = np.array([2.5, -3.0]) / 3.905
    ax.annotate('', xy=(E_center[0]-h_to_e_v[0]*(radius+0.1), E_center[1]-h_to_e_v[1]*(radius+0.1)), 
               xytext=(H_center[0]+h_to_e_v[0]*(radius+0.1), H_center[1]+h_to_e_v[1]*(radius+0.1)), arrowprops=arrow_props)
    
    a_to_e_v = np.array([-2.5, -3.0]) / 3.905
    ax.annotate('', xy=(E_center[0]-a_to_e_v[0]*(radius+0.1), E_center[1]-a_to_e_v[1]*(radius+0.1)), 
               xytext=(A_center[0]+a_to_e_v[0]*(radius+0.1), A_center[1]+a_to_e_v[1]*(radius+0.1)), arrowprops=arrow_props)
    
    # Connector labels - Refined language
    ax.text(5, 5.2, 'Cross-sector interaction', fontsize=10*font_scale, color=COLORS['text_grey'], ha='center')
    ax.text(2.6, 3.3, 'Human-associated\ninputs', fontsize=10*font_scale, color=COLORS['text_grey'], ha='center')
    ax.text(7.4, 3.3, 'Environmental\ncirculation', fontsize=10*font_scale, color=COLORS['text_grey'], ha='center')
    
    # Bottom Caption - Reduced opacity
    ax.text(5, 0.8, 'AMR as an interconnected, system-level challenge', 
            fontsize=9.5*font_scale, color=COLORS['text_grey'], ha='center', style='italic', alpha=0.7)


def draw_wastewater_sources(ax, font_scale=1.0):
    """Figure 2: Urban Wastewater as a Population-Level AMR Matrix."""
    ax.set_xlim(0, 10)
    ax.set_ylim(2.3, 8.1)
    ax.axis('off')
    
    create_gradient_background(ax)
    
    # Title - Title Case
    ax.text(5, 7.7, 'Wastewater as a Population Matrix', 
            fontsize=17*font_scale, fontweight='bold', color=COLORS['text_dark'], ha='center')
    
    # Subtitle - No quotes
    ax.text(5, 7.3, 'Population-level integration of antimicrobial resistance signals',
            fontsize=11*font_scale, color=COLORS['text_grey'], ha='center', style='italic', alpha=0.85)
    
    # Input boxes
    box_w, box_h = 2.4, 1.2
    y_in = 6.1
    sources = [
        (1.5, y_in, 'Community\nHouseholds', COLORS['non_medical']),
        (5, y_in, 'Healthcare\nFacilities', COLORS['medical']),
        (8.5, y_in, 'Other Urban\nActivities', COLORS['non_medical'])
    ]
    
    for x, y, label, color in sources:
        rect = FancyBboxPatch((x-box_w/2, y-box_h/2), box_w, box_h, boxstyle="round,pad=0.1", 
                             facecolor=color, alpha=0.8, edgecolor=COLORS['border'], 
                             linewidth=0.8, zorder=2)
        ax.add_patch(rect)
        ax.text(x, y, label, fontsize=11*font_scale, fontweight='normal', 
               color='white' if color != COLORS['neutral_light'] else COLORS['text_dark'],
               ha='center', va='center', zorder=3)
    
    # Symmetrical Connectors - Equal length and angle
    arrow_props = dict(arrowstyle='->', color=COLORS['neutral'], lw=1.0, mutation_scale=10)
    for x in [1.5, 5, 8.5]:
        start_x, start_y = x, y_in - box_h/2 - 0.05
        target_x = 4.0 if x == 1.5 else (6.0 if x == 8.5 else 5.0)
        target_y = 4.85
        ax.annotate('', xy=(target_x, target_y), xytext=(start_x, start_y), arrowprops=arrow_props)
    
    # Wastewater focus - Reduced height, single line
    ax.add_patch(FancyBboxPatch((2, 3.4), 6, 1.4, boxstyle="round,pad=0.1",
                                    facecolor=COLORS['wastewater'], alpha=0.1,
                                    edgecolor=COLORS['wastewater'], lw=1.5, zorder=1))
    
    ax.text(5, 4.4, 'URBAN WASTEWATER SYSTEM', fontsize=14*font_scale, fontweight='bold',
           color=COLORS['wastewater'], ha='center', zorder=3)
    ax.text(5, 3.9, 'Aggregated Population-Level Resistance Signal', fontsize=11.5*font_scale,
           color=COLORS['text_grey'], ha='center', fontweight='normal', zorder=3)
    
    # Caption - Reduced opacity
    ax.text(5, 2.6, 'Reflects aggregated urban resistance pressure, not individual risk', 
            fontsize=9.5*font_scale, color=COLORS['text_grey'], ha='center', style='italic', alpha=0.7)


def draw_tier_2_context(ax, font_scale=1.0):
    """Figure 3: Tier-2 Indian Urban Context Visualization."""
    ax.set_xlim(0, 10)
    ax.set_ylim(1.5, 8.3)
    ax.axis('off')
    
    create_gradient_background(ax)
    
    # Title - Title Case
    ax.text(5, 7.9, 'Tier-2 Urban Wastewater Profile', 
            fontsize=17*font_scale, fontweight='bold', color=COLORS['text_dark'], ha='center')
    
    # Subtitle - Refined
    ax.text(5, 7.5, 'Key characteristics of under-studied Tier-2 urban settings',
            fontsize=11*font_scale, color=COLORS['text_grey'], ha='center', style='italic', alpha=0.85)
    
    # Descriptive Layers - Equal spacing, simplified text
    layers = [
        (6.0, 'Mixed Land Use Patterns', 'Close proximity of residential, commercial, and healthcare zones', COLORS['neutral_light']),
        (4.2, 'Partial Infrastructure', 'Non-unified sewage networks with direct healthcare waste entry', COLORS['non_medical']),
        (2.4, 'Waste Convergence', 'Aggregated clinical and municipal signals in single matrix', COLORS['medical'])
    ]
    
    for y, title, desc, color in layers:
        # Box for title
        ax.add_patch(FancyBboxPatch((0.8, y-0.7), 3.2, 1.1, boxstyle="round,pad=0.1",
                                    facecolor=color, alpha=0.8, ec=COLORS['border'], lw=1.0))
        ax.text(2.4, y-0.15, title, fontsize=10.5*font_scale, fontweight='bold', 
               color=COLORS['text_dark'] if color==COLORS['neutral_light'] else 'white', ha='center', va='center')
        
        # Annotation - Aligned left margin
        ax.text(4.3, y-0.15, desc, fontsize=10.5*font_scale, color=COLORS['text_dark'], ha='left', va='center')
        
        # Connection line
        ax.plot([4.0, 4.25], [y-0.15, y-0.15], color=COLORS['neutral'], lw=1.0)
    
    # Concluding line - Reduced opacity
    ax.text(5, 1.7, 'Epidemiological relevance of incomplete waste segregation', 
            fontsize=9.5*font_scale, color=COLORS['text_grey'], ha='center', style='italic', alpha=0.7)

def draw_comparison_framework(ax, font_scale=1.0):
    """Figure 4: Comparative Study Logic."""
    ax.set_xlim(0, 10)
    ax.set_ylim(1.9, 8.1)
    ax.axis('off')
    
    create_gradient_background(ax)
    
    # Title - Title Case
    ax.text(5, 7.7, 'Comparative Study Logic',
            fontsize=17*font_scale, fontweight='bold', color=COLORS['text_dark'], ha='center')
    
    # Subtitle - Refined
    ax.text(5, 7.3, 'Ecological comparison of resistance patterns across wastewater types',
            fontsize=11*font_scale, color=COLORS['text_grey'], ha='center', style='italic', alpha=0.85)
    
    # Center Separator - Exactly centered
    ax.text(5, 4.9, 'Comparative\nEcological\nAnalysis', fontsize=11*font_scale, fontweight='bold',
           color=COLORS['neutral'], ha='center', va='center', 
           bbox=dict(boxstyle='circle,pad=0.5', facecolor=COLORS['white'], edgecolor=COLORS['neutral'], lw=1.2))
    
    # Comparison Panels - 3 bullets each, increased spacing
    box_w, box_h = 4.0, 4.0
    panels = [
        (0.6, 2.7, 'Medical-influenced\nWastewater', COLORS['medical'], 
         ['Elevated antibiotic exposure', 'Point-source healthcare inputs', 'Differentiated ARG patterns']),
        (5.4, 2.7, 'Non-medical\nWastewater', COLORS['non_medical'], 
         ['Community baseline signal', 'Distributed urban inputs', 'Background ARG patterns'])
    ]
    
    for x, y, title, color, points in panels:
        ax.add_patch(FancyBboxPatch((x, y), box_w, box_h, boxstyle="round,pad=0.1",
                                     facecolor=color, alpha=0.08, ec=color, lw=1.5))
        ax.text(x+box_w/2, y+box_h-0.4, title, fontsize=13*font_scale, fontweight='bold', color=color, ha='center')
        
        # Increased spacing between bullets
        for i, pt in enumerate(points):
            ax.text(x+0.3, y+box_h-1.1 - i*0.85, f'• {pt}', fontsize=11*font_scale, color=COLORS['text_dark'], ha='left')
    
    # Footnote - Reduced opacity
    ax.text(5, 2.2, 'Focus: Resistance patterns, not individual source causality', 
            fontsize=9.5*font_scale, color=COLORS['text_grey'], ha='center', style='italic', alpha=0.7)


def draw_analysis_pipeline(ax, font_scale=1.0):
    """Figure 5: Analytical and Interpretation Framework Visualization."""
    ax.set_xlim(0, 10)
    ax.set_ylim(1.6, 8.3)
    ax.axis('off')
    
    create_gradient_background(ax)
    
    # Title - Title Case
    ax.text(5, 7.9, 'Analytical & Interpretation Framework',
            fontsize=17*font_scale, fontweight='bold', color=COLORS['text_dark'], ha='center')
    
    # Pipeline steps - No numbering emphasis, increased spacing
    steps = [
        ('Data Acquisition', 'Secondary analysis of\nmetagenomic FASTQ'),
        ('ARG Annotation', 'Bioinformatics profiling\n(CARD / ResFinder)'),
        ('Comparison', 'Abundance and\ndiversity metrics'),
        ('Interpretation', 'One Health ecological\ncharacterization')
    ]
    
    y_step = 6.1
    for i, (title, desc) in enumerate(steps):
        if i > 0:
            ax.annotate('', xy=(1.5 + i*2.3, y_step), xytext=(0.9 + i*2.3, y_step), 
                       arrowprops=dict(arrowstyle='->', color=COLORS['neutral'], lw=1.0))
        
        ax.add_patch(FancyBboxPatch((0.4 + i*2.3, y_step-0.8), 2.0, 1.6, boxstyle="round,pad=0.1",
                                    facecolor=COLORS['neutral_light'], ec=COLORS['border'], lw=0.8))
        ax.text(1.4 + i*2.3, y_step+0.25, title, fontsize=9.5*font_scale, fontweight='bold', ha='center')
        ax.text(1.4 + i*2.3, y_step-0.3, desc, fontsize=8.5*font_scale, color=COLORS['text_grey'], ha='center')
    
    # Interpretation Constraint Box - Reduced height, simplified
    ax.add_patch(FancyBboxPatch((1.8, 3.0), 6.4, 1.4, boxstyle="round,pad=0.15",
                                 facecolor=COLORS['medical'], alpha=0.03, ec=COLORS['medical'], lw=1.2, linestyle='--'))
    
    ax.text(5, 3.9, 'Interpretation Boundary', fontsize=11*font_scale, fontweight='bold', color=COLORS['medical'], ha='center')
    ax.text(5, 3.5, 'Analysis constrained to population-level ecological patterns', 
           fontsize=11.5*font_scale, color=COLORS['medical'], ha='center', fontweight='normal', style='italic')
    
    # Footnote - Reduced opacity
    ax.text(5, 2.2, 'Workflow optimized for characterization of secondary datasets', 
            fontsize=9.5*font_scale, color=COLORS['text_grey'], ha='center', style='italic', alpha=0.7)


def create_full_visualization():
    """Create the complete 4-panel publication-grade visualization."""
    fig = plt.figure(figsize=(16, 14))
    fig.patch.set_facecolor(COLORS['white'])
    
    # Main title
    fig.suptitle('AMR SURVEILLANCE IN URBAN WASTEWATER', 
                 fontsize=22, fontweight='bold', color=COLORS['text_dark'], y=0.98)
    fig.text(0.5, 0.95, 'Analytical Framework for Assessing Medical Waste Influence on Resistance Patterns',
             fontsize=13, color=COLORS['text_grey'], ha='center', fontweight='bold')
    
    # Create 2x2 grid
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    
    # Draw each panel
    draw_one_health_framework(ax1)
    draw_wastewater_sources(ax2)
    draw_comparison_framework(ax3)
    draw_analysis_pipeline(ax4)
    
    # Add panel labels
    panels = [(ax1, 'A'), (ax2, 'B'), (ax3, 'C'), (ax4, 'D')]
    for ax, label in panels:
        ax.text(-0.02, 0.98, label, transform=ax.transAxes, fontsize=16,
               fontweight='bold', color=COLORS['text_dark'], va='top',
               bbox=dict(boxstyle='circle,pad=0.3', facecolor=COLORS['neutral_light'], 
                        edgecolor=COLORS['border'], linewidth=1.5))
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.94])
    
    return fig

def create_arg_heatmap_concept():
    """Create a refined conceptual ARG heatmap visualization."""
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor(COLORS['white'])
    ax.set_facecolor(COLORS['white'])
    
    # Aggregated conceptual data
    arg_mechanisms = [
        'Beta-lactam resistance', 'Aminoglycoside resistance', 
        'Tetracycline resistance', 'Fluoroquinolone resistance', 
        'Macrolide-Lincosamide-Streptogramin', 'Sulfonamide resistance',
        'Multidrug efflux pumps', 'Glycopeptide resistance', 
        'Polymyxin resistance', 'Carbapenems (High-priority)'
    ]
    
    sample_groups = ['Medical-influenced\nWastewater (Aggregated)', 'Non-medical\nWastewater (Aggregated)']
    
    # Generate conceptual data (higher for medical)
    np.random.seed(42)
    medical_vals = np.array([0.9, 0.7, 0.6, 0.8, 0.5, 0.6, 0.9, 0.4, 0.3, 0.8])
    non_med_vals = np.array([0.4, 0.3, 0.5, 0.2, 0.3, 0.4, 0.6, 0.1, 0.1, 0.2])
    data = np.vstack([medical_vals, non_med_vals]).T
    
    # Create scientific colormap (Purples/Blues)
    cmap = LinearSegmentedColormap.from_list('scientific_amr', 
                                            [COLORS['neutral_light'], COLORS['non_medical'], COLORS['medical']])
    
    # Plot heatmap
    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    
    # Configure axes
    ax.set_xticks(range(2))
    ax.set_xticklabels(sample_groups, fontsize=12, fontweight='bold', color=COLORS['text_dark'])
    ax.set_yticks(range(10))
    ax.set_yticklabels(arg_mechanisms, fontsize=12, color=COLORS['text_dark'])
    
    # Remove ticks
    ax.tick_params(axis='both', which='both', length=0)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.7)
    cbar.set_label('Relative Abundance (Normalized)', color=COLORS['text_dark'], fontsize=12)
    cbar.outline.set_visible(False)
    
    # Annotation
    ax.text(0.5, -0.9, 'Illustrative representation of expected differential patterns', 
            fontsize=11, color=COLORS['text_grey'], ha='center', style='italic', transform=ax.transAxes)
    
    # Title
    ax.set_title('COMPARATIVE ARG PROFILING (CONCEPTUAL)', fontsize=16, 
                fontweight='bold', color=COLORS['text_dark'], pad=40)
    
    # Borders
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    return fig


def draw_study_design_flowchart(ax, font_scale=1.0):
    """Draw the refined study design flowchart."""
    ax.set_facecolor(COLORS['white'])
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10.5)
    ax.axis('off')
    
    # Title
    ax.text(7, 10.2, 'STUDY DESIGN OVERVIEW', fontsize=22*font_scale, fontweight='bold',
            color=COLORS['text_dark'], ha='center')
    
    # Study Design Steps
    steps = [
        (2.5, 8.5, 'RESEARCH QUESTION', 'Characterizing antibiotic resistance gene (ARG) patterns\nin relation to medical waste influence using aggregated signals'),
        (2.5, 6.8, 'DATA ACQUISITION', 'Secondary analysis of publicly available metagenomic datasets\nfrom diverse Indian urban wastewater contexts'),
        (2.5, 5.1, 'BIOINFORMATICS', 'Standardized QC, ARG identification (CARD/ResFinder),\nand taxonomic profiling using open-source workflows'),
        (2.5, 3.4, 'STATISTICAL ANALYSIS', 'Comparative abundance analysis, alpha/beta diversity metrics,\nand non-causal correlation testing'),
        (2.5, 1.7, 'INTERPRETATION', 'One Health contextualization constrained to\npopulation-level ecological patterns')
    ]
    
    for i, (x_start, y_start, label, desc) in enumerate(steps):
        # Step label box
        ax.add_patch(FancyBboxPatch((x_start-1.5, y_start-0.45), 3, 0.9, boxstyle="round,pad=0.1",
                                    facecolor=COLORS['neutral'], alpha=0.9,
                                    edgecolor=COLORS['border'], linewidth=1.1*font_scale))
        ax.text(x_start, y_start, label, fontsize=11*font_scale, fontweight='bold',
                color='white', ha='center', va='center')
        
        # Description box
        ax.add_patch(FancyBboxPatch((x_start+2, y_start-0.65), 8.5, 1.3, boxstyle="round,pad=0.1",
                                    facecolor=COLORS['white'], edgecolor=COLORS['neutral'], linewidth=1))
        ax.text(x_start+6.25, y_start, desc, fontsize=11.5*font_scale, color=COLORS['text_dark'], ha='center', va='center')
        
        # Connection arrow to next step
        if i < len(steps) - 1:
            ax.annotate('', xy=(x_start, y_start - 1.0), xytext=(x_start, y_start - 0.5),
                       arrowprops=dict(arrowstyle='->', color=COLORS['neutral'], lw=2.0))
    
    # Scope Limitation Banner
    ax.add_patch(FancyBboxPatch((3, 0.15), 8, 0.75, boxstyle="round,pad=0.1",
                                    facecolor=COLORS['neutral_light'], alpha=1.0,
                                    edgecolor=COLORS['border'], linewidth=1.5*font_scale))
    ax.text(7, 0.55, 'SCOPE LIMITATION', fontsize=11*font_scale, fontweight='bold',
           color=COLORS['text_dark'], ha='center')
    ax.text(7, 0.35, 'Population-level, descriptive analysis only. Interpretation constrained to ecological signals.',
           fontsize=10*font_scale, color=COLORS['text_grey'], ha='center')

def create_study_design_flowchart():
    """Create a study design flowchart."""
    fig, ax = plt.subplots(figsize=(12, 9))
    fig.patch.set_facecolor(COLORS['white'])
    draw_study_design_flowchart(ax, font_scale=1.1)
    plt.tight_layout()
    return fig


def create_individual_panels(output_dir):
    """Create Figure 1 to 5 as individual images."""
    
    panels = [
        ('figure_1_one_health.png', draw_one_health_framework),
        ('figure_2_matrix.png', draw_wastewater_sources),
        ('figure_3_tier2_context.png', draw_tier_2_context),
        ('figure_4_logic.png', draw_comparison_framework),
        ('figure_5_framework.png', draw_analysis_pipeline)
    ]
    
    for filename, draw_func in panels:
        fig, ax = plt.subplots(figsize=(12, 10))
        fig.patch.set_facecolor(COLORS['white'])
        
        draw_func(ax, font_scale=1.4)
        
        plt.tight_layout(pad=1.0)
        fig.savefig(os.path.join(output_dir, filename),
                   dpi=300, facecolor=COLORS['white'], edgecolor='none',
                   bbox_inches='tight', pad_inches=0.4)
        plt.close(fig)
        print(f"      ✓ Saved: {filename}")


if __name__ == '__main__':
    print("=" * 60)
    print("AMR WASTEWATER - ACADEMIC PROPOSAL FIGURE GENERATOR")
    print("=" * 60)
    print("\nStarting generation of cohesive figure set...")
    
    # Create output directory
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate the 5 core figures
    create_individual_panels(output_dir)
    
    print("\n" + "=" * 60)
    print("✅ COHESIVE SET OF 5 ACADEMIC FIGURES GENERATED SUCCESSFUL!")
    print("=" * 60)
    print(f"\nLocation: {output_dir}")
    print("\nGenerated Figure Set:")
    print("  1. figure_1_one_health.png   - One Health Context of AMR")
    print("  2. figure_2_matrix.png       - Wastewater as Population Matrix")
    print("  3. figure_3_tier2_context.png - Tier-2 Indian Urban Context")
    print("  4. figure_4_logic.png        - Comparative Study Logic")
    print("  5. figure_5_framework.png    - Analytical/Interpretation Framework")
