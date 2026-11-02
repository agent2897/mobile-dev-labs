package com.mylenko.habits.ui.screens

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.mylenko.habits.data.Habit
import java.time.LocalDate
import java.time.format.TextStyle
import java.util.Locale

/** Вкладка «Статистика»: діаграма за 7 днів та відсоток виконання кожної звички */
@Composable
fun StatsScreen(habits: List<Habit>) {
    val today = LocalDate.now()
    val days = (6 downTo 0).map { today.minusDays(it.toLong()) }
    val counts = days.map { d -> habits.count { it.isDoneOn(d) } }
    val primary = MaterialTheme.colorScheme.primary

    Column(Modifier.verticalScroll(rememberScrollState()).padding(16.dp)) {
        Text("Останні 7 днів", style = MaterialTheme.typography.titleLarge)
        Text("Виконано звичок за кожен день", color = Color.Gray)
        Card(
            modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
        ) {
            Column(Modifier.padding(16.dp)) {
                // стовпчикова діаграма, намальована на Canvas
                Canvas(Modifier.fillMaxWidth().height(160.dp)) {
                    val max = maxOf(habits.size, 1)
                    val slot = size.width / days.size
                    for (i in 0..max) {
                        val y = size.height * i / max
                        drawLine(Color(0xFFE6E8F0), Offset(0f, y), Offset(size.width, y), 2f)
                    }
                    counts.forEachIndexed { i, c ->
                        val h = size.height * c / max
                        drawRoundRect(
                            color = if (i == days.lastIndex) primary else primary.copy(alpha = 0.5f),
                            topLeft = Offset(i * slot + slot * 0.2f, size.height - h),
                            size = Size(slot * 0.6f, h),
                            cornerRadius = CornerRadius(12f, 12f),
                        )
                    }
                }
                Row(Modifier.padding(top = 6.dp)) {
                    days.forEachIndexed { i, d ->
                        Column(Modifier.weight(1f)) {
                            Text("${counts[i]}", Modifier.fillMaxWidth(), textAlign = TextAlign.Center, fontWeight = FontWeight.Bold)
                            Text(
                                d.dayOfWeek.getDisplayName(TextStyle.SHORT, Locale("uk")),
                                Modifier.fillMaxWidth(), textAlign = TextAlign.Center, fontSize = 12.sp, color = Color.Gray,
                            )
                        }
                    }
                }
            }
        }
        Text("Виконання за 30 днів", style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(top = 8.dp))
        if (habits.isEmpty()) Text("Немає даних", color = Color.Gray, modifier = Modifier.padding(top = 8.dp))
        habits.sortedByDescending { it.completionRate(30) }.forEach { h ->
            val rate = h.completionRate(30)
            Column(Modifier.padding(vertical = 8.dp)) {
                Row {
                    Text("${h.emoji}  ${h.name}", Modifier.weight(1f))
                    Text("${(rate * 100).toInt()}%  ·  🏆 ${h.bestStreak()}", fontWeight = FontWeight.SemiBold)
                }
                LinearProgressIndicator(
                    progress = { rate },
                    modifier = Modifier.fillMaxWidth().padding(top = 6.dp).height(8.dp).clip(CircleShape),
                    color = Color(h.color),
                    trackColor = Color(0xFFE6E8F0),
                )
            }
        }
    }
}
