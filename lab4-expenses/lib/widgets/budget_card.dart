import 'package:flutter/material.dart';

import 'expense_tile.dart';

/// Картка з витратами за місяць та залишком бюджету
class BudgetCard extends StatelessWidget {
  const BudgetCard({super.key, required this.spent, required this.budget});

  final double spent;
  final double budget;

  @override
  Widget build(BuildContext context) {
    final ratio = budget > 0 ? (spent / budget).clamp(0.0, 1.0) : 0.0;
    final over = spent > budget;
    final scheme = Theme.of(context).colorScheme;
    return Card(
      margin: const EdgeInsets.all(12),
      color: scheme.primaryContainer,
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Витрачено цього місяця', style: TextStyle(color: scheme.onPrimaryContainer)),
            const SizedBox(height: 4),
            Text(money.format(spent),
                style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: scheme.onPrimaryContainer)),
            const SizedBox(height: 12),
            ClipRRect(
              borderRadius: BorderRadius.circular(6),
              child: LinearProgressIndicator(
                value: ratio,
                minHeight: 10,
                color: over ? Colors.red : scheme.primary,
                backgroundColor: scheme.surface,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              over
                  ? 'Перевищено бюджет на ${money.format(spent - budget)}'
                  : 'Залишок: ${money.format(budget - spent)} з ${money.format(budget)}',
              style: TextStyle(color: over ? Colors.red : scheme.onPrimaryContainer),
            ),
          ],
        ),
      ),
    );
  }
}
