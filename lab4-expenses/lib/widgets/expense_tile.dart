import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../models/expense.dart';

final money = NumberFormat.currency(locale: 'uk', symbol: '₴', decimalDigits: 0);

class ExpenseTile extends StatelessWidget {
  const ExpenseTile({super.key, required this.expense});

  final Expense expense;

  @override
  Widget build(BuildContext context) {
    final cat = expense.category;
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: cat.color.withValues(alpha: 0.15),
          child: Icon(cat.icon, color: cat.color),
        ),
        title: Text(expense.title, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text('${cat.label} · ${DateFormat('HH:mm').format(expense.date)}'),
        trailing: Text(
          '-${money.format(expense.amount)}',
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
    );
  }
}
