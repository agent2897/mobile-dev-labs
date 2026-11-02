import 'package:flutter/material.dart';

/// Категорії витрат з іконкою та кольором
enum Category {
  food('Їжа', Icons.restaurant, Color(0xFFEF6C00)),
  transport('Транспорт', Icons.directions_bus, Color(0xFF1E88E5)),
  home('Житло', Icons.home, Color(0xFF6D4C41)),
  fun('Розваги', Icons.sports_esports, Color(0xFF8E24AA)),
  health('Здоров\'я', Icons.favorite, Color(0xFFE53935)),
  other('Інше', Icons.category, Color(0xFF546E7A));

  const Category(this.label, this.icon, this.color);
  final String label;
  final IconData icon;
  final Color color;
}

class Expense {
  Expense({
    required this.id,
    required this.title,
    required this.amount,
    required this.date,
    required this.category,
  });

  final String id;
  final String title;
  final double amount;
  final DateTime date;
  final Category category;

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'amount': amount,
        'date': date.toIso8601String(),
        'category': category.name,
      };

  factory Expense.fromJson(Map<String, dynamic> json) => Expense(
        id: json['id'] as String,
        title: json['title'] as String,
        amount: (json['amount'] as num).toDouble(),
        date: DateTime.parse(json['date'] as String),
        category: Category.values.byName(json['category'] as String),
      );
}
