import os
import sqlite3

if __name__ == '__main__':
    databases = list(filter(lambda x: x.endswith('.db'), os.listdir('data')))
    print("Available databases:")
    for file in databases:
        print(f"[{databases.index(file)}] {file}")
    database_choice = databases[int(input("Select database : "))]
    before = int(os.path.getsize(f'data/{database_choice}') * 10e-7)
    db = sqlite3.connect(f"data/{database_choice}", check_same_thread=False)
    print("Vacuuming...")
    db.execute("VACUUM;")
    after = int(os.path.getsize(f'data/{database_choice}') * 10e-7)
    print(f"Done. {before}Mb -> {after}Mb")
