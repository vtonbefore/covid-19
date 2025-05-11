import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 

# 1. Data Collection & Loading
df = pd.read_csv("owid-covid-data.csv")

# 2. Data Cleaning
df = df[df['continent'].notna()]  # Remove aggregate entries like "World"
df['date'] = pd.to_datetime(df['date'])

# Get latest data per country
latest = df.sort_values("date").groupby("location").tail(1)

# 3. Visualizing Vacancy (Cases/Deaths) Progress for Selected Country
def line_chart(country):
    country_df = df[df['location'] == country]
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='date', y='total_cases', data=country_df, label="Total Cases")
    sns.lineplot(x='date', y='total_deaths', data=country_df, label="Total Deaths")
    plt.title(f"COVID-19 Trend in {country}")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

# 4. Choropleth Map – Total Cases by Country
def choropleth_map():
    fig = px.choropleth(
        latest,
        locations="iso_code",
        color="total_cases",
        hover_name="location",
        color_continuous_scale="Reds",
        title="Total COVID-19 Cases by Country"
    )
    fig.show()

# 5. Insights Reporting
def report_insights():
    top_cases = latest.nlargest(5, 'total_cases')[['location', 'total_cases']]
    top_deaths = latest.nlargest(5, 'total_deaths')[['location', 'total_deaths']]

    print("📊 Top 5 Countries by Total Cases:")
    print(top_cases.to_string(index=False))
    print("\n💀 Top 5 Countries by Total Deaths:")
    print(top_deaths.to_string(index=False))

# --- Run Everything ---
if __name__ == "__main__":
    print("COVID-19 Data Analysis")
    report_insights()
    country = input("Enter a country to view trend (e.g., India, Kenya, USA): ")
    line_chart(country)
    print("Generating world map of total cases...")
    choropleth_map()
