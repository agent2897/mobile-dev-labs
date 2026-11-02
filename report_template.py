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
      Paragraph('<b>ЗВІТ</b>', c), Paragraph('з лабораторної роботи №2', c),
      Paragraph('з дисципліни «Розробка програмних додатків для мобільних пристроїв»', c),
      Paragraph('на тему: «Браузер фільмів»', c), Spacer(1, 4*cm),
      Paragraph('Виконав: студент групи 401', r), Paragraph('Миленко Юрій', r),
      Spacer(1, 5*cm), Paragraph('2026', c), PageBreak()]

s += [Paragraph('Мета роботи', h),
      Paragraph('Навчитися організовувати навігацію між екранами мобільного додатка за допомогою '
                'React Navigation (StackNavigator), отримувати дані з мережевого API, відображати великі '
                'списки за допомогою FlatList з посторінковим довантаженням; розробити додаток для пошуку '
                'фільмів у відкритій базі даних OMDb.', n),
      Paragraph('Завдання', h),
      Paragraph('Створити браузер фільмів, який дозволяє шукати фільми в базі OMDb (omdbapi.com) і '
                'переглядати додаткову інформацію про вибраний фільм. Вимоги:', n)]
for t in ['використовувати лише бібліотеки expo, react, react-native, prop-types, react-navigation '
          'та бібліотеку іконок;',
          'наявність щонайменше одного StackNavigator;',
          'екран пошуку, що дозволяє шукати фільми;',
          'показ більше 10 результатів, якщо їх існує більше 10;',
          'екран з додатковою інформацією про вибраний фільм.']:
    s.append(Paragraph('• ' + t, li))

s += [Paragraph('Хід виконання роботи', h),
      Paragraph('1. Створено Expo-проєкт та встановлено залежності: @react-navigation/native, '
                '@react-navigation/stack (з необхідними для неї react-native-gesture-handler, '
                'react-native-screens, react-native-safe-area-context), prop-types та @expo/vector-icons '
                '(бібліотека іконок Ionicons).', n),
      Paragraph('2. Структура проєкту: App.js — контейнер навігації та StackNavigator з двома екранами '
                '(Search і Details); screens/SearchScreen.js — екран пошуку; screens/DetailsScreen.js — '
                'екран детальної інформації; components/MovieRow.js — рядок списку результатів; '
                'api.js — функції роботи з OMDb API; mockData.js — макетні дані.', n),
      Paragraph('3. Модуль api.js містить функції searchMovies(query, page) та getMovie(id). Перша '
                'звертається до OMDb з параметрами s (рядок пошуку) і page та повертає список результатів '
                'і їх загальну кількість; друга отримує повну інформацію про фільм за параметром i (imdbID). '
                'Якщо API-ключ не задано, функції працюють із макетними даними з mockData.js у тому ж '
                'форматі, що й відповіді OMDb.', n),
      Paragraph('4. На екрані пошуку пошук виконується автоматично під час введення (від 3 символів). '
                'Результати виводяться у FlatList. OMDb повертає по 10 результатів на сторінку, тому '
                'для показу понад 10 результатів використано подію onEndReached: при прокрутці до кінця '
                'списку завантажується наступна сторінка і додається до вже показаних. Під час '
                'завантаження відображається ActivityIndicator, а якщо нічого не знайдено — відповідне '
                'повідомлення.', n),
      Paragraph('5. Натискання на фільм викликає navigation.navigate(\'Details\', { id, title }). Екран '
                'деталей отримує imdbID з route.params, завантажує дані в useEffect і показує постер, '
                'рік, рейтинг IMDb, тривалість, жанр, режисера, акторів та опис. Назва фільму '
                'відображається в заголовку, а кнопка «назад» StackNavigator повертає до результатів пошуку. '
                'Для всіх компонентів задано PropTypes.', n),
      PageBreak(), Paragraph('Результати роботи', h)]
caps = [('1_search.png', 'Рис. 1 — Екран пошуку'),
        ('2_results.png', 'Рис. 2 — Результати пошуку «star» (перші 10)'),
        ('3_more.png', 'Рис. 3 — Довантажено понад 10 результатів (13)'),
        ('4_details.png', 'Рис. 4 — Екран детальної інформації про фільм'),
        ('5_empty.png', 'Рис. 5 — Пошук без результатів')]
cap = ParagraphStyle('cap', parent=c, fontSize=11, leading=13)
cells = [[Image(os.path.join(shots, f), width=5*cm, height=9.74*cm), Paragraph(t, cap)] for f, t in caps]
rows = [cells[i:i+3] for i in range(0, len(cells), 3)]
rows[-1] += [''] * (3 - len(rows[-1]))
s.append(Table(rows, colWidths=[5.6*cm]*3, style=[('VALIGN', (0, 0), (-1, -1), 'TOP')]))
s += [PageBreak(), Paragraph('Код програми', h)]
for p in ['App.js', 'screens/SearchScreen.js', 'screens/DetailsScreen.js', 'components/MovieRow.js',
          'api.js', 'mockData.js', 'package.json']:
    s += [Paragraph('<b>' + p + '</b>', ParagraphStyle('f', parent=n, firstLineIndent=0, fontSize=12)),
          Preformatted(src(p), code), Spacer(1, 8)]

s += [Paragraph('Висновки', h),
      Paragraph('У ході лабораторної роботи було розроблено мобільний додаток «Браузер фільмів» на '
                'React Native з використанням Expo. Реалізовано навігацію між екранами за допомогою '
                'StackNavigator з бібліотеки React Navigation, екран пошуку фільмів з посторінковим '
                'довантаженням результатів (показ понад 10 результатів) та екран з детальною інформацією '
                'про фільм. Отримано практичні навички роботи з мережевими запитами (fetch, async/await), '
                'компонентом FlatList, передачею параметрів між екранами, бібліотекою іконок та PropTypes.', n)]

SimpleDocTemplate(out, pagesize=A4, leftMargin=2.5*cm, rightMargin=1.5*cm,
                  topMargin=2*cm, bottomMargin=2*cm, title='Лабораторна робота 2').build(s)
