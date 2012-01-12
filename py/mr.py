# empty

import sqlite3
from mrjob.job import MRJob

def init_input():
    """Dumps data to a file from DB"""
    conn = sqlite3.connect('./data/db.sqlite3')
    cur = conn.cursor()

    f = open('./data/bug_files.txt', 'w')
    cur.execute("""
        SELECT commits_files.file
        FROM commits_files
        LEFT JOIN commits
        ON commits_files.commit_hash = commits.commit_hash
        WHERE commits.bug_id IS NOT NULL
    """)
    for res in cur:
        f.write(res[0] + '\n')

    f.close()
    conn.close()

class MRWordCounter(MRJob):
    """MapReduce"""
    def mapper(self, key, line):
        """Splits file path into subpaths and assigns weights"""
        paths = line.split('/')
        size = len(paths)
        divisor = sum(map(lambda x: x*x, range(size+1)))

        for i in range(size):
            yield '/'.join(paths[:i+1]), (i + 1.0)**2/divisor

    def reducer(self, path, weight):
        """Counts subpaths weights"""
        yield path, sum(weight)

def main():
    MRWordCounter.run()

if __name__ == '__main__':
    main()
