package com.mylenko.habits.ui

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.mylenko.habits.ui.screens.*

private data class Tab(val route: String, val title: String, val icon: ImageVector)

private val TABS = listOf(
    Tab("today", "Сьогодні", Icons.Default.Home),
    Tab("stats", "Статистика", Icons.Default.DateRange),
    Tab("settings", "Налаштування", Icons.Default.Settings),
)

/** Граф навігації: три вкладки нижньої панелі + екрани «Нова звичка» і «Деталі» */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppNavigation(vm: HabitViewModel = viewModel()) {
    val nav = rememberNavController()
    val habits by vm.habits.collectAsStateWithLifecycle()
    val route = nav.currentBackStackEntryAsState().value?.destination?.route
    val tab = TABS.find { it.route == route }

    Scaffold(
        topBar = { if (tab != null) TopAppBar(title = { Text(if (tab.route == "today") "Мої звички" else tab.title) }) },
        bottomBar = { if (tab != null) BottomBar(nav, route) },
        floatingActionButton = {
            if (route == "today") {
                FloatingActionButton(onClick = { nav.navigate("add") }) { Icon(Icons.Default.Add, "Додати звичку") }
            }
        },
    ) { padding ->
        NavHost(nav, startDestination = "today", modifier = Modifier.padding(if (tab != null) padding else androidx.compose.foundation.layout.PaddingValues())) {
            composable("today") {
                TodayScreen(habits, onToggle = vm::toggle, onOpen = { nav.navigate("habit/${it.id}") })
            }
            composable("stats") { StatsScreen(habits) }
            composable("settings") {
                SettingsScreen(habits.size, onDemo = vm::addDemoData, onClear = vm::clearAll)
            }
            composable("add") {
                AddHabitScreen(
                    onSave = { name, emoji, color -> vm.add(name, emoji, color); nav.popBackStack() },
                    onBack = { nav.popBackStack() },
                )
            }
            composable("habit/{id}") { entry ->
                val id = entry.arguments?.getString("id")?.toLongOrNull()
                val habit = habits.find { it.id == id }
                if (habit != null) {
                    HabitDetailScreen(
                        habit = habit,
                        onToggleDate = { vm.toggle(habit, it) },
                        onDelete = { vm.delete(habit.id); nav.popBackStack() },
                        onBack = { nav.popBackStack() },
                    )
                }
            }
        }
    }
}

@Composable
private fun BottomBar(nav: NavHostController, current: String?) {
    NavigationBar {
        TABS.forEach { t ->
            NavigationBarItem(
                selected = current == t.route,
                onClick = {
                    nav.navigate(t.route) {
                        popUpTo("today") { saveState = true }
                        launchSingleTop = true
                        restoreState = true
                    }
                },
                icon = { Icon(t.icon, contentDescription = null) },
                label = { Text(t.title) },
            )
        }
    }
}
