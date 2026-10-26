import sqlite3
conn = sqlite3.connect('aff_system.db')
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('Tables:', tables)
for t in tables:
    cnt = conn.execute(f"SELECT count(1) FROM {t}").fetchone()[0]
    print(f" - {t}: {cnt} rows")
