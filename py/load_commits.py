from xml.etree import ElementTree as ET
import datetime
import re
import sqlite3

def parse_date(el, obj):
    """Converts from ISO 8061 to YYYY-MM-DD HH:MM:SS and TZ

    >>> parse_date(ET.XML('<t>Fri Apr 22 08:32:04 2011 -0700</t>'), {})
    {'tz': -420, 't': '2011-04-22 01:32:04'}
    """
    tz = el.text[-5:]
    dt = el.text[:-6]
    tz = int(tz[:3])*60+int(tz[-2:]) # in min

    dt = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S %Y')
    delta = datetime.timedelta(minutes=tz)

    dt = dt + delta

    obj[el.tag] = dt.strftime('%Y-%m-%d %H:%M:%S')
    obj['tz'] = tz

    return obj

def parse_parent_hashes(el, obj):
    """Creates list of parents hashes
    
    >>> parse_parent_hashes(ET.XML('<t>one two three</t>'), {})
    {'parent_hashes': ['one', 'two', 'three']}
    """
    if el.text:
        obj['parent_hashes'] = el.text.split(' ')
    else:
        obj['parent_hashes'] = []

    return obj

BUG_PATTERN = re.compile(r'Bug.*?(\d+)')

def parse_message(element, obj):
    """Concats message lines. Sets bug_id if it exists within lines

    >>> parse_message(ET.XML('<t><l>Bug  123</l><l>asdf</l></t>'), {})
    {'bug_id': 123, 'message': 'asdf'}
    """
    bug = None
    msg = ''

    for el in element:
        res = BUG_PATTERN.match(el.text) 
        if res:
            bug = int(res.groups()[0])
        else:
            msg += el.text + '\n'

    obj['message'] = msg.rstrip()
    obj['bug_id'] = bug

    return obj

def parse_target(element, obj):
    """
    >>> parse_target(ET.XML('<c><t>one.sh</t><t>two.sh</t></c>'), {})
    {'files': ['one.sh', 'two.sh']}
    """
    files = []
    for el in element:
        files.append(el.text)
    obj['files'] = files

    return obj

def parse_change(element, obj):
    to_parse = ['project', 'commit_hash', 'tree_hash', 'parent_hashes',
        'author_e-mail', 'author_date', 'subject', 'message', 'target']
    for el in element:
        if el.tag == 'parent_hashes':
            parse_parent_hashes(el, obj)
        elif el.tag == 'author_date':
            parse_date(el, obj)
        elif el.tag == 'message':
            parse_message(el, obj)
        elif el.tag == 'target':
            parse_target(el, obj)
        else:
            if el.tag in to_parse:
                obj[el.tag] = el.text

    return obj

def grep_change(f):
    change = ''

    for line in f:
        line = line.strip()
        if (line == '<change>'):
            change = line
        elif (line == '</change>'):
            change += line
            return change
        else:
            change += line

    return None

def write_change(obj, conn, cur):
    cur.execute("""
        INSERT INTO commits(commit_hash, tree_hash, project, author,
            commit_date, tz, subject, message, bug_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
                obj['commit_hash'],
                obj['tree_hash'],
                obj['project'],
                obj['author_e-mail'],
                obj['author_date'],
                obj['tz'],
                obj['subject'],
                obj['message'],
                obj['bug_id']
        )
    ),
    for h in obj['parent_hashes']:
        cur.execute("""
            INSERT INTO commits_parents(commit_hash, parent_hash)
            VALUES (?, ?)
        """, (
                obj['commit_hash'],
                h
            )
        )

    for f in obj['files']:
        cur.execute("""
            INSERT INTO commits_files(commit_hash, commit_date, file)
            VALUES (?, ?, ?)
        """, (
                obj['commit_hash'],
                obj['author_date'],
                f
            )
        )

    conn.commit()

def main():
    f = open('./data/git.log.xml', 'r')
    conn = sqlite3.connect('./data/db.sqlite3')
    cur = conn.cursor()
    i = 0

    while True:
        change = grep_change(f)
        i += 1
        if change:
            if i % 10 == 0:
                print i
            try:
                write_change(parse_change(ET.XML(change), {}), conn, cur)
            except Exception:
                print change
        else:
            return

    cur.close()
    conn.close()
    f.close()

if __name__ == '__main__':
    main()
