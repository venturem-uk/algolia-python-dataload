# Algolia Data Loader

This is a small python project to load the offline data from "payload.json" file to Algolia index.

## Introduction

- Sets up the imports needed for running the indexing
- Loads the data file from local data directory to json
- Uploads the json data to algolia index by creating a client
- Finishes off by sending a * query and printing number of results
- TODO - add an assertion to confirm that local data count equals algolia result count

## Running
* Assuming that you have python and pip installed on the machine.

- Activate the environment by ```source .env/bin/activate```
- Install the dependencies by ```pip install -r requirements.txt```
- Esnure that log directory exists ```mkdir logs```
- Run the program by ```python main.py```


