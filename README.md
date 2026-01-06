# 🌍 Global Wellbeing  Analysis

By utilizing web scraping, statistical anomaly detection, and modern interactive visualizations, we identify which countries are over-performing or under-performing (Health-wise) relative to their GDP

## Project Overview
- **Scraper Module** - Data Collection.
- **Data Manager Module** - Data cleaning and merging of cleaned data.
- **Analyzer Module** - Find anomalous data (through Z-score).
- **Visualizer Module** - Interactive Scatter plot & Choropleth map.

- - - -

## 📊 Project Structure, Code Complexity and Bonus Point Criteria

| Rubric Category      | Requirement              | Implementation Script      | Key Features                                       |
| :------------------- | :----------------------- | :------------------------- | :------------------------------------------------- |
| **Data Acquisition** | Scraped Messy Data (+10) | `scripts/scraper.py`       | Bypasses 403 blocks; multi-source scraping.        |
| **Data Cleaning**    | [Step-by-Step Description](https://github.com/TK-L05T/Global-Wellbeing-Analysis/edit/main/README.md#step-by-step-data-cleaning-scriptscleanpy) | `scripts/cleaner.py` | Regex-based entity resolution; outlier removal.    |
| **Analysis**         | Data Science (+15)       | `scripts/analysis.py`      | Z-score normalization; Anomaly detection.          |
| **Visualization**    | Modern Web Viz (+15)     | `scripts/visualizer.py`    | Plotly interactive HTML with dark-outline markers. |

- - - -

## Data Acquisition

Our dataset was not downloaded; rather, it was scraped from multiple Wikipedia sources using `Requests` and `Pandas`. 
Wikipedia tables are notoriously inconsistent, so we performed the following

- - - -

## Step-by-Step Data Cleaning (`scripts/cleaner.py`)

Wikipedia tables are notoriously inconsistent, so we performed the following "Data Surgery":

**Regex Footnote Scrubbing:** Wikipedia uses citations like `Country[a]`. Our code uses `re.sub(r'\[.*?\]', '', text)` to ensure names are standardized for merging.

**Entity Resolution:** We encountered non-breaking spaces (`\xa0`) and hidden HTML characters. We implemented a "Nuclear Match Key" that strips all non-alphanumeric characters and converts to lowercase to force matches between different tables (e.g., `U.S.A`. → `usa`).

**Numeric Sanitization:** Values like `$65,000*` were cleaned using regex to remove currency symbols and punctuation, then cast to floats for mathematical analysis.

- - - -

## Statistical Methodology (scripts/analyze.py)

We moved beyond basic averages to perform **Anomaly Detection** using a Health to Wealth Gap metric.

1. **Standardization:** We transformed all raw metrics into Z-scores to allow for direct comparison between USD and Years of Life:

$$z = \frac{x - \mu}{\sigma}$$
 
2. **The Gap Calculation:** We defined the Health and Wealth Gap as the difference between a country's Health Z-score and its Wealth Z-score.

3. **Anomaly Labeling:**

    * **Positive Outliers:** Countries with a gap >1.0 (Health outcomes significantly exceed economic predictions).

    * **Negative Outliers:** Countries with a gap <−1.0 (Health outcomes lag significantly behind economic capacity).

*Later used in [visualization](link) to report the data*

- - - -

## Interactive Visualizations (scripts/visualize.py)

Our visualization uses **Plotly**, providing a modern web-based front-end that far exceeds static Matplotlib/Seaborn charts.

* **The Global Map:** An interactive choropleth map. Missing data is rendered in neutral grey, while active data points use a RdYlGn (Red-Yellow-Green) divergence scale to highlight outliers.

* **The Scatter Plot:**

    * **X-Axis:** GDP (Logarithmic Scale)

    * **Y-Axis:** Life Expectancy

    * **Color:** Health to Wealth Gap (Standard Score (Z-Score))

    * **Dot Size:** Literacy Rate

    * **Design:** Dark marker outlines for high contrast and readability.

- - - -

## How To Run

1. Install Dependencies:
```bash
pip install -r requirements.txt
```
2. Run the Master Pipeline:
```bash
python main.py
```
