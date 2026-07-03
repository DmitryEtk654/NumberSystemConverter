import sqlite3
from datetime import datetime

dbs = "history.db"

class HistoryManager:
    def __init__(self):
        self.conn = None
        self.init_db()
    
    def init_db(self):
        self.conn = sqlite3.connect(dbs)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                input_value TEXT NOT NULL,
                base_from INTEGER NOT NULL,
                base_to INTEGER NOT NULL,
                result TEXT NOT NULL
            )
        """)
        self.conn.commit()
    
    def add_record(self, input_value, base_from, base_to, result):
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO history (timestamp, input_value, base_from, base_to, result) VALUES (?, ?, ?, ?, ?)",
            (timestamp, input_value, base_from, base_to, result)
        )
        self.conn.commit()
    
    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY id DESC")
        return cursor.fetchall()
    
    def clear(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM history")
        self.conn.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()
