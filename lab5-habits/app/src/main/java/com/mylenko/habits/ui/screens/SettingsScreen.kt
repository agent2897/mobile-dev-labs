package com.mylenko.habits.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color

/** Вкладка «Налаштування»: демо-дані, очищення бази, інформація про додаток */
@Composable
fun SettingsScreen(habitCount: Int, onDemo: () -> Unit, onClear: () -> Unit) {
    var confirm by remember { mutableStateOf(false) }
    Column {
        ListItem(
            headlineContent = { Text("Додати демонстраційні звички") },
            supportingContent = { Text("5 звичок з історією за 40 днів") },
            leadingContent = { Icon(Icons.Default.Star, null) },
            modifier = Modifier.clickable(onClick = onDemo),
        )
        HorizontalDivider()
        ListItem(
            headlineContent = { Text("Видалити всі звички", color = Color(0xFFD32F2F)) },
            supportingContent = { Text("Звичок у базі: $habitCount") },
            leadingContent = { Icon(Icons.Default.Delete, null, tint = Color(0xFFD32F2F)) },
            modifier = Modifier.clickable { confirm = true },
        )
        HorizontalDivider()
        ListItem(
            headlineContent = { Text("Трекер звичок 1.0") },
            supportingContent = { Text("Kotlin · Jetpack Compose · SQLite\nМиленко Юрій, група 401") },
            leadingContent = { Icon(Icons.Default.Info, null) },
        )
    }
    if (confirm) {
        AlertDialog(
            onDismissRequest = { confirm = false },
            title = { Text("Видалити всі звички?") },
            text = { Text("Цю дію не можна скасувати.") },
            confirmButton = { TextButton(onClick = { confirm = false; onClear() }) { Text("Видалити") } },
            dismissButton = { TextButton(onClick = { confirm = false }) { Text("Скасувати") } },
        )
    }
}
