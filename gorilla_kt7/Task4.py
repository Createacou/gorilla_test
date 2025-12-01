import pytest
import aiosqlite
import os
import asyncio

DB_PATH = ":memory:"  # Используем in-memory базу для теста

async def insert_user(name: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor = await db.execute("INSERT INTO users (name) VALUES (?)", (name,))
        await db.commit()
        return cursor.lastrowid

@pytest.mark.asyncio
async def test_insert_user_adds_record(event_loop):
    user_id = await insert_user("Alice")
    assert user_id is not None

    # Проверка, что запись действительно добавлена
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT name FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        assert row is not None
        assert row[0] == "Alice"