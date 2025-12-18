import sqlite3
from config import path_db

# ------------------ SQL-запросы ------------------

CREATE_TABLE_HISTORY = """
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

INSERT_HISTORY = "INSERT INTO history (name, created_at) VALUES (?, ?);"
SELECT_HISTORY = "SELECT id, name, created_at FROM history;"
DELETE_LAST_HISTORY = "DELETE FROM history WHERE id = (SELECT MAX(id) FROM history);"
DELETE_ALL_HISTORY = "DELETE FROM history;"

# ------------------ Функции ------------------

def init_db():
    """Создаём таблицу истории приветствий"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_HISTORY)
    conn.commit()
    conn.close()

def add_name(name, created_at):
    """Добавляем имя в историю"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(INSERT_HISTORY, (name, created_at))
    conn.commit()
    conn.close()

def get_history():
    """Получаем всю историю"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(SELECT_HISTORY)
    data = cursor.fetchall()
    conn.close()
    return data

def delete_last():
    """Удаляем последнюю запись"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(DELETE_LAST_HISTORY)
    conn.commit()
    conn.close()

def delete_all():
    """Удаляем всю историю"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(DELETE_ALL_HISTORY)
    conn.commit()
    conn.close()