import sqlite3, pathlib
p = pathlib.Path.home() / '.gemini/antigravity/scratch/ai-aff-video-system/data/aff_system.db'
if p.exists():
    conn = sqlite3.connect(str(p))
    for t in [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
        cnt = conn.execute(f"SELECT count(1) FROM {t}").fetchone()[0]
        print(f"{t}: {cnt} rows")
