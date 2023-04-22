<div align="center">
  <a>
    <img src="Stock Analysis Dashboard.png" alt="Logo" width="1250">
  </a>
  <h3 align="center">Stock Analysis Dashboard</h3>
</div>

## Project Overview:

The objective of this project is to perform a stock analysis on the top 10 most active stocks in Singapore, to gain insights and make informed investment decisions based on the analysis .

## Codes and Resources Used

**Python Version:** 3.9.10

**Built with:** [Microsoft Visual Studio Code](https://code.visualstudio.com/), [Google Colab](https://colab.research.google.com/), [Streamlit](https://streamlit.io/), [Django](https://www.djangoproject.com/), [Git](https://git-scm.com/)

**Notable Packages:** praw, pandas, numpy, scikit-learn, xgboost, transformers, pytorch, torchvision, tqdm, streamlit, django (view requirements.txt for full list)

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

### **Prerequisites**

Make sure you have installed all of the following on your development machine:

- Python 3.8.X or 3.9.X

<p align="right">(<a href="#top">back to top</a>)</p>

### **Installation**

We recommend setting up a virtual environment to run this project.


### _1. Python Virtual Environment_

Installing and Creation of a Virtual Environment

```sh
pip install virtualenv
virtualenv <your_env_name>
source <your_env_name>/bin/active
```

The requirements.txt file contains Python libraries that your notebooks depend on, and they will be installed using:

```sh
pip install -r requirements.txt
```

### _2. Running On localhost_
 
```sh
python my_app.py
```

### Data Ingestion Sources

Our team extracted both structured and unstructred data from the following sources:

| Source | Description | Size |
| ----------- | ----------- | ----------- |
| [Yahoo Finance](https://sg.finance.yahoo.com/) | Extracted using the [yfinance](https://pypi.org/project/yfinance/) API | - |
