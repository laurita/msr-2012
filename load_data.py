from xml.etree import ElementTree as ET
from datetime import datetime
import sqlite3

def parse_email(el, obj):
    """Delete three dots from email address

    >>> parse_email(ET.XML('<t>foo...@bar.com</t>'), {})
    {'t': 'foo@bar.com'}
    """
    if el.text == 'null':
        obj[el.tag] = None
    else:
        obj[el.tag] = el.text.replace('...', '')

    return obj

def parse_date(el, obj):
    """Converts from RFC 2822 or ISO 8061 to YYYY-MM-DD HH:MM:SS

    >>> parse_date(ET.XML('<t>Fri, 21 May 2010 05:18:13 +0000</t>'), {})
    {'t': '2010-05-21 05:18:13'}
    >>> parse_date(ET.XML('<t>2010-08-10T04:20:10.000Z</t>'), {})
    {'t': '2010-08-10 04:20:10'}
    """
    if el.text == 'null':
        obj[el.tag] = None
    else:
        try:
            dt = datetime.strptime(el.text, '%a, %d %b %Y %H:%M:%S +0000')
        except ValueError:
            dt = datetime.strptime(el.text, '%Y-%m-%dT%H:%M:%S.000Z')

        obj[el.tag] = dt.strftime('%Y-%m-%d %H:%M:%S')

    return obj

def parse_comment(element, obj):
    comment_obj = {}
    for el in element:
        if el.tag == 'author':
            comment_obj = parse_email(el, comment_obj)
        elif el.tag == 'when':
            comment_obj = parse_date(el, comment_obj)
        else:
            comment_obj[el.tag] = el.text

    if 'comment' in obj:
        obj['comment'].append(comment_obj)
    else:
        obj['comment'] = [comment_obj]

    return obj

def parse_bug(element, obj):
    for el in element:
        if el.tag == 'owner':
            obj = parse_email(el, obj)
        elif el.tag == 'closedOn':
            obj = parse_date(el, obj)
        elif el.tag == 'reportedBy':
            obj = parse_email(el, obj)
        elif el.tag == 'openedDate':
            obj = parse_date(el, obj)
        elif el.tag == 'comment':
            obj = parse_comment(el, obj)
        else:
            obj[el.tag] = el.text

    return obj

def grep_bug(f):
    bug = ''

    for line in f:
        line = line.rstrip()
        if (line == '<bug>'):
            bug = line
        elif (line == '</bug>'):
            bug += line
            return bug
        else:
            bug += line

    return None

def write_bug(obj, conn, cur):
    cur.execute("""
        INSERT INTO bugs(bug_id, title, status, owner, closed_on, type,
            priority, component, stars, reported_by,
            opened_date, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
                obj['bugid'],
                obj['title'],
                obj['status'],
                obj['owner'],
                obj['closedOn'],
                obj['type'],
                obj['priority'],
                obj['component'],
                obj['stars'],
                obj['reportedBy'],
                obj['openedDate'],
                obj['description'],
        )
    ),
    obj['comment'] = ('comment' in obj) and obj['comment'] or []
    for c in obj['comment']:
        cur.execute("""
            INSERT INTO comments(bug_id, author, comment_date, what)
            VALUES (?, ?, ?, ?)
        """, (
                obj['bugid'],
                c['author'],
                c['when'],
                c['what'],
            )
        )

    conn.commit()

def main():
    f = open('./data/android_platform_bugs.xml', 'r')
    conn = sqlite3.connect('./data/db.sqlite3')
    cur = conn.cursor()

    while True:
        bug = grep_bug(f)
        if bug:
            write_bug(parse_bug(ET.XML(bug), {}), conn, cur)
        else:
            return

    cur.close()
    conn.close()
    f.close()

if __name__ == '__main__':
    main()
