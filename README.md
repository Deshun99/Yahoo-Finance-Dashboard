<div align="center">
  <a>
    <img src="Stock Analysis Dashboard.png" alt="Logo" width="1250">
  </a>
  <h3 align="center">Stock Analysis Dashboard</h3>
</div>

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

### _2. Google Colab Environment_

Our deep learning models were primarily trained on [Google Colab Pro](https://colab.research.google.com) due to the access to high performance GPUs required for the training of complex neural network systems. 

You can set up the Google Colab environment to run our model training codes by executing the following:

```py
from google.colab import drive
drive.mount('/content/drive')
content_path = "insert/path/to/your/data"
```
You will be prompted to log in with your Google Account. Simply replace the ```content_path``` with the path to directory where you have uploaded the data.

Alternatively, if you do not wish to authenticate with your Google Account, you may simply run the following code to retrieve the data from a permanent link:

```py
train_path = 'https://drive.google.com/uc?export=download&id=1ZTfYOXeZLW57mLR7IegIFovi7FW1chS6'
val_path = 'https://drive.google.com/uc?export=download&id=1ZMJI7DyKMLHpHp-HBUO64kWbP6A-qj9k'

train_df = pd.read_csv(train_path)
val_df = pd.read_csv(val_path)
```

The required additional modules required for each ```.ipynb``` notebook runned on Google Colab have been included in each notebook to be installed using ```pip```.

<p align="right">(<a href="#top">back to top</a>)</p>


## Source Layer

```
📦WebScrapper
 ┗ 📜reddit_scrapper.py
```

### Data Ingestion Sources

Our team extracted both structured and unstructred data from the following sources:

| Source | Description | Size |
| ----------- | ----------- | ----------- |
| [Reddit](https://www.reddit.com/) | Extracted using the [PRAW API](https://praw.readthedocs.io/en/stable/) endpoint | 16828 |
| [ChatGPT](https://chat.openai.com/chat) | Generated using ChatGPT 3.5 and 4 | 6043 |
| Confounding Dataset | Manually created to include confounding and additional hate & ads | 26676 |

### Reddit Scraper Agent
