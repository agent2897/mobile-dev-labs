package com.mylenko.habits.data

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import java.time.LocalDate

/** Локальна база SQLite: таблиця звичок і таблиця відміток виконання */
class HabitDatabase(context: Context) : SQLiteOpenHelper(context, "habits.db", null, 1) {

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(
            """CREATE TABLE habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                emoji TEXT NOT NULL,
                color INTEGER NOT NULL,
                created_at TEXT NOT NULL)"""
        )
        db.execSQL(
            """CREATE TABLE completions (
                habit_id INTEGER NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
                date TEXT NOT NULL,
                PRIMARY KEY (habit_id, date))"""
        )
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        db.execSQL("DROP TABLE IF EXISTS completions")
        db.execSQL("DROP TABLE IF EXISTS habits")
        onCreate(db)
    }

    override fun onConfigure(db: SQLiteDatabase) {
        db.setForeignKeyConstraintsEnabled(true)
    }

    fun getAll(): List<Habit> {
        val done = mutableMapOf<Long, MutableSet<LocalDate>>()
        readableDatabase.rawQuery("SELECT habit_id, date FROM completions", null).use { c ->
            while (c.moveToNext()) {
                done.getOrPut(c.getLong(0)) { mutableSetOf() }.add(LocalDate.parse(c.getString(1)))
            }
        }
        val result = mutableListOf<Habit>()
        readableDatabase.rawQuery("SELECT id, name, emoji, color, created_at FROM habits ORDER BY id", null)
            .use { c ->
                while (c.moveToNext()) {
                    val id = c.getLong(0)
                    result += Habit(
                        id = id,
                        name = c.getString(1),
                        emoji = c.getString(2),
                        color = c.getLong(3),
                        createdAt = LocalDate.parse(c.getString(4)),
                        doneDates = done[id] ?: emptySet(),
                    )
                }
            }
        return result
    }

    fun insert(name: String, emoji: String, color: Long, createdAt: LocalDate = LocalDate.now()): Long =
        writableDatabase.insert("habits", null, ContentValues().apply {
            put("name", name)
            put("emoji", emoji)
            put("color", color)
            put("created_at", createdAt.toString())
        })

    fun delete(id: Long) {
        writableDatabase.delete("habits", "id = ?", arrayOf(id.toString()))
    }

    fun setDone(habitId: Long, date: LocalDate, done: Boolean) {
        if (done) {
            writableDatabase.insertWithOnConflict("completions", null, ContentValues().apply {
                put("habit_id", habitId)
                put("date", date.toString())
            }, SQLiteDatabase.CONFLICT_IGNORE)
        } else {
            writableDatabase.delete(
                "completions", "habit_id = ? AND date = ?", arrayOf(habitId.toString(), date.toString())
            )
        }
    }

    fun clear() {
        writableDatabase.delete("habits", null, null)
    }
}
