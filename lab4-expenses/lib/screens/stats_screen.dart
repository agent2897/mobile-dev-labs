import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../models/expense.dart';
import '../state/expense_store.dart';
import '../widgets/bar_chart.dart';
import '../widgets/expense_tile.dart';

/// Вкладка «Статистика»: діаграма та розподіл витрат за категоріями
class StatsScreen extends StatelessWidget {
  const StatsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final store = StoreScope.of(context);
    final data = store.byCategory;
    final total = store.monthTotal;
    final sorted = Category.values.where((c) => (data[c] ?? 0) > 0).toList()
      ..sort((a, b) => data[b]!.compareTo(data[a]!));

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text(toBeginningOfSentenceCase(DateFormat('LLLL yyyy', 'uk').format(DateTime.now())),
            style: Theme.of(context).textTheme.titleLarge),
        Text('Усього: ${money.format(total)}'),
        const SizedBox(height: 20),
        CategoryBarChart(data: data),
        const SizedBox(height: 20),
        if (sorted.isEmpty) const Center(child: Text('Немає даних за цей місяць')),
        for (final c in sorted)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 6),
            child: Row(children: [
              Icon(c.icon, color: c.color),
              const SizedBox(width: 12),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Row(children: [
                    Expanded(child: Text(c.label)),
                    Text('${money.format(data[c])} · ${(data[c]! / total * 100).round()}%'),
                  ]),
                  const SizedBox(height: 4),
                  LinearProgressIndicator(value: data[c]! / total, color: c.color, minHeight: 6),
                ]),
              ),
            ]),
          ),
      ],
    );
  }
}
