import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../models/expense.dart';

/// Екран додавання витрати; повертає Expense через Navigator.pop
class AddExpenseScreen extends StatefulWidget {
  const AddExpenseScreen({super.key});

  @override
  State<AddExpenseScreen> createState() => _AddExpenseScreenState();
}

class _AddExpenseScreenState extends State<AddExpenseScreen> {
  final _formKey = GlobalKey<FormState>();
  final _title = TextEditingController();
  final _amount = TextEditingController();
  Category _category = Category.food;
  DateTime _date = DateTime.now();

  @override
  void dispose() {
    _title.dispose();
    _amount.dispose();
    super.dispose();
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _date,
      firstDate: DateTime(2020),
      lastDate: DateTime.now(),
    );
    if (picked != null) setState(() => _date = picked);
  }

  void _submit() {
    if (!_formKey.currentState!.validate()) return;
    Navigator.pop(
      context,
      Expense(
        id: DateTime.now().microsecondsSinceEpoch.toString(),
        title: _title.text.trim(),
        amount: double.parse(_amount.text.replaceAll(',', '.')),
        date: _date,
        category: _category,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Нова витрата')),
      body: Form(
        key: _formKey,
        autovalidateMode: AutovalidateMode.onUserInteraction,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            TextFormField(
              controller: _title,
              decoration: const InputDecoration(labelText: 'Назва', prefixIcon: Icon(Icons.edit)),
              validator: (v) => (v == null || v.trim().isEmpty) ? 'Введіть назву' : null,
            ),
            const SizedBox(height: 12),
            TextFormField(
              controller: _amount,
              keyboardType: const TextInputType.numberWithOptions(decimal: true),
              decoration: const InputDecoration(labelText: 'Сума, ₴', prefixIcon: Icon(Icons.payments)),
              validator: (v) {
                final n = double.tryParse((v ?? '').replaceAll(',', '.'));
                return (n == null || n <= 0) ? 'Введіть додатну суму' : null;
              },
            ),
            const SizedBox(height: 20),
            Text('Категорія', style: Theme.of(context).textTheme.titleSmall),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final c in Category.values)
                  ChoiceChip(
                    avatar: Icon(c.icon, size: 18, color: c.color),
                    label: Text(c.label),
                    selected: _category == c,
                    onSelected: (_) => setState(() => _category = c),
                  ),
              ],
            ),
            const SizedBox(height: 20),
            ListTile(
              contentPadding: EdgeInsets.zero,
              leading: const Icon(Icons.calendar_today),
              title: Text(DateFormat('d MMMM yyyy', 'uk').format(_date)),
              trailing: TextButton(onPressed: _pickDate, child: const Text('Змінити')),
            ),
            const SizedBox(height: 20),
            FilledButton.icon(
              onPressed: _submit,
              icon: const Icon(Icons.check),
              label: const Text('Зберегти'),
              style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50)),
            ),
          ],
        ),
      ),
    );
  }
}
