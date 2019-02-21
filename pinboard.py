import json
import sys

import requests
import codecs

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

    org_template = """* [[{href}][{description}]]   {joined_tags}
  :PROPERTIES:
  :TIME_SAVED: {time}
  :URL: {href}
  :END:
  {extended}
"""

    with codecs.open(orgfile, 'w', encoding='utf-8') as fout:
        fout.write(header)
        for l in json_lines:
            description = l['description']
            href = l['href']
            server_tags = l['tags'].split(' ')
            server_tags_fixed = [w.replace('-', '_') for w in server_tags]
            tags = list(filter(None, server_tags_fixed))
            if tags:
                joined_tags = ":".join([""] + tags + [""])
            else:
                joined_tags = ""
            server_time = datetime.datetime.strptime(l['time'],
                                                     '%Y-%m-%dT%H:%M:%SZ')
            org_time = org_time_format.format(server_time)

            extended = l['extended']
            org_line = org_template.format(description=description,
                                           href=href,
                                           joined_tags=joined_tags,
                                           time=org_time,
                                           extended=extended)
            # print("Writing: ", org_line.encode('utf-8'))
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
