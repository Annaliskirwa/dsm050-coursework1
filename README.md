# DSM050 Data Visualisation — Midterm Coursework

**MSc Data Science, University of London**
**Module:** DSM050 Data Visualisation
**Weight:** 30% of final module mark

## Topic
Global determinants of life expectancy: a visual investigation of the WHO Life
Expectancy dataset (2000–2015), aimed at informing policymakers.

## Repository structure
```
Coursework1/
├── data/
│   ├── raw/              # original, untouched dataset
│   └── processed/        # cleaned dataset used for analysis
├── notebooks/
│   └── DSM050_CW1.ipynb  # preprocessing, EDA, visualisations, dashboard
├── figures/
│   ├── univariate/
│   ├── multivariate/
│   └── dashboard/
├── report/
│   ├── DSM050_CW1.md     # source of the written report
│   ├── DSM050_CW1.pdf    # submitted PDF (built from .md)
│   └── build_pdf.py      # Markdown → HTML → PDF (headless Chromium)
├── requirements.txt
└── README.md
```

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name dsm050 --display-name "Python (dsm050)"
python -m playwright install chromium   # one-time browser download for PDF export
jupyter notebook notebooks/DSM050_CW1.ipynb
```

## Build the report PDF
```bash
python report/build_pdf.py
# → writes report/DSM050_CW1.pdf
```

## Dataset
WHO Life Expectancy Data (Kaggle, Kumar Rajarshi).
Place `Life Expectancy Data.csv` in `data/raw/`.
Source: https://www.kaggle.com/datasets/kumarajarshi/life-expectancy-who

## AI-tool declaration
See the *AI Use Declaration* appendix in `report/report.md`.
