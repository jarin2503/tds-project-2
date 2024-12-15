from cred import *
import pandas as pd
import seaborn
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import requests
import matplotlib.pyplot as plt
import os
import sys
import numpy as np

def generate_story(data, images):
    r"""Generates a narrative from the data and plots."""
    proxy_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}",
    }
    plot_descriptions = "\n".join(
        [f"Plot {i+1}: {img}" for i, img in enumerate(images)]
    )
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You have to analyze the data and narrate a comprehensive story from the data and plots.",
            },
            {
                "role": "user",
                "content": f"Dataset summary:\n{data}\n\nPlots:\n{plot_descriptions}",
            },
        ],
        "temperature": 0,
        "max_tokens": 1500,
    }
    response = requests.post(url=proxy_url, headers=headers, json=payload)
    if response.ok:
        ai_response = response.json()
        return ai_response["choices"][0]["message"]["content"].strip()
    return f"Error fetching story. Status code: {response.status_code}"

def touch_readmefile(story):
    r"""Writes the generated story to a README.md file."""
    readme_path = f"{name}/README.md"
    with open(readme_path, "w") as f:
        f.write("# Analysis Report\n\n")
        f.write(story)
    print(f"README.md file created at {readme_path}")

def scatter_pair_plts(data):
    r"""Creates scatter plots for all pairs of numeric columns in the dataset."""
    numeric_data = data.select_dtypes(include=["number"])
    if numeric_data.empty:
        raise ValueError("No numeric columns found in the dataset.")

    seaborn.pairplot(numeric_data, diag_kind="kde", plot_kws={"alpha": 0.6})
    plt.suptitle(f"Scatter Plots for Numeric Columns in {name} dataset", y=1.02)
    plt.savefig(f"{name}/scatter_plot.png")
    plt.close()
    return f"{name}/scatter_plot.png"

def make_direc():
    r"""Creates a directory for storing results."""
    processed_name = give_names(sys.argv[1])
    try:
        os.makedirs(processed_name)
    except FileExistsError:
        pass

def missing_plot_matplotlib(data):
    r"""Creates a bar chart for missing data by columns."""
    missing_cols = []
    missing_values = []
    for col in data.columns:
        if data[col].isna().sum() > 0:
            missing_cols.append(col)
            missing_values.append(data[col].isna().sum())
    if missing_cols:
        plt.figure(figsize=(10, 6))
        plt.bar(missing_cols, missing_values, color="blue", alpha=0.7, edgecolor="black")
        plt.title(f"Missing Data by Column in {give_names(sys.argv[1]).capitalize()} Dataset")
        plt.xlabel("Columns")
        plt.ylabel("Number of Missing Values")
        plt.xticks(rotation=45, ha="right")
        plt.savefig(f"{name}/missing_plot_matplotlib.png")
        plt.close()
        return f"{name}/missing_plot_matplotlib.png"

def create_correlation(data):
    r"""
    Generates a heatmap of correlations between numerical features in the dataset.

    Parameters:
    data (DataFrame): The dataset as a pandas DataFrame.
    save_path (str): Path to save the heatmap image.
    """
    numeric_data = data.select_dtypes(include=['number'])
    
    if numeric_data.empty:
        print("No numerical data available for correlation heatmap.")
        return

    correlation_matrix = numeric_data.corr()

    plt.figure(figsize=(10, 8))
    seaborn.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(f"{name}/correlation_heatmap.png")
    return f"{name}/correlation_heatmap.png"

def give_description(data):
    r"""Gives a short description of the data."""
    return str(data.describe(include="all"))

def plt_imp_cols(data):
    r"""Plots cumulative explained variance using PCA."""
    numeric_data = data.select_dtypes(include=["number"])

    if numeric_data.empty:
        raise ValueError("No numeric columns found in the dataset.")

    imputer = SimpleImputer(strategy="mean")
    numeric_data_imputed = imputer.fit_transform(numeric_data)

    n_components = min(numeric_data.shape[1], numeric_data.shape[0])
    pca = PCA(n_components=n_components)
    pca.fit(numeric_data_imputed)

    cum_variance = pca.explained_variance_ratio_.cumsum()

    plt.figure(figsize=(8, 6))
    plt.plot(range(1, n_components + 1), cum_variance, marker="o", linestyle="--")
    plt.title(f"Cumulative Explained Variance by PCA Components in {name.capitalize()} Dataset")
    plt.xlabel("Number of Principal Components")
    plt.ylabel("Cumulative Explained Variance")
    plt.grid(True)
    plt.axhline(y=0.9, color="r", linestyle="--", label="90% Variance Threshold")
    plt.legend(loc="lower right")
    plt.savefig(f"{name}/number_of_important_columns.png")
    plt.close()
    return f"{name}/number_of_important_columns.png"

def load_dataset():
    r"""Loads the data by pd.read_csv. Run uv autolysis.py and dataset.csv"""
    try:
        data = pd.read_csv(sys.argv[1])
        return data
    except UnicodeDecodeError:
        data = pd.read_csv(sys.argv[1], encoding='ISO-8859-1')
        return data
    except:
        raise Exception("Dataset File is missing. Use uv run autolysis.py <CSV FILE PATH>")

def give_names(string: str):
    r"""
    Returns the filtered filename without . and \.
    """
    if "\\" in string:
        string = string.split("\\")[-1]
    if "." in string:
        string = string.split(".")[0]
    return string


data = load_dataset()
name = give_names(sys.argv[1])

make_direc()

data_summary = give_description(data)
plot_files = [
    missing_plot_matplotlib(data),
    plt_imp_cols(data),
    scatter_pair_plts(data),
    create_correlation(data)
]

story = generate_story(data_summary, plot_files)
touch_readmefile(story)

