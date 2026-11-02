import sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak, Image, Table

proj, out, shots = sys.argv[1], sys.argv[2], sys.argv[3]
F = 'C:/Windows/Fonts/'
pdfmetrics.registerFont(TTFont('TNR', F + 'times.ttf'))
pdfmetrics.registerFont(TTFont('TNRB', F + 'timesbd.ttf'))
pdfmetrics.registerFont(TTFont('Mono', F + 'consola.ttf'))

n = ParagraphStyle('n', fontName='TNR', fontSize=14, leading=20, alignment=TA_JUSTIFY, firstLineIndent=1.25*cm)
c = ParagraphStyle('c', parent=n, alignment=TA_CENTER, firstLineIndent=0)
h = ParagraphStyle('h', parent=c, fontName='TNRB', spaceBefore=10, spaceAfter=6)
r = ParagraphStyle('r', parent=n, alignment=TA_RIGHT, firstLineIndent=0)
li = ParagraphStyle('li', parent=n, firstLineIndent=0, leftIndent=1.25*cm)
code = ParagraphStyle('code', fontName='Mono', fontSize=8.5, leading=10.5)

def src(p):
    with open(os.path.join(proj, p), encoding='utf-8') as f:
        return f.read()

s = []
s += [Paragraph('МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ', c), Spacer(1, 5*cm),
      Paragraph('<b>ЗВІТ</b>', c), Paragraph('з лабораторної роботи №4', c),
      Paragraph('з дисципліни «Розробка програмних додатків для мобільних пристроїв»', c),
      Paragraph('на тему: «Саморобний додаток на Flutter. Трекер витрат»', c), Spacer(1, 4*cm),
      Paragraph('Виконав: студент групи 401', r), Paragraph('Миленко Юрій', r),
      Spacer(1, 5*cm), Paragraph('2026', c), PageBreak()]

s += [Paragraph('Мета роботи', h),
      Paragraph('Ознайомитися з програмним каркасом Flutter та мовою Dart; навчитися будувати інтерфейс '
                'з віджетів Material 3, керувати станом додатка, організовувати навігацію між екранами, '
                'працювати з формами та локальним сховищем даних; реалізувати власний додаток з нуля.', n),
      Paragraph('Завдання', h),
      Paragraph('Реалізувати власний мобільний додаток з використанням Flutter з нуля. Обрано тему — '
                'трекер особистих витрат. Вимоги та функціональність:', n)]
for t in ['проєкт створено на Flutter (Dart) з нуля;',
          'масштаб не менший, ніж у попередніх проєктах;',
          'додавання витрат через форму з валідацією, вибір категорії та дати;',
          'список витрат, згрупований за днями, з видаленням свайпом і скасуванням;',
          'місячний бюджет та статистика за категоріями з діаграмою;',
          'збереження даних між запусками додатка.']:
    s.append(Paragraph('• ' + t, li))

s += [Paragraph('Хід виконання роботи', h),
      Paragraph('1. Встановлено Flutter SDK, проєкт створено командою '
                '<font name="Mono">flutter create</font>. Додано пакети shared_preferences (локальне '
                'сховище «ключ–значення»), intl (форматування дат і грошових сум українською) та '
                'flutter_localizations (локалізація стандартних віджетів, зокрема календаря). Запуск — '
                '<font name="Mono">flutter run</font> на емуляторі або телефоні.', n),
      Paragraph('2. Структура проєкту (каталог lib): main.dart — точка входу, тема Material 3 та головний '
                'екран з нижньою навігацією; models/expense.dart — модель Expense та перелік Category '
                '(enum з назвою, іконкою і кольором); state/expense_store.dart — стан додатка; screens/ — '
                'екрани «Витрати», «Нова витрата», «Статистика», «Налаштування»; widgets/ — віджети '
                'ExpenseTile, BudgetCard та CategoryBarChart.', n),
      Paragraph('3. Керування станом: клас ExpenseStore наслідує ChangeNotifier і містить список витрат '
                'та бюджет, методи add, remove, setBudget, clear та обчислювані властивості monthTotal '
                'і byCategory. Після кожної зміни викликається notifyListeners() і дані серіалізуються в JSON '
                'та зберігаються в SharedPreferences, а під час запуску — завантажуються. Сховище передається '
                'по дереву віджетів через InheritedNotifier (StoreScope), тому всі вкладки автоматично '
                'перебудовуються при зміні даних.', n),
      Paragraph('4. Навігація: HomeShell містить NavigationBar з трьома вкладками, сторінки зберігаються '
                'в IndexedStack. Кнопка «+» відкриває екран нової витрати через Navigator.push, а введена '
                'витрата повертається як результат Navigator.pop. Форма використовує Form і TextFormField '
                'з валідаторами (порожня назва, недодатна сума), ChoiceChip для вибору категорії та '
                'showDatePicker для вибору дати.', n),
      Paragraph('5. Список витрат групується за днями; кожен елемент обгорнуто в Dismissible — свайп '
                'вліво видаляє витрату, а SnackBar дає змогу скасувати видалення. Картка BudgetCard показує '
                'суму за місяць і залишок бюджету з індикатором прогресу. На вкладці «Статистика» '
                'стовпчикову діаграму намальовано власноруч через CustomPainter, нижче — частка кожної '
                'категорії. Бюджет змінюється в діалозі AlertDialog. Логіку моделі та сховища покрито '
                'модульними тестами (flutter test).', n),
      PageBreak(), Paragraph('Результати роботи', h)]
