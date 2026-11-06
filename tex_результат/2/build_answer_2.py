from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
text = (root / 'tex/2/chapter.tex').read_text(encoding='utf-8')
text = re.sub(r'^%.*\n', '', text, flags=re.M)
footnote_number = 0
def preserve_footnote_number(match):
    global footnote_number
    if match.group().startswith(r'\setcounter'):
        footnote_number = 0
        return ''
    footnote_number += 1
    return r'\footnote[' + str(footnote_number) + ']'
text = re.sub(r'\\setcounter\{footnote\}\{0\}|\\footnote(?=\{)', preserve_footnote_number, text)
text = text.replace(r'\ref{q2:fig-5}', '5').replace(r'\ref{q2:fig-6}', '6')

def excerpt(start, end):
    a = text.index(start)
    return text[a:text.index(end, a)].strip()

quotes = [
    (excerpt('Исторически уравнение', ' При медленных (ползущих)'), '3', '14--15'),
    (excerpt('При медленных (ползущих)', '\n\nПри $'), '3', '15'),
    (excerpt('При $', '\n\nЕсли жидкость в порах'), '3', '15'),
    (excerpt('Коэффициент проницаемости $k$', ' Он имеет размерность') + '\n\n[…]\n\n' + excerpt('Для неоднородных пористых сред', '\n\n\\topic'), '3', '16'),
    (excerpt('При фильтрации в анизотропных', '\n\n\\subsection'), '3', '17'),
    (excerpt('В некоторых практически важных', '\n\n\\topic'), '4', '18'),
    (excerpt('Предполагая для простоты', '\nЧто касается направления'), '4', '18--19'),
    (excerpt('Итак, общий вид закона', '\n\\setcounter{figure}'), '4', '19--20'),
    (excerpt('В противоположном случае', '\nПример зависимости'), '4', '20'),
    (excerpt('При практических расчетах', '\n\n\\topic'), '4', '21'),
    (excerpt('Как видно из рис.', '\n\n\\topic'), '4', '21'),
    (excerpt('В ряде природных процессов', ' В качестве примеров'), '4', '22--23'),
    (excerpt('Для моделирования таких явлений', '\n\nНаличие предельного'), '4', '23'),
    (text[text.index('Наличие предельного градиента'):].strip(), '4', '23--24'),
]

preamble = r'''% !TeX program = xelatex
% Вопрос 2. Только цитаты из ../../tex/2/chapter.tex.
% Библиографические сведения: ../../tex/2/main.tex.
% Источником отбора цитат служит TeX, а не иные книги или сведения по памяти.
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[english,russian]{babel}
\usepackage{amsmath,amssymb}
\usepackage[margin=22mm]{geometry}
\usepackage[unicode,hidelinks]{hyperref}
\DeclareMathOperator{\grad}{grad}
\DeclareMathOperator{\Div}{div}
\newcommand{\Rey}{\mathrm{Re}}
\setlength{\emergencystretch}{3em}
\setlength{\parindent}{0pt}
\renewcommand{\thefootnote}{\arabic{footnote})}
\newenvironment{textquote}{\begin{quote}}{\end{quote}\nopagebreak[4]}
\newcommand{\source}[2]{\par\nobreak\smallskip{\small Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд., 2017. Глава I, §~#1, с.~#2.}\par\medskip}
\begin{document}
% BEGIN QUESTION HEADER
\section*{Вопрос 2}
\noindent Закон Дарси и пределы его применимости. Учёт анизотропии пористой среды. Двучленный закон фильтрации Форхгеймера. Фильтрация с предельным градиентом давления.

\medskip
\noindent\textbf{Источник:} Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд. Москва: МАКС Пресс, 2017. Глава I, §§ 3--4, печатные страницы 13--24. Ответ составлен из дословных цитат перенесённого в TeX текста учебника.
\par\bigskip
% END QUESTION HEADER
'''
parts = [preamble]
for i, (quote, section, pages) in enumerate(quotes, 1):
    parts.append(f'% Цитата {i}; печатные страницы: {pages}\n')
    parts.append('\\begin{textquote}\n' + quote + '\n')
    parts.append(f'\\source{{{section}}}{{{pages}}}\n')
    parts.append('\\end{textquote}\n\n')
parts.append('\\end{document}\n')
(root / 'tex_результат/2/2.tex').write_text(''.join(parts), encoding='utf-8')
print('Saved 2.tex; quotations:', len(quotes))

# % Paths updated
