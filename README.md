# Pinboard Org

This is a simple Python helper script for exporting your information from
[Pinboard.in](https://pinboard.in) as an [Org mode](http://orgmode.org/) file to
use with Emacs.

## Python Version

Tested and working with Python 3.5.0.

## Usage

Install the requirements from `requirements.txt`.

Then, place your [api key](https://pinboard.in/settings/password) in `~/.netrc` as:

    machine api.pinboard.in login <user> password <password>

Where your api key is formatted as `<user>:<password>`. 

Finally, use it by running it as:

    python pinboard.py <outputfile>
    

