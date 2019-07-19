# Compare Gap Junctions

A python script that compare gap junctions from a catmaid project to the Durbin datasets

## Requirements

- Python 3.7
- Pipenv

## Usage

Install project dependencies
`pipenv install`

Edit config.py with your values for:
- ```token```: Your personal token for the CATMAID API
- ```project_id```: Your project id
- ```stack_id```: Your stack id

Run the script:
`pipenv run python compare_gap_junctions.py`