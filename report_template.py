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
      Paragraph('<b>ЗВІТ</b>', c), Paragraph('з лабораторної роботи №5', c),
      Paragraph('з дисципліни «Розробка програмних додатків для мобільних пристроїв»', c),
      Paragraph('на тему: «Нативний додаток на Kotlin. Трекер звичок»', c), Spacer(1, 4*cm),
      Paragraph('Виконав: студент групи 401', r), Paragraph('Миленко Юрій', r),
      Spacer(1, 5*cm), Paragraph('2026', c), PageBreak()]

s += [Paragraph('Мета роботи', h),
      Paragraph('Опанувати нативну розробку під Android мовою Kotlin; навчитися будувати інтерфейс '
                'за допомогою Jetpack Compose, працювати з базою даних SQLite, застосовувати архітектуру '
                'з ViewModel та StateFlow, організовувати навігацію; реалізувати власний додаток з нуля.', n),
      Paragraph('Завдання', h),
      Paragraph('Реалізувати власний мобільний додаток засобами нативної розробки на Kotlin з нуля. '
                'Обрано тему — трекер щоденних звичок. Вимоги та функціональність:', n)]
for t in ['проєкт створено нативно на Kotlin (Android SDK, Jetpack Compose) з нуля;',
          'масштаб не менший, ніж у попередніх проєктах;',
          'створення звичок з назвою, іконкою та кольором, валідація форми;',
          'щоденні відмітки виконання та підрахунок серій (поточна, найкраща);',
          'календар історії з можливістю змінювати відмітки за минулі дні;',
          'статистика з діаграмою за 7 днів і відсотком виконання за 30 днів;',
          'зберігання даних у локальній базі SQLite.']:
    s.append(Paragraph('• ' + t, li))

s += [Paragraph('Хід виконання роботи', h),
      Paragraph('1. Встановлено Android SDK (платформа API 35, build-tools, емулятор) та JDK 21. Проєкт '
                'створено вручну зі збиранням через Gradle (Kotlin DSL): Android Gradle Plugin 8.7, Kotlin 2.0, '
                'Jetpack Compose (Material 3), navigation-compose, lifecycle-viewmodel-compose. Збирання — '
                '<font name="Mono">gradlew assembleDebug</font>, перевірка — на емуляторі Pixel 6 (Android 15).', n),
      Paragraph('2. Структура проєкту (пакет com.mylenko.habits): MainActivity — точка входу; data/Habit.kt — '
                'модель звички з методами підрахунку серій і відсотка виконання; data/HabitDatabase.kt — робота '
                'з SQLite; ui/HabitViewModel.kt — ViewModel; ui/AppNavigation.kt — граф навігації; '
                'ui/screens/ — екрани «Сьогодні», «Нова звичка», «Деталі», «Статистика», «Налаштування»; '
                'ui/theme/ — тема Material 3.', n),
      Paragraph('3. Зберігання даних: клас HabitDatabase наслідує SQLiteOpenHelper і створює дві таблиці — '
                'habits (назва, емодзі, колір, дата створення) та completions (звичка + дата виконання) '
                'з зовнішнім ключем ON DELETE CASCADE. Реалізовано методи getAll, insert, delete, setDone '
                'та clear з параметризованими запитами.', n),
      Paragraph('4. Архітектура: HabitViewModel (AndroidViewModel) виконує операції з базою у фоновому '
                'потоці через корутини (viewModelScope, Dispatchers.IO) і публікує актуальний список звичок '
                'у StateFlow. Екрани підписуються на нього через collectAsStateWithLifecycle, тому інтерфейс '
                'оновлюється автоматично після будь-якої зміни.', n),
      Paragraph('5. Інтерфейс і навігація: NavHost з навігацією Compose містить три вкладки нижньої панелі '
                'NavigationBar та екрани «Нова звичка» і «Деталі» (маршрут habit/{id}). На екрані деталей '
                'намальовано календар місяця (натискання на день змінює відмітку), картки поточної та '
                'найкращої серії; видалення підтверджується діалогом AlertDialog. На вкладці «Статистика» '
                'діаграму за 7 днів намальовано на Canvas. Логіку підрахунку серій покрито юніт-тестами JUnit.', n),
      PageBreak(), Paragraph('Результати роботи', h)]
caps = [('1_empty.png', 'Рис. 1 — Перший запуск'),
        ('2_today.png', 'Рис. 2 — Звички на сьогодні з відмітками'),
        ('3_validation.png', 'Рис. 3 — Валідація форми нової звички'),
        ('4_add.png', 'Рис. 4 — Вибір назви, іконки та кольору'),
        ('5_added.png', 'Рис. 5 — Нову звичку додано'),
        ('6_detail.png', 'Рис. 6 — Деталі звички: серії та календар'),
        ('7_stats.png', 'Рис. 7 — Статистика за 7 і 30 днів')]
cap = ParagraphStyle('cap', parent=c, fontSize=11, leading=13)
cells = [[Image(os.path.join(shots, f), width=5*cm, height=11.11*cm), Paragraph(t, cap)] for f, t in caps]
rows = [cells[i:i+3] for i in range(0, len(cells), 3)]
rows[-1] += [''] * (3 - len(rows[-1]))
s.append(Table(rows, colWidths=[5.6*cm]*3, style=[('VALIGN', (0, 0), (-1, -1), 'TOP')]))
GH = 'https://github.com/agent2897/mobile-dev-labs/tree/main/lab5-habits'
s += [PageBreak(), Paragraph('Код програми', h),
      Paragraph(f'Код програми розміщено на GitHub: <link href="{GH}" color="blue"><u>{GH}</u></link>', n),
      Spacer(1, 6)]
K = 'app/src/main/java/com/mylenko/habits/'
for p in [K + 'MainActivity.kt', K + 'data/Habit.kt', K + 'data/HabitDatabase.kt',
          K + 'ui/HabitViewModel.kt', K + 'ui/AppNavigation.kt', K + 'ui/screens/TodayScreen.kt',
          K + 'ui/screens/AddHabitScreen.kt', K + 'ui/screens/HabitDetailScreen.kt',
          K + 'ui/screens/StatsScreen.kt', K + 'ui/screens/SettingsScreen.kt', K + 'ui/theme/Theme.kt',
          'app/src/test/java/com/mylenko/habits/HabitTest.kt', 'app/build.gradle.kts',
          'app/src/main/AndroidManifest.xml']:
    s += [Paragraph('<b>' + p + '</b>', ParagraphStyle('f', parent=n, firstLineIndent=0, fontSize=12)),
          Preformatted(src(p), code), Spacer(1, 8)]

s += [Paragraph('Висновки', h),
      Paragraph('У ході лабораторної роботи з нуля розроблено нативний Android-додаток «Трекер звичок» '
                'мовою Kotlin. Реалізовано створення звичок, щоденні відмітки, підрахунок поточної та '
                'найкращої серії, календар історії, статистику з діаграмою та зберігання даних у SQLite. '
                'Додаток зібрано через Gradle і перевірено на емуляторі Android 15. Отримано практичні навички '
                'роботи з Android SDK, Jetpack Compose, SQLiteOpenHelper, ViewModel, корутинами та StateFlow, '
                'навігацією Compose, а також порівняно нативну розробку з кросплатформними підходами '
                '(React Native, Flutter).', n)]

SimpleDocTemplate(out, pagesize=A4, leftMargin=2.5*cm, rightMargin=1.5*cm,
                  topMargin=2*cm, bottomMargin=2*cm, title='Лабораторна робота 5').build(s)
