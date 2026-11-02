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
      Paragraph('<b>ЗВІТ</b>', c), Paragraph('з лабораторної роботи №3', c),
      Paragraph('з дисципліни «Розробка програмних додатків для мобільних пристроїв»', c),
      Paragraph('на тему: «Саморобний додаток. Застосунок прогнозу погоди»', c), Spacer(1, 4*cm),
      Paragraph('Виконав: студент групи 401', r), Paragraph('Миленко Юрій', r),
      Spacer(1, 5*cm), Paragraph('2026', c), PageBreak()]

s += [Paragraph('Мета роботи', h),
      Paragraph('Реалізувати проєкт на JavaScript та React Native з нуля; побудувати робочий процес '
                'розробки мобільного додатка; створити власні інтерфейси; навчитися керувати глобальним '
                'станом додатка за допомогою Redux та поєднувати стековий навігатор із навігатором по вкладках.', n),
      Paragraph('Завдання', h),
      Paragraph('Розробити власний мобільний додаток. Обрано тему — застосунок прогнозу погоди з пошуком '
                'міст, обраними містами та налаштуваннями. Вимоги:', n)]
for t in ['використання Redux для керування станом;',
          'щонайменше один мережевий виклик;',
          'щонайменше один стековий навігатор;',
          'щонайменше один навігатор по вкладках;',
          'масштаб не менший, ніж у попередніх проєктах.']:
    s.append(Paragraph('• ' + t, li))

s += [Paragraph('Хід виконання роботи', h),
      Paragraph('1. Створено Expo-проєкт і встановлено залежності: @reduxjs/toolkit та react-redux '
                '(керування станом), @react-navigation/native, @react-navigation/stack, '
                '@react-navigation/bottom-tabs (навігація), @expo/vector-icons (іконки), prop-types. '
                'Як джерело даних обрано відкритий API Open-Meteo, який не потребує ключа.', n),
      Paragraph('2. Структура проєкту: App.js — Provider зі сховищем Redux, навігатор по вкладках '
                '(«Пошук», «Обране», «Налаштування») та два стекові навігатори; api.js — мережеві виклики; '
                'store/ — сховище та слайси; screens/ — екрани SearchScreen, WeatherScreen, FavoritesScreen, '
                'SettingsScreen; components/CityRow.js — рядок міста; weatherCodes.js — розшифровка кодів '
                'погоди WMO в текст та іконку.', n),
      Paragraph('3. Мережеві виклики (api.js): searchCities(name) звертається до Geocoding API Open-Meteo '
                'та повертає список міст з координатами; getForecast(city, unit) отримує поточну погоду '
                '(температура, відчуття, вологість, вітер, код погоди) і прогноз на 7 днів у вибраних '
                'одиницях температури.', n),
      Paragraph('4. Redux-сховище створено функцією configureStore і складається з чотирьох слайсів: '
                'cities — результати пошуку міст (асинхронний thunk findCities зі станами loading/done/error); '
                'forecast — прогнози, кешовані за id міста (thunk loadForecast, який бере одиниці з '
                'getState().settings); favorites — список обраних міст (дії toggleFavorite, clearFavorites); '
                'settings — одиниці температури (дія setUnit). Компоненти отримують стан через useSelector '
                'і змінюють його через useDispatch.', n),
      Paragraph('5. Навігація: нижній навігатор по вкладках містить три вкладки. Вкладки «Пошук» та '
                '«Обране» є стековими навігаторами: зі списку міст виконується перехід '
                'navigation.navigate(\'Weather\', { city }) на екран прогнозу. На екрані прогнозу через '
                'navigation.setOptions у заголовок додано назву міста та кнопку-зірку для додавання в обране. '
                'Обрані міста одразу з’являються на вкладці «Обране», оскільки стан спільний для всього '
                'додатка. Зміна одиниць у налаштуваннях автоматично перезавантажує прогноз.', n),
      PageBreak(), Paragraph('Результати роботи', h)]
caps = [('1_search.png', 'Рис. 1 — Вкладка «Пошук»'),
        ('2_results.png', 'Рис. 2 — Результати пошуку міста «Київ»'),
        ('3_weather.png', 'Рис. 3 — Поточна погода і прогноз на 7 днів'),
        ('5_favorites.png', 'Рис. 4 — Вкладка «Обране»'),
        ('6_settings.png', 'Рис. 5 — Налаштування: вибрано °F'),
        ('7_weather_f.png', 'Рис. 6 — Прогноз у градусах Фаренгейта')]
cap = ParagraphStyle('cap', parent=c, fontSize=11, leading=13)
cells = [[Image(os.path.join(shots, f), width=5*cm, height=9.74*cm), Paragraph(t, cap)] for f, t in caps]
rows = [cells[i:i+3] for i in range(0, len(cells), 3)]
rows[-1] += [''] * (3 - len(rows[-1]))
s.append(Table(rows, colWidths=[5.6*cm]*3, style=[('VALIGN', (0, 0), (-1, -1), 'TOP')]))
GH = 'https://github.com/agent2897/mobile-dev-labs/tree/main/lab3-weather'
s += [PageBreak(), Paragraph('Код програми', h),
      Paragraph(f'Код програми розміщено на GitHub: <link href="{GH}" color="blue"><u>{GH}</u></link>', n),
      Spacer(1, 6)]
for p in ['App.js', 'api.js', 'store/index.js', 'store/citiesSlice.js', 'store/forecastSlice.js',
          'store/favoritesSlice.js', 'store/settingsSlice.js', 'screens/SearchScreen.js',
          'screens/WeatherScreen.js', 'screens/FavoritesScreen.js', 'screens/SettingsScreen.js',
          'components/CityRow.js', 'weatherCodes.js', 'package.json']:
    s += [Paragraph('<b>' + p + '</b>', ParagraphStyle('f', parent=n, firstLineIndent=0, fontSize=12)),
          Preformatted(src(p), code), Spacer(1, 8)]

s += [Paragraph('Висновки', h),
      Paragraph('У ході лабораторної роботи з нуля розроблено власний мобільний додаток прогнозу погоди '
                'на React Native з використанням Expo. Глобальний стан (результати пошуку, прогнози, обрані '
                'міста, налаштування) зберігається в Redux; асинхронні мережеві запити до API Open-Meteo '
                'виконуються через createAsyncThunk. Навігацію побудовано на поєднанні навігатора по вкладках '
                'та стекових навігаторів. Отримано практичні навички проєктування архітектури додатка, роботи '
                'з Redux Toolkit, react-redux, React Navigation та мережевими API.', n)]

SimpleDocTemplate(out, pagesize=A4, leftMargin=2.5*cm, rightMargin=1.5*cm,
                  topMargin=2*cm, bottomMargin=2*cm, title='Лабораторна робота 3').build(s)
