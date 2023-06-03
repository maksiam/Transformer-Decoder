Transformer-Decoder
==============================

A short description of the project.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── mlruns             <- Backend store and artifact store fro MLflow
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks.
    │                        
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── data_extraction.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── data_tokenize.py
    │   │
    │   └── models         <- Scripts to train models and then use trained models to make
    │       │                 predictions
    │       ├── predict_model.py
    │       ├── model.py
    │       ├── utils.py
    │       └── train_model.py
    │
    ├── poetry.lock        <- Poetry processes all dependencies in your pyproject.toml file and locks them into the poetry.lock file
    │
    ├── pyproject.toml     <- specified file format of PEP 518 which contains the build system requirements of Python projects.
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------
# Установка проекта  
Клонируем репозиторий и переходим в него
```shell
git clone https://github.com/maksiam/Transformer-Decoder
cd Transformer-Decoder
```
Устанавливаем библиотеку Poetry
```shell
pip install poetry
```
Указываем путь для создания виртуальной среды, заменяем path/for/venv (можно не указывать, тогда расположится по дефолту)
```shell
poetry config virtualenvs.path path/for/venv
```
Устанавливаем зависимости
```shell
poetry install
```
Переходим в shell виртуальной среды
```shell
poetry shell
```
Устанавливаем все данные с помощью dvc из S3-хранилища (ВНИМАНИЕ! Модель может занимать около 1Гб места)
```shell
dvc pull
```
# Генерация текста
Запускаем файл predict_model.py, передаем на вход аргументы: начало предложения, количество токенов для генерации, путь до модели
```shell
python src\models\predict_model.py "Гарри Поттер вошел в комнату и " 100 "models\model.pt"
```
Пример вывода

# Обучение модели
Запускаем файл train_model.py, который забирает параметры модели из файла src\models\utils.py
```shell
python src\models\train_model.py
```
