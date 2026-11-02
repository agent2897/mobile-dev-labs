package com.mylenko.habits

import com.mylenko.habits.data.Habit
import org.junit.Assert.assertEquals
import org.junit.Test
import java.time.LocalDate

class HabitTest {
    private val today = LocalDate.of(2026, 11, 10)

    private fun habit(vararg daysAgo: Long) =
        Habit(1, "Тест", "✅", 0, today.minusDays(30), daysAgo.map { today.minusDays(it) }.toSet())

    @Test
    fun currentStreakCountsBackFromToday() {
        assertEquals(3, habit(0, 1, 2, 5).currentStreak(today))
    }

    @Test
    fun currentStreakStartsFromYesterdayIfTodayNotDone() {
        assertEquals(2, habit(1, 2, 4).currentStreak(today))
    }

    @Test
    fun bestStreakFindsLongestRun() {
        assertEquals(4, habit(0, 1, 5, 6, 7, 8, 12).bestStreak())
    }

    @Test
    fun completionRateOverPeriod() {
        assertEquals(0.5f, habit(0, 2, 4, 6, 8).completionRate(10, today))
    }
}
