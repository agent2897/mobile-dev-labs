package com.mylenko.habits.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.mylenko.habits.data.Habit
import java.time.LocalDate
import java.time.YearMonth
import java.time.format.DateTimeFormatter
import java.util.Locale

private val monthFormat = DateTimeFormatter.ofPattern("LLLL yyyy", Locale("uk"))
private val WEEK = listOf("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")

/** Екран звички: статистика, календар місяця (натискання змінює відмітку) та видалення */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HabitDetailScreen(
    habit: Habit,
    onToggleDate: (LocalDate) -> Unit,
    onDelete: () -> Unit,
    onBack: () -> Unit,
) {
    var month by remember { mutableStateOf(YearMonth.now()) }
    var confirmDelete by remember { mutableStateOf(false) }
    val color = Color(habit.color)

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("${habit.emoji} ${habit.name}") },
                navigationIcon = {
                    IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, "Назад") }
                },
                actions = {
                    IconButton(onClick = { confirmDelete = true }) { Icon(Icons.Default.Delete, "Видалити") }
                },
            )
        },
    ) { padding ->
        Column(Modifier.padding(padding).verticalScroll(rememberScrollState()).padding(16.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                StatCard("🔥", "${habit.currentStreak()}", "Поточна серія", Modifier.weight(1f))
                StatCard("🏆", "${habit.bestStreak()}", "Найкраща серія", Modifier.weight(1f))
                StatCard("✅", "${habit.doneDates.size}", "Усього днів", Modifier.weight(1f))
            }
            Card(
                modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
            ) {
                Column(Modifier.padding(12.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        IconButton(onClick = { month = month.minusMonths(1) }) {
                            Icon(Icons.AutoMirrored.Filled.KeyboardArrowLeft, "Попередній місяць")
                        }
                        Text(
                            month.format(monthFormat).replaceFirstChar { it.uppercase() },
                            modifier = Modifier.weight(1f), textAlign = TextAlign.Center,
                            fontWeight = FontWeight.SemiBold, fontSize = 17.sp,
                        )
                        IconButton(onClick = { month = month.plusMonths(1) }, enabled = month < YearMonth.now()) {
                            Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, "Наступний місяць")
                        }
                    }
                    MonthGrid(month, habit, color, onToggleDate)
                }
            }
            Text(
                "Виконання за 30 днів: ${(habit.completionRate(30) * 100).toInt()}%",
                modifier = Modifier.padding(top = 16.dp), fontSize = 15.sp,
            )
            LinearProgressIndicator(
                progress = { habit.completionRate(30) },
                modifier = Modifier.fillMaxWidth().padding(top = 8.dp).height(8.dp).clip(CircleShape),
                color = color,
            )
        }
    }

    if (confirmDelete) {
        AlertDialog(
            onDismissRequest = { confirmDelete = false },
            title = { Text("Видалити звичку?") },
            text = { Text("Історію виконання «${habit.name}» буде втрачено.") },
            confirmButton = { TextButton(onClick = { confirmDelete = false; onDelete() }) { Text("Видалити") } },
            dismissButton = { TextButton(onClick = { confirmDelete = false }) { Text("Скасувати") } },
        )
    }
}

@Composable
private fun StatCard(icon: String, value: String, label: String, modifier: Modifier) {
    Card(modifier, colors = CardDefaults.cardColors(containerColor = Color.White)) {
        Column(Modifier.fillMaxWidth().padding(vertical = 12.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(icon, fontSize = 20.sp)
            Text(value, fontSize = 22.sp, fontWeight = FontWeight.Bold)
            Text(label, fontSize = 11.sp, color = Color.Gray, textAlign = TextAlign.Center)
        }
    }
}

@Composable
private fun MonthGrid(month: YearMonth, habit: Habit, color: Color, onToggleDate: (LocalDate) -> Unit) {
    val today = LocalDate.now()
    val offset = month.atDay(1).dayOfWeek.value - 1
    val cells = offset + month.lengthOfMonth()
    Row {
        WEEK.forEach {
            Text(it, Modifier.weight(1f), textAlign = TextAlign.Center, fontSize = 12.sp, color = Color.Gray)
        }
    }
    for (week in 0 until (cells + 6) / 7) {
        Row {
            for (dow in 0 until 7) {
                val dayNum = week * 7 + dow - offset + 1
                Box(Modifier.weight(1f).aspectRatio(1f).padding(3.dp), contentAlignment = Alignment.Center) {
                    if (dayNum in 1..month.lengthOfMonth()) {
                        val date = month.atDay(dayNum)
                        val done = habit.isDoneOn(date)
                        val future = date.isAfter(today)
                        Box(
                            Modifier.fillMaxSize().clip(CircleShape)
                                .background(if (done) color else Color.Transparent)
                                .clickable(enabled = !future) { onToggleDate(date) },
                            contentAlignment = Alignment.Center,
                        ) {
                            Text(
                                "$dayNum",
                                color = when {
                                    done -> Color.White
                                    future -> Color.LightGray
                                    else -> Color.DarkGray
                                },
                                fontWeight = if (date == today) FontWeight.Bold else FontWeight.Normal,
                            )
                        }
                    }
                }
            }
        }
    }
}
