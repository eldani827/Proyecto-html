import sqlite3
from collections import defaultdict
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute("SELECT app, name FROM django_migrations ORDER BY app, name")
rows = cur.fetchall()
d = defaultdict(list)
for r in rows:
    d[r[0]].append(r[1])
print('Total migrations recorded:', len(rows))
for app, names in sorted(d.items()):
    print(app, len(names))
    for n in names:
        print('  ', n)
conn.close()
