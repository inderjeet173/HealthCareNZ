# NZ Health Dashboard

An interactive data visualization dashboard for New Zealand health statistics, built with Python, Dash, and Plotly.

## Overview

This project showcases disease patterns across New Zealand regions, analyzing health data from multiple years (2024-2025). The dashboard provides interactive filtering and visual analytics including:

- **Real-time KPIs**: Total cases, top diseases, regional hotspots, and demographic insights
- **Interactive Filters**: Filter by year, region, and disease type
- **Multi-dimensional Visualizations**:
  - Cases by disease (bar chart)
  - Cases by region (bar chart with counts)
  - Cases by age group (bar chart)
  - Gender distribution (donut chart)

## Tech Stack

- **Frontend**: Dash, Plotly
- **Data Processing**: Pandas, NumPy
- **Backend**: Flask (via Dash)
- **Language**: Python 3.11+

## Prerequisites

- Python 3.11 or newer
- Virtual environment (recommended)

## Setup (Windows)

1. Activate the project's virtual environment:

```powershell
venv\Scripts\Activate.ps1
```

2. Install required Python packages:

```powershell
pip install -r requirements.txt
```

Or install manually:

```powershell
pip install dash plotly pandas numpy
```

## Running the Dashboard

From the repository root, execute:

```powershell
python data/run_health_data.py
```

The dashboard will start on `http://localhost:8050`

## Project Structure

```
HealthCareNZ/
├── data/
│   ├── NZ_Health_Dataset.csv      # Generated health dataset
│   ├── run_health_data.py         # Main dashboard application
│   ├── health_dashboard.py        # Data generation script
│   ├── analysis_show.ipynb        # Jupyter notebook with analysis
│   └── show_health_data.ipynb     # Data exploration notebook
└── README.md
```

## Features

- **Year-based Filtering**: Analyze trends across 2024-2025 data
- **Multi-select Filters**: Compare multiple regions and diseases simultaneously
- **Age Group Analysis**: Understand disease distribution by age brackets (0-18, 19-35, 36-50, 51+)
- **Gender Demographics**: Visual breakdown of health cases by gender
- **Real-time Updates**: All charts update dynamically based on filter selections

## Dataset

The project uses a synthetic New Zealand health dataset with the following attributes:
- Patient ID
- Age (0-100)
- Gender (Male/Female)
- Region (Auckland, Wellington, Christchurch, Otago, Bay of Plenty, etc.)
- Disease (Heart Disease, Diabetes, Asthma, Flu, etc.)
- Number of Cases
- Year (2024-2025)

## Notes

- Run the script from the repository root to avoid path issues
- Debug mode is enabled for development; disable in production by setting `debug=False`
- To generate a `requirements.txt` file:

```powershell
pip freeze > requirements.txt
```

## Future Enhancements

- Export functionality (CSV, PDF reports)
- Time-series trend analysis
- Predictive analytics for disease outbreaks
- Regional comparison metrics

## License

MIT
