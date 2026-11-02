package com.mylenko.habits.data

import java.time.LocalDate

/** Звичка та дати, коли її було виконано */
data class Habit(
    val id: Long,
    val name: String,
    val emoji: String,
    val color: Long,
    val createdAt: LocalDate,
    val doneDates: Set<LocalDate> = emptySet(),
) {
    fun isDoneOn(date: LocalDate) = date in doneDates

    /** Поточна серія: скільки днів поспіль виконано до сьогодні (або до вчора) */
    fun currentStreak(today: LocalDate = LocalDate.now()): Int {
        var day = if (isDoneOn(today)) today else today.minusDays(1)
        var count = 0
        while (isDoneOn(day)) {
            count++
            day = day.minusDays(1)
        }
        return count
    }

    /** Найдовша серія за весь час */
    fun bestStreak(): Int {
        var best = 0
        var run = 0
        var prev: LocalDate? = null
        for (d in doneDates.sorted()) {
            run = if (prev != null && prev.plusDays(1) == d) run + 1 else 1
            best = maxOf(best, run)
            prev = d
        }
        return best
    }

    /** Відсоток виконання за останні [days] днів */
    fun completionRate(days: Int, today: LocalDate = LocalDate.now()): Float {
        val from = today.minusDays(days.toLong() - 1)
        val done = doneDates.count { !it.isBefore(from) && !it.isAfter(today) }
        return done.toFloat() / days
    }
}
