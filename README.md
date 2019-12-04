[![Build Status](https://travis-ci.org/zwoefler/SciPy-Metadata-Analysis.svg?branch=master)](https://travis-ci.org/zwoefler/SciPy-Metadata-Analysis)
# SciPy Metadata Analysis
This repository extracts metadata information from scientifc papers throughout scientific databases with selenium

Currently, these information is beeing pulled from the papers:
- [X] Author names
- [X] Paper Title
- [X] DOI
- [X] Keywords
- [X] Publication Date
- [X] Journalname
- [X] Journal Impact Factor
- [X] Amount of Citations


## Current objective
Transform the project, so that the buildscript gets a file with a
link list, determines the scientific database and extracts all
relevant metadata into a json-file, containing all the meta information.
Automatically make some analysis regarding the gathered data. Such as correlations for authors and keywords or so.

## Goal
The goal is to learn and use [Selenium](https://selenium-python.readthedocs.io/) for webscrapping and deepen the knowledge of Python3.
Also to support my bachelor thesis.


## Usage
1. Clone this repository:
    - `git clone git@github.com:zwoefler/SciPy-Metadata-Analysis.git`
2. Create a virtual environment, named `Env` at the end to be ignored by git:
    - `python3 -m venv DevEnv`
3. Activate the environment:
    - `source DevEnv/bin/activate`
4. Install the requirements:
    - `pip install -r requirements.txt`
5. Install selenium:
    - Since Selenium is already installed with the `requirements.txt` you just need
    your browser driver. Download one of the following drivers and place it in your
    `/usr/bin` directory to be available from everywher:

    |Browser | Link                                                                     |
    |--------|--------------------------------------------------------------------------|
    |Firefox | https://github.com/mozilla/geckodriver/releases                          |
    |Chrome  | https://sites.google.com/a/chromium.org/chromedriver/downloads           |
    |Edge    | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/    |
    |Safari  | https://webkit.org/blog/6900/webdriver-support-in-safari-10/             |



# Origins of the Idea
My Bachelorthesis needed an meta data-analysis over all the relevant papers that i have found in online databases such as `Science Direct`, `IEEE` and `Springer Online`.
Since I already know the Pandas library for Python3, I wanted to gather the data as automatically as possible. Furthermore I was able to expand my knowledge in the field of webscrapping with `Selenium`.

# To implement

- [ ] Link recognition, so that the script knows which class it needs to call
- [X] ScienceDirect Integration
- [X] IEEE Integration
- [ ] SpringerLink:
    - [ ] Author names
    - [ ] Paper Title
    - [ ] DOI
    - [ ] Keywords
    - [ ] Publication Date
    - [ ] Journalname
    - [ ] Journal Impact Factor
    - [ ] Amount of Citations



# Lessons Learned
1. Improved my skills in Webscrapping with `Selenium`.
2. `Beautiful Soup` is not suitable for dynamic (JavaScript generated) webpage content



#### Author
[@zwoefler](https://github.com/zwoefler)