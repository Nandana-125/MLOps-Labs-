# Lab 5 - Apache Beam CSV Processing Pipeline

## Overview

This lab explores Apache Beam for processing structured CSV data. Instead of the standard word count example from the original Apache Beam lab, I built a pipeline that reads an IMDb movies dataset and runs multiple aggregations on it — things like average ratings by genre, movie counts, budget trends, and revenue breakdowns.


## Dataset

- **IMDb Movies Dataset** from [Kaggle](https://www.kaggle.com/datasets/danielgrijalvas/movies)
- ~7,600 movies with columns like name, genre, year, score, budget, gross, rating, director, etc.

## What the Pipeline Does

The pipeline reads `movies.csv`, parses each row into a dictionary, filters out bad records, and then branches into 4 separate aggregations:

1. **Average IMDb Score per Genre** — uses a custom `CombineFn` to calculate mean scores
2. **Movie Count per Genre** — counts how many movies fall under each genre
3. **Average Budget per Year** — shows how movie budgets have changed over the decades
4. **Total Gross Revenue per Genre** — sums up box office earnings by genre

Each result gets written to a separate text file in the `outputs/` folder.

## Changes from the Original Lab

- Used a **CSV dataset** instead of a plain text file (King Lear)
- Built **4 different aggregations** instead of just word count
- Wrote a **custom `CombineFn` class** (`AverageFn`) for computing averages
- Added **data validation** and error handling for missing/bad values in the CSV
- Created **visualizations** (bar charts) using matplotlib in the notebook
- Included a standalone Python script (`imdb_beam_pipeline.py`) alongside the notebook

## Project Structure

```
Lab5/
├── README.md
├── imdb_beam_pipeline.py        # Standalone pipeline script
├── IMDb_Beam_Pipeline.ipynb     # Notebook with step-by-step walkthrough
├── data/
│   └── movies.csv               # IMDb dataset
├── outputs/
│   ├── avg_score_per_genre-00000-of-00001.txt
│   ├── movie_count_per_genre-00000-of-00001.txt
│   ├── avg_budget_per_year-00000-of-00001.txt
│   ├── total_gross_per_genre-00000-of-00001.txt
│   └── visualizations.png
└── beam_env/                    # Virtual environment (not pushed)
```

## How to Run

### Setup

```bash
git clone https://github.com/Nandana-125/MLOps-Labs-.git
cd MLOps-Labs-/Lab5
python3 -m venv beam_env
source beam_env/bin/activate
pip install apache-beam pandas matplotlib jupyter
```

### Run the standalone script

```bash
python imdb_beam_pipeline.py
```

Output files will appear in the `outputs/` folder.

### Run the notebook

```bash
jupyter notebook IMDb_Beam_Pipeline.ipynb
```

Run all cells — the notebook walks through the pipeline step by step and generates charts at the end.

### Note

If you're using Python 3.13 with a newer version of pandas, Beam's Jupyter integration might throw an error about missing DataFrame methods. To fix this, patch the `is_in_ipython()` function in `apache_beam/utils/interactive_utils.py` to return `False`. The standalone script (`imdb_beam_pipeline.py`) runs fine without any patches.

## Sample Output

**Average Score per Genre:**

```
AvgScore | Drama: 6.69
AvgScore | Comedy: 6.19
AvgScore | Action: 6.2
AvgScore | Animation: 6.77
AvgScore | Biography: 7.03
```

**Movie Count per Genre:**

```
MovieCount | Comedy: 2245
MovieCount | Action: 1705
MovieCount | Drama: 1518
MovieCount | Crime: 551
MovieCount | Biography: 443
```

## Tools Used

- Apache Beam (DirectRunner)
- Python 3.13
- pandas (for data preview in notebook)
- matplotlib (for charts)
