from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
text = (root/'tex/3/chapter.tex').read_text(encoding='utf-8')
text = re.sub(r'^%.*\n', '', text, flags=re.M)
text = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', text, flags=re.S)
text = re.sub(r'\\setcounter\{figure\}\{\d+\}', '', text)
footnote_number = 0
def preserve_footnote_number(match):
    global footnote_number
    if match.group().startswith(r'\setcounter'):
        footnote_number = int(re.search(r'\{(\d+)\}$', match.group()).group(1))
        return ''
    footnote_number += 1
    return r'\footnote[' + str(footnote_number) + ']'
text = re.sub(r'\\setcounter\{footnote\}\{\d+\}|\\footnote(?=\{)', preserve_footnote_number, text)
text = re.sub(r'\\eqref\{q3:eq-(\d+)-(\d+)\}', lambda m: '('+m[1]+'.'+m[2]+')', text)
text = re.sub(r'\\ref\{q3:fig-(\d+)\}', lambda m: m[1], text)

def excerpt(start, end):
    a = text.index(start)
    return text[a:text.index(end, a)].strip()

quotes = [
    (excerpt('Интегральная формулировка закона', r'\topic{Уравнение баланса'), '3', '14'),
    (excerpt('Исторически уравнение', ' По структуре уравнение'), '3', '14--15'),
    (excerpt(r'В случае \textit{недеформируемого неподвижного}', '\nДоказательство первой'), '5', '25'),
    (excerpt('Теперь с помощью (5.1)', r'\topic{Упрощение уравнения движения'), '5', '26--27'),
    (excerpt('Удобно выделить в явном виде', '\nОтметим, что если жидкость'), '5', '28'),
    (excerpt('В случае постоянной пористости закон', '\nПодчеркнем, что даже'), '5', '29'),
    (excerpt('Осреднение уравнения энергии для жидкости', r'\topic{Упрощение уравнения энергии}'), '5', '29--30'),
    (excerpt('Этому уравнению можно придать', r'\subsection*{§ 6.'), '5', '30--31'),
    (excerpt('Связь параметров при переходе', '\nУсловие (6.2) несложно'), '6', '32'),
    (excerpt('Применение (6.2) к законам', '\nДалее мы перечислим'), '6', '33'),
    (excerpt('На границе пористой среды с непроницаемой', ' Примерами таких границ'), '6', '33'),
    (excerpt('Обратим внимание, что при микроскопическом', r'\topic{Граница пористой среды с чистым флюидом}'), '6', '33--34'),
    (excerpt('Во многих задачах встречаются границы', ' Такой границей,')+'\n\n[…]\n\n'+excerpt('Как правило, на таких границах', r'\topic{Граница раздела фаз'), '6', '34'),
    (excerpt('Если разные части пористой среды', '\nНапример, часто')+'\n\n[…]\n\n'+excerpt('При изотермической фильтрации на подвижной', r'\topic{Промежуток'), '6', '35'),
    (excerpt('В ряде гидротехнических задач', r'\topic{Граница двух пористых сред}'), '6', '36'),
    (text[text.index(r'\topic{Граница двух пористых сред}'):].strip(), '6', '36--37'),
]

preamble = r'''% !TeX program = xelatex
% Вопрос 3. Только цитаты из ../../tex/3/chapter.tex.
% Библиографические сведения: ../../tex/3/main.tex.
% Пропуски обозначены […]. Внешние ссылки оригинала сохранены в читаемом виде.
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[english,russian]{babel}
\usepackage{amsmath,amssymb,cancel}
\usepackage[margin=22mm]{geometry}
\usepackage[unicode,hidelinks]{hyperref}
\DeclareMathOperator{\grad}{grad}
\DeclareMathOperator{\Div}{div}
\newcommand{\Rey}{\mathrm{Re}}
\newcommand{\topic}[1]{\par\medskip\noindent\textbf{#1}\par\nobreak\smallskip}
\setlength{\emergencystretch}{3em}
\interfootnotelinepenalty=10000
\setlength{\parindent}{0pt}
\renewcommand{\thefootnote}{\arabic{footnote})}
\newenvironment{textquote}{\begin{quote}}{\end{quote}}
\newcommand{\source}[2]{\par\nobreak\smallskip{\small Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд., 2017. Глава I, §~#1, с.~#2.}\par\medskip}
\begin{document}
% BEGIN QUESTION HEADER
\section*{Вопрос 3}
\noindent Уравнения баланса массы, импульса и энергии для течений в пористых средах. Соотношения на разрывах. Типичные граничные условия.

\medskip
\noindent\textbf{Источник:} Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд. Москва: МАКС Пресс, 2017. Глава I, §§ 3, 5--6, печатные страницы 13--17 и 24--37. Ответ составлен из дословных цитат перенесённого в TeX текста учебника.
\par\bigskip
% END QUESTION HEADER
'''
parts = [preamble]
for i, (quote, section, pages) in enumerate(quotes, 1):
    parts.append(f'% Цитата {i}; печатные страницы: {pages}\n')
    parts.append('\\begin{textquote}\n'+quote+'\n')
    parts.append(f'\\source{{{section}}}{{{pages}}}\n')
    parts.append('\\end{textquote}\n\n')
parts.append('\\end{document}\n')
(root/'tex_результат/3/3.tex').write_text(''.join(parts), encoding='utf-8')
print('Saved 3.tex; quotations:', len(quotes))

# % Paths updated
