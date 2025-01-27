# Convaiid-Models
--------------------------------
## Models for Convaiid
-------------------------------
To run,

```bash
$pip install -r requirements.txt
```
or
```bash
$poetry install .
```

then run the following command to get API:

```bash
$uvicorn main:app --reload
```

-------------------------------
## With conda environment
-------------------------------
```bash
$conda env create -f environment.yml
```
activate the environment

```bash
$conda activate convaiid-models
```

then run the following command to get API:

```bash
$uvicorn main:app --reload
```
or
```bash
$Scripts\run.bat
```
-----------------------------
## With Docker
-----------------------------

```bash
$docker build -t convaiid-models .
```

