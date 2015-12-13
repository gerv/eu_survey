# EUSurvey bridge

This tool gathers and maps EUSurvey fields into a LimeSurvey format.


## Installation

To install grab a copy of the repository.

Install the requirements:

    pip install -r requirements.txt


And install the python package with:

    python setup develop


## Import a survey

The command to import a survey is:

    survey.py --ingest URL

Where `URL` is a EUSurvey URL. e.g.

    survey.py --ingest https://ec.europa.eu/eusurvey/runner/Platforms/


An `--update` flag is available in case the form has been re-configured for import.

**IMPORTANT:** This command will overwrite without confirmation any existing file that it requires. e.g.

    survey.py --ingest https://ec.europa.eu/eusurvey/runner/Platforms/ --update


# Submit exported answers to a survey

Once the survey answers are ready to be sent back to the EUSurvey service they must be exported with:

- A CSV file format.
- Headings using the "question code".
- Using "answer codes" without converting the `Y` and `N` values.

After this data has been exported it must be placed inside the `db` directory of the survey. The tool will detect the file if using the LimeSurvey default export filename.

After this is completed the form is ready to be sent to the service with the following command:

    survey.py --forward URL

Where `URL` is a EUSurvey URL. e.g.

    survey.py --forward https://ec.europa.eu/eusurvey/runner/Platforms/

This command will send back the survey exports one by one. Please note that the tool will stop if a row is not ready to be sent.


# DB structure

When a survey is imported a file structure is created to record the survey and any submissions, and its current state.

Structure:

    db/{ SURVEY_NAME }/
    ├── answers-export.csv
    ├── config.cfg
    ├── limesurvey.txt
    ├── limesurvey_map.csv
    ├── source.html
    ├── submissions/
    └── submissions.csv

Where:

- `SURVEY_NAME`: Name of the survey.
- `config.cfg`: Configuration file of the survey.
- `limesurvey.txt`: CSV tab separated representation of the survey ready to be consumed by LimeSurvey.
- `limesurvey_map.csv`: A CSV file that can be used to map other limesurvey answers exports to the current ingested survey.
- `source.html`: Cached original form used to generate the survey export.
- `submisions/`: Directory with an HTML file with the response for each submission sent.
- `submissions.csv`: CSV file listing all the survey submissions sent to the EUSurvey service.


# Mapping a survey

When another LimeSurvey needs to be mapped to a survey generated by this tool it can be done by:

**1. Exporting the answers database from the origin survey**

Once the survey that will be translated is ready to be processed it will need to be exported, placed inside the `db` folder of the tool generated survey and named `untranslated.csv`

e.g.

    db/httpseceuropaeueusurveyrunnerplatforms/untranslated.csv

**2. Update the map file in the tool survey**

The map file is called `limesurvey_map.csv` and contains the expected fields by the tool generated survey.

In this file the `translation` column must be updated with the `name` equivalent values of the survey that will be translated.

**3. Run the importer command**

This command will generate a translated survey result in the DB folder `translated.csv`. This file will have the required columns for the submissions to be sent to the EUSurvey service.

Usage:

   survey.py --map https://ec.europa.eu/eusurvey/runner/Platforms/