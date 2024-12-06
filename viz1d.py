import os
from glob import glob
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
#from upaths import csv_pattern


# esawc_data = {
#     "Value": [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100],
#     "Color": ["#006400", "#ffbb22", "#ffff4c", "#f096ff", "#fa0000", "#b4b4b4", 
#               "#f0f0f0", "#0064c8", "#0096a0", "#00cf75", "#fae6a0"],
#     "Description": [
#         "Tree cover", "Shrubland", "Grassland", "Cropland", "Built-up", 
#         "Bare / sparse vegetation", "Snow and ice", "Permanent water bodies", 
#         "Herbaceous wetland", "Mangroves", "Moss and lichen"
#     ]
# }
# esawc_df = pd.DataFrame(esawc_data)
# esawc_df.to_csv('esawc.csv', index=False)


def lineplot_points(df,pnts_csv):

    title = os.path.basename(pnts_csv)
    columns_to_plot = [col for col in df.columns if col not in ['esawc', 'geometry']]

    # Plot each column
    df[columns_to_plot].plot(subplots=False, layout=(len(columns_to_plot), 1), 
                            figsize=(10, 5), title=title)
    plt.ylabel('Elevation (m)')
    plt.xlabel('Pixel distance from sampling origin')
    plt.tight_layout()
    plt.legend(loc='lower left')
    png = pnts_csv.replace('.csv', '__MLineProfile.png')
    plt.savefig(png, dpi=300)
    plt.show()


def plot_profile_with_esawc(df,pnts_csv,colname='cdem' ):
    esawc_data = {
    "Value": [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100],
    "Color": ["#006400", "#ffbb22", "#ffff4c", "#f096ff", "#fa0000", "#b4b4b4", 
              "#f0f0f0", "#0064c8", "#0096a0", "#00cf75", "#fae6a0"],
    "Description": [
        "Tree cover", "Shrubland", "Grassland", "Cropland", "Built-up", 
        "Bare / sparse vegetation", "Snow and ice", "Permanent water bodies", 
        "Herbaceous wetland", "Mangroves", "Moss and lichen"
    ]
    }
    esawc_df = pd.DataFrame(esawc_data)
    df = df.merge(esawc_df, left_on='esawc', right_on='Value', how='left')

    # Create a scatter plot using seaborn
    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        data=df, x=df.index, y=colname, 
        hue='Description', palette=dict(zip(esawc_df['Description'], esawc_df['Color'])), 
        s=80
    )

    # Add plot titles and labels
    plt.title(f"{colname}")
    plt.xlabel("Index")
    plt.ylabel("cdem")
    plt.legend(title='Land Cover Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    png = pnts_csv.replace('.csv', f'__SLineProfile_{colname}.png')
    plt.savefig(png, dpi=300)
    # need 3 of this stacked: lidar, cdem, dtm-lidar

