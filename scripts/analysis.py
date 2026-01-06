import pandas as pd
import os

os.makedirs('data/results', exist_ok=True)

def run_analysis():
    print("-" * 40) 
    print("Starting Statistical Outlier Analysis...")

    df = pd.read_csv('data/processed/master_data.csv')

    # Standardize the data using Z-Scores
    cols = ['GDP_Per_Capita', 'Life_Expectancy', 'Literacy_Rate']
    for col in cols:
        df[f'{col}_ZScore'] = (df[col] - df[col].mean()) / df[col].std()

    # Calculate the Statistical Deviation using Z-Score
    # Positive = Higher health than wealth predicts 
    # Negative = Lower health than wealth predicts
    df['Efficiency_Gap'] = df['Life_Expectancy_ZScore'] - df['GDP_Per_Capita_ZScore']

    # Identifing top 10 Neg/Pos outliers 
    positive_outliers = df.sort_values(by='Efficiency_Gap', ascending=False).head(10)
    negative_outliers = df.sort_values(by='Efficiency_Gap', ascending=True).head(10)

    # Save results to 'results' folder
    df.to_csv('data/results/analyzed_data.csv', index=False)
    positive_outliers.to_csv('data/results/positive_outliers.csv', index=False)
    negative_outliers.to_csv('data/results/negative_outliers.csv', index=False)
    
    print("==Analysis Complete==")
    print("-" * 30)
    print(f"\n📈 Positive Outliers (Higher Health compared to Wealth):")
    print(positive_outliers[['Country', 'Life_Expectancy', 'GDP_Per_Capita']].head(5))
    print(f"\n📉 Negative Outliers (Higher Wealth compared to Health):")
    print(negative_outliers[['Country', 'Life_Expectancy', 'GDP_Per_Capita']].head(5))

if __name__ == "__main__":
    run_analysis()
