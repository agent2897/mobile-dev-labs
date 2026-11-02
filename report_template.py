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
    with open(os.path.join(proj, p), encoding='utf-8-sig') as f:
        return f.read()

s = []
s += [Paragraph('МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ', c), Spacer(1, 5*cm),
      Paragraph('<b>ЗВІТ</b>', c), Paragraph('з лабораторної роботи №6', c),
      Paragraph('з дисципліни «Розробка програмних додатків для мобільних пристроїв»', c),
      Paragraph('на тему: «Додаток на .NET MAUI. Курси валют НБУ»', c), Spacer(1, 4*cm),
      Paragraph('Виконав: студент групи 401', r), Paragraph('Миленко Юрій', r),
      Spacer(1, 5*cm), Paragraph('2026', c), PageBreak()]

s += [Paragraph('Мета роботи', h),
      Paragraph('Ознайомитися з технологією .NET MAUI та мовою C#; навчитися описувати інтерфейс '
                'мовою XAML, застосовувати шаблон MVVM з прив’язками даних і командами, використовувати '
                'впровадження залежностей, навігацію Shell та мережеві запити; реалізувати власний додаток з нуля.', n),
      Paragraph('Завдання', h),
      Paragraph('Реалізувати власний мобільний додаток з використанням технології Xamarin або MAUI з нуля. '
                'Обрано .NET MAUI (сучасний наступник Xamarin.Forms) і тему — курси валют '
                'Національного банку України. Вимоги та функціональність:', n)]
for t in ['проєкт створено на .NET MAUI (C#, XAML) з нуля;',
          'масштаб не менший, ніж у попередніх проєктах;',
          'отримання офіційних курсів з відкритого API НБУ, пошук і оновлення свайпом;',
          'сторінка валюти з графіком курсу за 7, 30 або 90 днів;',
          'конвертер між будь-якими двома валютами;',
          'список обраних валют, що зберігається між запусками.']:
    s.append(Paragraph('• ' + t, li))

s += [Paragraph('Хід виконання роботи', h),
      Paragraph('1. Встановлено .NET 9 SDK та робоче навантаження maui-android. Проєкт створено командою '
                '<font name="Mono">dotnet new maui</font> і налаштовано на платформу Android. Збирання — '
                '<font name="Mono">dotnet build -f net9.0-android</font>, перевірка — на емуляторі Pixel 6 '
                '(Android 15). Сторонні NuGet-пакети не використовувалися.', n),
      Paragraph('2. Структура проєкту за шаблоном MVVM: Models/Rate.cs — модель курсу; Services/NbuService.cs — '
                'мережеві запити; Services/FavoritesService.cs — обрані валюти; ViewModels/ — BaseViewModel, '
                'RatesViewModel, ConverterViewModel, DetailsViewModel; Views/ — сторінки XAML; '
                'Controls/RateChart.cs — власний елемент-графік; AppShell.xaml — навігація; MauiProgram.cs — '
                'реєстрація залежностей.', n),
      Paragraph('3. Мережа: NbuService через HttpClient звертається до API НБУ '
                '(bank.gov.ua/NBUStatService/v1/statdirectory/exchange) за курсами на сьогодні та до '
                'exchange_site за історією курсу за період; відповіді JSON десеріалізуються System.Text.Json. '
                'Курси кешуються, оновлення — жестом «потягнути вниз» (RefreshView). Помилки мережі '
                'перехоплюються в BaseViewModel і показуються користувачу.', n),
      Paragraph('4. MVVM: BaseViewModel реалізує INotifyPropertyChanged; дії користувача прив’язані через '
                'ICommand (Command). Сторінки XAML використовують компільовані прив’язки (x:DataType), '
                'CollectionView, SearchBar, Picker, Entry. Сервіси, ViewModel і сторінки реєструються в '
                'контейнері залежностей у MauiProgram і автоматично передаються в конструктори. Обрані '
                'валюти зберігаються в Preferences.', n),
      Paragraph('5. Навігація Shell: TabBar з вкладками «Курси», «Конвертер», «Обране»; сторінка валюти '
                'зареєстрована як маршрут details і відкривається поверх вкладок через Shell.GoToAsync з '
                'передачею об’єкта (IQueryAttributable). Графік курсу намальовано власноруч через GraphicsView '
                'та IDrawable: сітка, лінія, заливка, підписи значень і дат.', n),
      PageBreak(), Paragraph('Результати роботи', h)]
