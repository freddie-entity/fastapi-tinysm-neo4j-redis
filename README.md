# TinySM

A simple implementation of FastAPI and following technologies below.

> This project is a backend part of the Tiny Social Media app (TinySM) for my school project.
> The frontend part is in https://github.com/freddie-entity/vite-tinysm

## Consist of

- FastAPI .
- Neo4j database.
- OAuth2
- Redis stream, pubsub, cache aside.

## Start the project

- Download git repo:

```console
git clone <thisisrepourl>
```

- Change working directory

```console
cd <folderyoujustcloned>
```

- Create new virtual environment to decouple packages from the original python

```console
python -m venv venv
```

- Activate the virtual environment just created.
- Jump to working directory to app `cd app`then run

```console
pip install -r requirements.txt
```

```console
python main.py
```

You create brand-new free neo4j auradb or sandbox instance in their official website and replace the credential in setting files.

The starter listens on http://localhost:8000

## FastAPI Docs

###### These are all of my api endpoints serving the frontend.

![](https://user-images.githubusercontent.com/74780149/142719071-1deb4ee8-004c-463d-914b-51f82edaf50d.PNG)
![](https://user-images.githubusercontent.com/74780149/142719096-0ed75e82-7f48-46b1-9e3f-ef9dd47363d3.PNG)
