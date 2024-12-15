# Autolysis.py

Autolysis.py is a Python-based data analysis tool that processes CSV datasets, generates various insights and visualizations, and writes a comprehensive analysis to a `README.md` file. The script includes features for handling missing data, PCA analysis, scatter plots, correlation heatmaps, and automated story generation using OpenAI's API.

## Features

- **Data Description**: Generates a summary of the dataset, including statistics for all columns.
- **Missing Data Visualization**: Creates a bar chart to display missing values by column.
- **Scatter Plot Matrix**: Produces scatter plots for all pairs of numeric columns in the dataset.
- **PCA Analysis**: Plots the cumulative explained variance to identify the most important principal components.
- **Correlation Heatmap**: Visualizes correlations between numeric features.
- **Automated Story Generation**: Creates a narrative analysis using OpenAI's GPT API based on dataset summaries and plots.
- **README.md Generation**: Writes the generated analysis and insights to a `README.md` file.

## Prerequisites

Ensure the following Python packages are installed:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `requests`

You also need an OpenAI proxy token. Set it in your environment variables:

```bash
export AIPROXY_TOKEN=your_token_here
```

## Usage

Run the script with a CSV file as an argument:

```bash
python autolysis.py <path_to_csv>
```

### Example

```bash
python autolysis.py dataset.csv
```

## Output

- **Visualizations**: The script generates and saves the following plots in a directory named after the dataset:
  - Missing data bar chart
  - PCA cumulative explained variance plot
  - Scatter plot matrix
  - Correlation heatmap

- **README.md**: A file summarizing the analysis is generated in the dataset's directory.

## Code Overview

### Key Functions

- **`load_dataset`**: Loads the dataset using `pandas.read_csv`.
- **`give_names`**: Extracts a clean name for the dataset file.
- **`make_direc`**: Creates a directory to store results.
- **`give_description`**: Provides a statistical summary of the dataset.
- **`missing_plot_matplotlib`**: Visualizes missing data.
- **`plt_imp_cols`**: Performs PCA and plots cumulative explained variance.
- **`scatter_pair_plts`**: Generates scatter plot matrices.
- **`create_correlation`**: Produces a heatmap of feature correlations.
- **`generate_story`**: Creates a narrative analysis using OpenAI's GPT API.
- **`touch_readmefile`**: Writes the analysis to a `README.md` file.

### Example Directory Structure

After running the script, the directory will look like this:

```
<dataset_name>/
├── README.md
├── missing_plot_matplotlib.png
├── number_of_important_columns.png
├── scatter_plot.png
├── correlation_heatmap.png
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
