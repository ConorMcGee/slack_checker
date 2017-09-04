# Slack Channel User Metrics

## Installation

### Prerequisites:

This code has only been tested on Linux and Mac OS, although it should be straight forward to run on Windows as well.

Your computer should have a version of Python installed - Mac OS comes with Python 2.7 installed by default.

You will need `pip`, the python package manager. Details for installing that can be found [here](https://pip.pypa.io/en/stable/installing/).

### Quick install

If everything is working properly, you should be able to skip the next few steps by running `./install.sh`.

### Install third-party packages

After cloning the repository, install the necessary python packages using:
`pip install --user -r requirements.txt`

NOTE: If you've used python before you're probably already using virtualenvs so you'd probably be better off using on here.

## Creating a config file

Before running the script, you must create a yaml config file in the repo named `config.yaml`, in which we place the slack auth token, the channel name and the time period to examine.
Example:
```
token: "your_really_long_slack_token"
channel_name: "channel-name"
weeks: 4
```

`weeks` is an optional setting, and will default to `12` if left out.


## Running the programme

Run the script with:
`python scrape.py`


## Viewing the results in table format

The results will be saved in the `slack_results.csv` file in the same directory. You should be able to open this file in any Excel-like application.
