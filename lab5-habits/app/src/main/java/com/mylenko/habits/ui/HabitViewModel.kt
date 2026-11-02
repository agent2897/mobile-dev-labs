package com.mylenko.habits.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.mylenko.habits.data.Habit
import com.mylenko.habits.data.HabitDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.time.LocalDate
import kotlin.random.Random

/** ViewModel: читає та змінює дані в базі у фоновому потоці, віддає стан у StateFlow */
class HabitViewModel(app: Application) : AndroidViewModel(app) {

    private val db = HabitDatabase(app)
    private val _habits = MutableStateFlow<List<Habit>>(emptyList())
    val habits: StateFlow<List<Habit>> = _habits.asStateFlow()

    init {
        refresh()
    }

    private fun io(block: () -> Unit) = viewModelScope.launch(Dispatchers.IO) {
        block()
        _habits.value = db.getAll()
    }

    fun refresh() = io { }

    fun add(name: String, emoji: String, color: Long) = io { db.insert(name, emoji, color) }

    fun delete(id: Long) = io { db.delete(id) }

    fun toggle(habit: Habit, date: LocalDate = LocalDate.now()) =
        io { db.setDone(habit.id, date, !habit.isDoneOn(date)) }

    fun clearAll() = io { db.clear() }

    /** Демонстраційні звички з історією за останні 40 днів */
    fun addDemoData() = io {
        val today = LocalDate.now()
        val rnd = Random(5)
        val demo = listOf(
            Triple("Пити 2 л води", "💧", 0xFF1E88E5) to 0.9,
            Triple("Ранкова зарядка", "🏃", 0xFFE53935) to 0.7,
            Triple("Читати 20 сторінок", "📚", 0xFF8E24AA) to 0.6,
            Triple("Вивчати англійську", "🇬🇧", 0xFF43A047) to 0.8,
            Triple("Лягти до 23:00", "😴", 0xFF546E7A) to 0.45,
        )
        for ((info, chance) in demo) {
            val id = db.insert(info.first, info.second, info.third, today.minusDays(40))
            for (d in 1L..40L) {
                if (rnd.nextDouble() < chance) db.setDone(id, today.minusDays(d), true)
            }
        }
    }
}
