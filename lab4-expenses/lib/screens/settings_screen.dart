import 'package:flutter/material.dart';

import '../state/expense_store.dart';
import '../widgets/expense_tile.dart';

/// Вкладка «Налаштування»: місячний бюджет і керування даними
class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  Future<void> _editBudget(BuildContext context, ExpenseStore store) async {
    final ctrl = TextEditingController(text: store.budget.toStringAsFixed(0));
    final value = await showDialog<double>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Місячний бюджет'),
        content: TextField(
          controller: ctrl,
          keyboardType: TextInputType.number,
          autofocus: true,
          decoration: const InputDecoration(suffixText: '₴'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Скасувати')),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, double.tryParse(ctrl.text)),
            child: const Text('Зберегти'),
          ),
        ],
      ),
    );
    if (value != null && value > 0) store.setBudget(value);
  }

  Future<void> _confirmClear(BuildContext context, ExpenseStore store) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Видалити всі витрати?'),
        content: const Text('Цю дію не можна скасувати.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Ні')),
          FilledButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Видалити')),
        ],
      ),
    );
    if (ok == true) store.clear();
  }

  @override
  Widget build(BuildContext context) {
    final store = StoreScope.of(context);
    return ListView(
      children: [
        ListTile(
          leading: const Icon(Icons.account_balance_wallet),
          title: const Text('Місячний бюджет'),
          subtitle: Text(money.format(store.budget)),
          trailing: const Icon(Icons.edit),
          onTap: () => _editBudget(context, store),
        ),
        const Divider(),
        ListTile(
          leading: const Icon(Icons.auto_awesome),
          title: const Text('Додати демонстраційні дані'),
          onTap: store.addDemoData,
        ),
        ListTile(
          leading: const Icon(Icons.delete_forever, color: Colors.red),
          title: const Text('Видалити всі витрати', style: TextStyle(color: Colors.red)),
          subtitle: Text('Записів: ${store.expenses.length}'),
          onTap: () => _confirmClear(context, store),
        ),
        const Divider(),
        const AboutListTile(
          icon: Icon(Icons.info_outline),
          applicationName: 'Трекер витрат',
          applicationVersion: '1.0.0',
          applicationLegalese: 'Миленко Юрій, група 401',
        ),
      ],
    );
  }
}
