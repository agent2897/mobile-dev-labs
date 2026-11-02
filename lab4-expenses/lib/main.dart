import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/date_symbol_data_local.dart';

import 'models/expense.dart';
import 'screens/add_expense_screen.dart';
import 'screens/expenses_screen.dart';
import 'screens/settings_screen.dart';
import 'screens/stats_screen.dart';
import 'state/expense_store.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting('uk');
  final store = ExpenseStore();
  await store.load();
  runApp(StoreScope(store: store, child: const ExpenseApp()));
}

class ExpenseApp extends StatelessWidget {
  const ExpenseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Трекер витрат',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorSchemeSeed: Colors.teal, useMaterial3: true),
      locale: const Locale('uk'),
      supportedLocales: const [Locale('uk')],
      localizationsDelegates: GlobalMaterialLocalizations.delegates,
      home: const HomeShell(),
    );
  }
}

/// Головний екран з нижньою навігацією між трьома вкладками
class HomeShell extends StatefulWidget {
  const HomeShell({super.key});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  int _tab = 0;

  static const _titles = ['Мої витрати', 'Статистика', 'Налаштування'];
  static const _pages = [ExpensesScreen(), StatsScreen(), SettingsScreen()];

  Future<void> _addExpense() async {
    final store = StoreScope.of(context);
    final result = await Navigator.push<Expense>(
      context,
      MaterialPageRoute(builder: (_) => const AddExpenseScreen()),
    );
    if (result != null) store.add(result);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(_titles[_tab])),
      body: IndexedStack(index: _tab, children: _pages),
      floatingActionButton: _tab == 0
          ? FloatingActionButton(onPressed: _addExpense, child: const Icon(Icons.add))
          : null,
      bottomNavigationBar: NavigationBar(
        selectedIndex: _tab,
        onDestinationSelected: (i) => setState(() => _tab = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.receipt_long), label: 'Витрати'),
          NavigationDestination(icon: Icon(Icons.bar_chart), label: 'Статистика'),
          NavigationDestination(icon: Icon(Icons.settings), label: 'Налаштування'),
        ],
      ),
    );
  }
}
