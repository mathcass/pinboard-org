import json
import sys

import requests
from requests.utils import get_netrc_auth

TMP_FILE = '/tmp/pinboard.json'  # May not exist in all platforms
default_params = {'format': 'json'}


def get_all():
    """Gets most recent posts from pinboard.in"""
    endpoint = "https://api.pinboard.in/v1/"
    user, token = get_netrc_auth(endpoint)
    auth_token = "{user}:{token}".format(user=user, token=token)
    params = {'auth_token': auth_token}
    params.update(default_params)
    r = requests.get(endpoint + "posts/all", params=params)
    return r.json()


def write_all_to_tmp_file(all_bookmarks):
    """Gets all of the bookmarks from pinboard.in and writes to file as json
    payload"""
    with open(TMP_FILE, 'w') as f:
        for bookmark in all_bookmarks:
            f.write(json.dumps(bookmark) + '\n')


def tmpjsonfile_to_orgfile(orgfile):
    """Gets the saved json to file"""
    import datetime
    import getpass

    with open(TMP_FILE) as f:
        json_lines = [json.loads(l) for l in f]

    # Each pinboard item must have:
    # * description
    # * time
    # * href
    # * tags
    # * extended (extended text along with it)

    user = getpass.getuser()
    org_time_format = '{0:[%Y-%m-%d %a %H:%M]}'
    now = org_time_format.format(datetime.datetime.now())
    header = """#+TITLE: Pinboard.in Export
#+AUTHOR: {user}
#+EXPORT_TIME: {time}

""".format(user=user,
           time=now)

    org_template = """* [[{href}][{description}]] {joined_tags}
  :PROPERTIES:
  :Time_Saved: {time}
  :END:
  {extended}
"""

    with open(orgfile, 'w') as fout:
        fout.write(header)
        for l in json_lines:
            description = l['description']
            href = l['href']
            tags = l['tags'].split(' ')
            time = l['time']
            extended = l['extended']
            org_line = org_template.format(description=description,
                                           href=href,
                                           joined_tags=":".join(tags),
                                           time=time,
                                           extended=extended)
            fout.write(org_line)


def main(output_file):
    """Main method"""
    all_bookmarks = get_all()
    write_all_to_tmp_file(all_bookmarks)
    tmpjsonfile_to_orgfile(output_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: pinboard.py <outputfile>")
        exit(1)
    output_file = sys.argv[1]
    main(output_file)