caps = [('1_empty.png', 'Рис. 1 — Перший запуск, витрат немає'),
        ('2_list.png', 'Рис. 2 — Список витрат і бюджет'),
        ('3_validation.png', 'Рис. 3 — Валідація форми'),
        ('4_add.png', 'Рис. 4 — Додавання нової витрати'),
        ('5_list_added.png', 'Рис. 5 — Витрату додано до списку'),
        ('6_stats.png', 'Рис. 6 — Статистика за категоріями'),
        ('7_budget.png', 'Рис. 7 — Зміна місячного бюджету')]
cap = ParagraphStyle('cap', parent=c, fontSize=11, leading=13)
cells = [[Image(os.path.join(shots, f), width=5*cm, height=9.74*cm), Paragraph(t, cap)] for f, t in caps]
rows = [cells[i:i+3] for i in range(0, len(cells), 3)]
rows[-1] += [''] * (3 - len(rows[-1]))
s.append(Table(rows, colWidths=[5.6*cm]*3, style=[('VALIGN', (0, 0), (-1, -1), 'TOP')]))
GH = 'https://github.com/agent2897/mobile-dev-labs/tree/main/lab4-expenses'
s += [PageBreak(), Paragraph('Код програми', h),
      Paragraph(f'Код програми розміщено на GitHub: <link href="{GH}" color="blue"><u>{GH}</u></link>', n),
      Spacer(1, 6)]
for p in ['lib/main.dart', 'lib/models/expense.dart', 'lib/state/expense_store.dart',
          'lib/screens/expenses_screen.dart', 'lib/screens/add_expense_screen.dart',
          'lib/screens/stats_screen.dart', 'lib/screens/settings_screen.dart',
          'lib/widgets/expense_tile.dart', 'lib/widgets/budget_card.dart', 'lib/widgets/bar_chart.dart',
          'test/widget_test.dart']:
    s += [Paragraph('<b>' + p + '</b>', ParagraphStyle('f', parent=n, firstLineIndent=0, fontSize=12)),
          Preformatted(src(p), code), Spacer(1, 8)]

s += [Paragraph('Висновки', h),
      Paragraph('У ході лабораторної роботи з нуля розроблено мобільний додаток «Трекер витрат» з '
                'використанням програмного каркаса Flutter і мови Dart. Реалізовано додавання витрат через '
                'форму з валідацією, список з групуванням за днями та видаленням свайпом, місячний бюджет, '
                'статистику з власноруч намальованою діаграмою та збереження даних між запусками. Отримано '
                'практичні навички побудови інтерфейсу з віджетів Material 3, керування станом через '
                'ChangeNotifier та InheritedNotifier, навігації за допомогою Navigator і NavigationBar, '
                'роботи з локальним сховищем, а також порівняно підходи Flutter і React Native.', n)]

SimpleDocTemplate(out, pagesize=A4, leftMargin=2.5*cm, rightMargin=1.5*cm,
                  topMargin=2*cm, bottomMargin=2*cm, title='Лабораторна робота 4').build(s)
