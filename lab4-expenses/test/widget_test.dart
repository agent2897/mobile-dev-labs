import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:expense_tracker/models/expense.dart';
import 'package:expense_tracker/state/expense_store.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});

  test('Expense серіалізується в JSON і назад', () {
    final e = Expense(id: '1', title: 'Кава', amount: 75, date: DateTime(2026, 11, 2), category: Category.food);
    final copy = Expense.fromJson(e.toJson());
    expect(copy.title, 'Кава');
    expect(copy.amount, 75);
    expect(copy.category, Category.food);
  });

  test('Сума за місяць і за категоріями', () {
    final store = ExpenseStore();
    final now = DateTime.now();
    store.add(Expense(id: '1', title: 'A', amount: 100, date: now, category: Category.food));
    store.add(Expense(id: '2', title: 'B', amount: 50, date: now, category: Category.transport));
    store.add(Expense(id: '3', title: 'C', amount: 25, date: now, category: Category.food));
    expect(store.monthTotal, 175);
    expect(store.byCategory[Category.food], 125);
  });
}
