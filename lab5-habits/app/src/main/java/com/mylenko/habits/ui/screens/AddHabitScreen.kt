package com.mylenko.habits.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val EMOJIS = listOf("💧", "🏃", "📚", "🧘", "🍎", "💪", "🇬🇧", "😴", "🎸", "✍️", "🚭", "💊")
private val COLORS = listOf(0xFF1E88E5, 0xFFE53935, 0xFF8E24AA, 0xFF43A047, 0xFFFB8C00, 0xFF546E7A, 0xFF00897B)

/** Екран створення нової звички */
@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun AddHabitScreen(onSave: (String, String, Long) -> Unit, onBack: () -> Unit) {
    var name by remember { mutableStateOf("") }
    var emoji by remember { mutableStateOf(EMOJIS.first()) }
    var color by remember { mutableStateOf(COLORS.first()) }
    var showError by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Нова звичка") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Назад")
                    }
                },
            )
        },
    ) { padding ->
        Column(Modifier.padding(padding).padding(16.dp)) {
            OutlinedTextField(
                value = name,
                onValueChange = { name = it; showError = false },
                label = { Text("Назва звички") },
                isError = showError,
                supportingText = { if (showError) Text("Введіть назву") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
            )
            Text("Іконка", style = MaterialTheme.typography.titleSmall, modifier = Modifier.padding(top = 12.dp, bottom = 8.dp))
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                EMOJIS.forEach { e ->
                    Box(
                        Modifier.size(48.dp).clip(RoundedCornerShape(12.dp))
                            .background(if (e == emoji) Color(color).copy(alpha = 0.2f) else Color.White)
                            .border(2.dp, if (e == emoji) Color(color) else Color.Transparent, RoundedCornerShape(12.dp))
                            .clickable { emoji = e },
                        contentAlignment = Alignment.Center,
                    ) { Text(e, fontSize = 22.sp) }
                }
            }
            Text("Колір", style = MaterialTheme.typography.titleSmall, modifier = Modifier.padding(top = 20.dp, bottom = 8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                COLORS.forEach { c ->
                    Box(
                        Modifier.size(38.dp).clip(CircleShape).background(Color(c)).clickable { color = c },
                        contentAlignment = Alignment.Center,
                    ) {
                        if (c == color) Icon(Icons.Default.Check, contentDescription = null, tint = Color.White)
                    }
                }
            }
            Spacer(Modifier.height(28.dp))
            Button(
                onClick = { if (name.isBlank()) showError = true else onSave(name.trim(), emoji, color) },
                modifier = Modifier.fillMaxWidth().height(52.dp),
            ) { Text("Зберегти", fontSize = 16.sp) }
        }
    }
}
