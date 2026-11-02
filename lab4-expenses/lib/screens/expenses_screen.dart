import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../models/expense.dart';
import '../state/expense_store.dart';
import '../widgets/budget_card.dart';
import '../widgets/expense_tile.dart';

/// Вкладка «Витрати»: бюджет і список витрат, згрупований за днями
class ExpensesScreen extends StatelessWidget {
  const ExpensesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final store = StoreScope.of(context);
    final items = store.expenses;

    // групування за датою
    final groups = <String, List<Expense>>{};
    for (final e in items) {
      groups.putIfAbsent(DateFormat('d MMMM, EEEE', 'uk').format(e.date), () => []).add(e);
    }

    return ListView(
      padding: const EdgeInsets.only(bottom: 90),
      children: [
        BudgetCard(spent: store.monthTotal, budget: store.budget),
        if (items.isEmpty)
          const Padding(
            padding: EdgeInsets.all(40),
            child: Column(children: [
              Icon(Icons.receipt_long, size: 64, color: Colors.grey),
              SizedBox(height: 12),
              Text('Витрат ще немає.\nНатисніть «+», щоб додати.', textAlign: TextAlign.center),
            ]),
          ),
        for (final entry in groups.entries) ...[
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 12, 20, 4),
            child: Text(entry.key, style: Theme.of(context).textTheme.titleSmall),
          ),
          for (final e in entry.value)
            Dismissible(
              key: ValueKey(e.id),
              direction: DismissDirection.endToStart,
              background: Container(
                alignment: Alignment.centerRight,
                padding: const EdgeInsets.only(right: 24),
                color: Colors.red,
                child: const Icon(Icons.delete, color: Colors.white),
              ),
              onDismissed: (_) {
                store.remove(e);
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                  content: Text('«${e.title}» видалено'),
                  action: SnackBarAction(label: 'Скасувати', onPressed: () => store.add(e)),
                ));
              },
              child: ExpenseTile(expense: e),
            ),
        ],
      ],
    );
  }
}
