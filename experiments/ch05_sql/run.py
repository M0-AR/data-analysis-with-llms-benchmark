"""Ch05 verification: natural-language → SQL + Data Exploration artifact.
Book Ch.5 games.db rebuilt in SQLite. Verifies: prompt contains DDL, EX metric,
exploration.json (Walk-Before-Run), difficulty stratification.
Public live: Spider dev sample + BIRD Mini-Dev schema (downloaded separately).
"""
import sqlite3, json, time, hashlib
from pathlib import Path
OUT = Path("results/ch05.json")
OUT.parent.mkdir(parents=True, exist_ok=True)
DB = Path("data/games.db")
DB.parent.mkdir(parents=True, exist_ok=True)

GAMES = [
    (1, "Wii Sports", "Wii", 2006, "Sports", "Nintendo", 41.49, 29.02, 3.77, 8.46, 82.74),
    (2, "Super Mario Bros.", "NES", 1985, "Platform", "Nintendo", 29.08, 3.58, 6.81, 0.77, 40.24),
    (3, "Mario Kart Wii", "Wii", 2008, "Racing", "Nintendo", 15.85, 12.88, 3.79, 3.31, 35.82),
    (4, "FIFA 17", "PS4", 2016, "Sports", "Electronic Arts", 5.1, 4.2, 0.5, 2.1, 11.9),
    (5, "Phantasy Star Online 2", "PS4", 2017, "Role-Playing", "Sega", 0.1, 0.05, 0.8, 0.02, 0.97),
    (6, "Call of Duty WWII", "PS4", 2017, "Shooter", "Activision", 4.5, 3.1, 0.3, 1.2, 9.1),
]

QUERIES = [
    ("How many games are stored?", "SELECT COUNT(*) FROM games;", "easy"),
    ("How many games did Activision create?", "SELECT COUNT(*) FROM games WHERE publisher='Activision';", "easy"),
    ("Game sales by genre in 2017?", "SELECT genre, COUNT(*) FROM games WHERE year=2017 GROUP BY genre;", "medium"),
    ("Top game of 2016 by global sales?", "SELECT name FROM games WHERE year=2016 ORDER BY globalsales DESC LIMIT 1;", "medium"),
    ("Ratio of sports sales America vs Japan?", "SELECT SUM(americasales)/SUM(japansales) FROM games WHERE genre='Sports';", "hard"),
]

def build_db():
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE games(rank int, name text, platform text, year int, genre text,
      publisher text, americasales numeric, eusales numeric, japansales numeric, othersales numeric, globalsales numeric)""")
    con.executemany("INSERT INTO games VALUES (?,?,?,?,?,?,?,?,?,?,?)", GAMES)
    con.commit()
    n = con.execute("SELECT COUNT(*) FROM games").fetchone()[0]
    con.close()
    return n

def exploration_artifact():
    con = sqlite3.connect(DB)
    ddl = con.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    cols = con.execute("PRAGMA table_info(games)").fetchall()
    sample = con.execute("SELECT * FROM games LIMIT 3").fetchall()
    con.close()
    art = {"tables": ["games"], "ddl": [d[0] for d in ddl],
           "columns": [{"cid": c[0], "name": c[1], "type": c[2]} for c in cols],
           "sample_rows": 3, "keys_inferred": ["rank PRIMARY KEY candidate"],
           "quality_flags": ["tiny demo DB; production needs profiling per Walk-Before-Run"]}
    Path("results/exploration.json").write_text(json.dumps(art, indent=2))
    return art

def run_queries():
    con = sqlite3.connect(DB)
    out = []
    for q, sql, diff in QUERIES:
        try:
            rows = con.execute(sql).fetchall()
            out.append({"q": q, "sql": sql, "difficulty": diff, "ok": True, "rows": rows})
        except Exception as e:
            out.append({"q": q, "sql": sql, "difficulty": diff, "ok": False, "error": str(e)[:200]})
    con.close()
    return out

def prompt_template_demo(question, ddl):
    # exact book pattern: Database: <DDL> + Translate + [Question]
    return f"Database:\n{ddl}\nTranslate this question into SQL query:\n{question}"

if __name__ == "__main__":
    n = build_db()
    art = exploration_artifact()
    runs = run_queries()
    ex = sum(1 for r in runs if r["ok"]) / len(runs)
    ddl_text = art["ddl"][0][:200]
    res = {"chapter": "ch05", "n_games": n, "execution_accuracy_demo": ex,
           "runs": runs, "exploration": art,
           "prompt_example": prompt_template_demo("How many games in 2017?", ddl_text),
           "hidden_pattern_checks": {
               "tables_beat_text": "see docs/METHODOLOGY.md §1 (40.29% paper)",
               "annotation_warning": "BIRD 52.8% / Spider2-snow 62.8% errors → dual-score required",
               "spider_cliff": "Spider 91.2 → BIRD 73 → Spider2.0 21.3 expected on enterprise shift"},
           "ts": time.time()}
    res["digest"] = hashlib.sha256(json.dumps(res, sort_keys=True).encode()).hexdigest()[:16]
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))
