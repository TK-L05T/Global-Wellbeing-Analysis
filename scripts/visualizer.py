import pandas as pd
import plotly.express as px
import os

# Ensures the output directory exists
os.makedirs('data/charts', exist_ok=True)

class GlobalWellbeingVisualizer:
    """
    A professional visualization suite for analyzing 
    the relationship between Health, Wealth, and Literacy.
    """
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.df.rename(columns={'Efficiency_Gap': 'Health_and_Wealth_Gap'}, inplace=True)
        print("-" * 60)
        print(f"Visualizer initialized with {len(self.df)} countries.")

    def create_world_map(self):
        print("Generating Map...")
        
        fig = px.choropleth(
            self.df,
            locations="Country",
            locationmode="country names",
            color="Health_and_Wealth_Gap",
            hover_name="Country",
            hover_data={
                'Health_and_Wealth_Gap': ':.2f',
                'Life_Expectancy': ':.1f years',
                'GDP_Per_Capita': ':$,.0f',
            },
            color_continuous_scale="RdYlGn", #red-yellow-green color scale
            color_continuous_midpoint=0,
            range_color=[-2.5, 2.5],
            title="Global Health and Wealth Gap (Statistical Deviation)"
        )

        # Handle countries with no data
        fig.update_geos(
            showcountries=True, countrycolor="Silver",
            showland=True, landcolor="lightgrey",
            showocean=True, oceancolor="#85b6e0"
        )
        
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
        
        output_path = 'data/charts/health_wealth_map.html'
        fig.write_html(output_path)
        fig.show()

    def create_scatter_plot(self):
        print("Generating Correlation Plot...")
        
        fig = px.scatter(
            self.df,
            x="GDP_Per_Capita",
            y="Life_Expectancy",
            color="Health_and_Wealth_Gap",
            hover_name="Country",
            size="Literacy_Rate", #Dot size represents literacy rate
            hover_data={
                'GDP_Per_Capita': ':$,.0f',
                'Life_Expectancy': ':.1f years',
                'Literacy_Rate': ':.1f%%',
                'Health_and_Wealth_Gap': ':.2f'
            },
            log_x=True,
            color_continuous_scale="RdYlGn", #red-yellow-green color scale
            color_continuous_midpoint=0,
            title="Life Expectancy vs. GDP (Size by Literacy, Color by Health and Wealth Gap)",
            labels={
                'GDP_Per_Capita': 'GDP Per Capita (Log Scale)', 
                'Life_Expectancy': 'Life Expectancy (Years)',
                'Health_to_Wealth_Gap': 'Health-Wealth Gap'
            }
        )

        fig.update_layout(font_family="Arial", title_font_size=20)

        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                
        output_path = 'data/charts/health_wealth_scatter.html'
        fig.write_html(output_path)
        fig.show()

if __name__ == "__main__":
    viz = GlobalWellbeingVisualizer('data/results/analyzed_data.csv')
    
    # Run visualizations
    viz.create_world_map()
    viz.create_scatter_plot()
    
    print("\nComplete: Interactive visualizations launched")
    print("-" * 60)