caps = [('1_rates.png', 'Рис. 1 — Курси НБУ на сьогодні'),
        ('2_search.png', 'Рис. 2 — Пошук валюти'),
        ('3_details_30.png', 'Рис. 3 — Сторінка валюти, графік за 30 днів'),
        ('4_details_90.png', 'Рис. 4 — Графік за 90 днів'),
        ('5_converter.png', 'Рис. 5 — Конвертер USD → UAH'),
        ('6_converter_swap.png', 'Рис. 6 — Обмін валют місцями'),
        ('7_favorites.png', 'Рис. 7 — Обрані валюти')]
cap = ParagraphStyle('cap', parent=c, fontSize=11, leading=13)
cells = [[Image(os.path.join(shots, f), width=5*cm, height=11.11*cm), Paragraph(t, cap)] for f, t in caps]
rows = [cells[i:i+3] for i in range(0, len(cells), 3)]
rows[-1] += [''] * (3 - len(rows[-1]))
s.append(Table(rows, colWidths=[5.6*cm]*3, style=[('VALIGN', (0, 0), (-1, -1), 'TOP')]))
GH = 'https://github.com/agent2897/mobile-dev-labs/tree/main/lab6-currency'
s += [PageBreak(), Paragraph('Код програми', h),
      Paragraph(f'Код програми розміщено на GitHub: <link href="{GH}" color="blue"><u>{GH}</u></link>', n),
      Spacer(1, 6)]
for p in ['MauiProgram.cs', 'AppShell.xaml', 'AppShell.xaml.cs', 'Models/Rate.cs',
          'Services/NbuService.cs', 'Services/FavoritesService.cs', 'ViewModels/BaseViewModel.cs',
          'ViewModels/RatesViewModel.cs', 'ViewModels/ConverterViewModel.cs', 'ViewModels/DetailsViewModel.cs',
          'Views/RatesPage.xaml', 'Views/RatesPage.xaml.cs', 'Views/ConverterPage.xaml',
          'Views/ConverterPage.xaml.cs', 'Views/DetailsPage.xaml', 'Views/DetailsPage.xaml.cs',
          'Views/FavoritesPage.cs', 'Controls/RateChart.cs', 'CurrencyApp.csproj']:
    s += [Paragraph('<b>' + p + '</b>', ParagraphStyle('f', parent=n, firstLineIndent=0, fontSize=12)),
          Preformatted(src(p), code), Spacer(1, 8)]

s += [Paragraph('Висновки', h),
      Paragraph('У ході лабораторної роботи з нуля розроблено мобільний додаток «Курси валют НБУ» на '
                'технології .NET MAUI мовою C#. Реалізовано отримання офіційних курсів з API Національного '
                'банку, пошук, сторінку валюти з власноруч намальованим графіком динаміки, конвертер валют '
                'та список обраних. Додаток зібрано для Android і перевірено на емуляторі з реальними даними. '
                'Отримано практичні навички роботи з XAML, шаблоном MVVM, прив’язками даних і командами, '
                'впровадженням залежностей, навігацією Shell, HttpClient та графікою MAUI.', n)]

SimpleDocTemplate(out, pagesize=A4, leftMargin=2.5*cm, rightMargin=1.5*cm,
                  topMargin=2*cm, bottomMargin=2*cm, title='Лабораторна робота 6').build(s)
