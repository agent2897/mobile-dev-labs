package com.mylenko.habits.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
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
import java.time.format.DateTimeFormatter
import java.util.Locale

private val dayFormat = DateTimeFormatter.ofPattern("EEEE, d MMMM", Locale("uk"))

/** Вкладка «Сьогодні»: прогрес дня та список звичок з відмітками */
@Composable
fun TodayScreen(habits: List<Habit>, onToggle: (Habit) -> Unit, onOpen: (Habit) -> Unit) {
    val today = LocalDate.now()
    val done = habits.count { it.isDoneOn(today) }

    LazyColumn(contentPadding = PaddingValues(bottom = 96.dp)) {
        item {
            Card(
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primary),
            ) {
                Column(Modifier.padding(20.dp)) {
                    Text(
                        today.format(dayFormat).replaceFirstChar { it.uppercase() },
                        color = Color.White.copy(alpha = 0.85f),
                    )
                    Text(
                        "Виконано $done з ${habits.size}",
                        color = Color.White, fontSize = 26.sp, fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(vertical = 8.dp),
                    )
                    LinearProgressIndicator(
                        progress = { if (habits.isEmpty()) 0f else done.toFloat() / habits.size },
                        modifier = Modifier.fillMaxWidth().height(8.dp).clip(CircleShape),
                        color = Color.White,
                        trackColor = Color.White.copy(alpha = 0.3f),
                    )
                }
            }
        }
        if (habits.isEmpty()) {
            item {
                Text(
                    "Звичок ще немає.\nНатисніть «+», щоб додати першу.",
                    textAlign = TextAlign.Center,
                    color = Color.Gray,
                    modifier = Modifier.fillMaxWidth().padding(40.dp),
                )
            }
        }
        items(habits, key = { it.id }) { habit ->
            HabitRow(habit, today, onToggle = { onToggle(habit) }, onClick = { onOpen(habit) })
        }
    }
}

@Composable
private fun HabitRow(habit: Habit, today: LocalDate, onToggle: () -> Unit, onClick: () -> Unit) {
    val color = Color(habit.color)
    val done = habit.isDoneOn(today)
    Card(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 5.dp).clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = Color.White),
    ) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(
                Modifier.size(46.dp).clip(CircleShape).background(color.copy(alpha = 0.15f)),
                contentAlignment = Alignment.Center,
            ) { Text(habit.emoji, fontSize = 22.sp) }
            Column(Modifier.weight(1f).padding(horizontal = 14.dp)) {
                Text(habit.name, fontWeight = FontWeight.SemiBold, fontSize = 16.sp)
                Text("🔥 Серія: ${habit.currentStreak(today)} дн.", color = Color.Gray, fontSize = 13.sp)
            }
            Box(
                Modifier.size(38.dp).clip(CircleShape)
                    .background(if (done) color else Color(0xFFE6E8F0))
                    .clickable(onClick = onToggle),
                contentAlignment = Alignment.Center,
            ) {
                if (done) Icon(Icons.Default.Check, contentDescription = "Виконано", tint = Color.White)
            }
        }
    }
}
