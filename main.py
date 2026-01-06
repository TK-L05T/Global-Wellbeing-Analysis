import os
import sys

# Importing the modules from the scripts folder
try:
    from scripts.scraper import scrape_all_data
    from scripts.data_manager import clean_data
    from scripts.analysis import run_analysis
    from scripts.visualizer import GlobalWellbeingVisualizer
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def run_project():
    print("="*50)
    print("\nSTARTING GLOBAL WELLBEING DATA PIPELINE\n")
    print("="*50)

    # SCRAPE
    scrape_all_data()

    # CLEAN & MERGE
    clean_data()

    # ANALYZE & CALCULATE
    run_analysis()

    # STEP 4: VISUALIZE
    print("\n🎨 Phase 4: Generating Interactive Visuals...")
    # Point the visualizer to the analyzed result file
    viz = GlobalWellbeingVisualizer('data/results/analyzed_data.csv')
    viz.create_world_map()
    viz.create_scatter_plot()

    print("\n" + "="*50)
    print("✅ PROJECT COMPLETE!")
    print("All charts are open in your browser and saved in data/charts/")
    print("="*50)

if __name__ == "__main__":
    run_project()