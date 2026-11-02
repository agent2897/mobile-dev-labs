import 'dart:convert';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/expense.dart';

/// Стан додатка: список витрат і бюджет, зберігаються в SharedPreferences
class ExpenseStore extends ChangeNotifier {
  static const _expensesKey = 'expenses';
  static const _budgetKey = 'budget';

  final List<Expense> _expenses = [];
  double _budget = 10000;

  List<Expense> get expenses => List.unmodifiable(_expenses);
  double get budget => _budget;

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_expensesKey);
    if (raw != null) {
      final list = jsonDecode(raw) as List;
      _expenses
        ..clear()
        ..addAll(list.map((e) => Expense.fromJson(e as Map<String, dynamic>)));
    }
    _budget = prefs.getDouble(_budgetKey) ?? _budget;
    _sort();
    notifyListeners();
  }

  Future<void> _save() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_expensesKey, jsonEncode(_expenses.map((e) => e.toJson()).toList()));
    await prefs.setDouble(_budgetKey, _budget);
  }

  void _sort() => _expenses.sort((a, b) => b.date.compareTo(a.date));

  void add(Expense e) {
    _expenses.add(e);
    _sort();
    _changed();
  }

  void remove(Expense e) {
    _expenses.removeWhere((x) => x.id == e.id);
    _changed();
  }

  void setBudget(double value) {
    _budget = value;
    _changed();
  }

  void clear() {
    _expenses.clear();
    _changed();
  }

  void _changed() {
    notifyListeners();
    _save();
  }

  /// Витрати поточного місяця
  List<Expense> get thisMonth {
    final now = DateTime.now();
    return _expenses.where((e) => e.date.year == now.year && e.date.month == now.month).toList();
  }

  double get monthTotal => thisMonth.fold(0, (sum, e) => sum + e.amount);

  /// Суми за категоріями за поточний місяць
  Map<Category, double> get byCategory {
    final map = <Category, double>{};
    for (final e in thisMonth) {
      map[e.category] = (map[e.category] ?? 0) + e.amount;
    }
    return map;
  }

  /// Демонстраційні дані для перевірки роботи додатка
  void addDemoData() {
    final rnd = Random(4);
    final now = DateTime.now();
    const samples = [
      ('Продукти АТБ', Category.food, 640.0),
      ('Кава', Category.food, 75.0),
      ('Метро', Category.transport, 32.0),
      ('Таксі Uklon', Category.transport, 185.0),
      ('Комунальні послуги', Category.home, 2350.0),
      ('Кіно', Category.fun, 260.0),
      ('Steam', Category.fun, 499.0),
      ('Аптека', Category.health, 318.0),
      ('Обід у кафе', Category.food, 290.0),
      ('Інтернет', Category.home, 250.0),
      ('Подарунок', Category.other, 700.0),
    ];
    for (var i = 0; i < samples.length; i++) {
      final (title, cat, amount) = samples[i];
      _expenses.add(Expense(
        id: '${now.microsecondsSinceEpoch}_$i',
        title: title,
        amount: amount,
        date: now.subtract(Duration(days: rnd.nextInt(now.day), hours: i)),
        category: cat,
      ));
    }
    _sort();
    _changed();
  }
}

/// Передає ExpenseStore вниз по дереву віджетів і перебудовує залежні віджети
class StoreScope extends InheritedNotifier<ExpenseStore> {
  const StoreScope({super.key, required ExpenseStore store, required super.child})
      : super(notifier: store);

  static ExpenseStore of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<StoreScope>()!.notifier!;
}
