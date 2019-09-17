# Compare Gap Junctions

A python script to compare gap junctions from a catmaid project to the Durbin datasets

## Requirements

- Python 2
- Pipenv

## Usage

Install project dependencies
`pipenv install`

Edit config.py with your values for:
- ```token```: Your personal token for the CATMAID API
- ```project_id```: Your project id
- ```stack_id```: Your stack id
- ```jsh_project_id```: Id for the jsh project
- ```jsh_stack_id```: Stack id for the jsh project
- ```n2u_project_id```: Id for the n2u project
- ```n2u_stack_id```: Stack id for the n2u project

Run the script with pipenv:

`pipenv run python compare_gap_junctions.py`

OR

Run the script with python:
`python compare_gap_junctions.py`

The output folder will contain the csv files for the difference, and intersections.
