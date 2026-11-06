from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
text = (root/'tex/4/chapter.tex').read_text(encoding='utf-8')
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
    return r'\footnote['+str(footnote_number)+']'
text = re.sub(r'\\setcounter\{footnote\}\{\d+\}|\\footnote(?=\{)', preserve_footnote_number, text)
text = re.sub(r'\\eqref\{q4:eq-(\d+)-(\d+)\}', lambda m: '('+m[1]+'.'+m[2]+')', text)
text = re.sub(r'\\ref\{q4:fig-(\d+)\}', lambda m: m[1], text)

def excerpt(start, end):
    a = text.index(start)
    return text[a:text.index(end,a)].strip()

quotes = [
    (excerpt('Полная система уравнений', '\nСистема (7.1) годится'), '38'),
    (excerpt('Для экспериментального определения', '\nПри $h\\to d$'), '39--40'),
    (excerpt('Предположим, что в некоторую точку', '\nОбратим внимание, что в окрестности'), '40--41'),
    (excerpt('Обратим внимание, что в окрестности', r'\topic{Скважина, вскрывающая тонкий пласт}'), '41--42'),
    (text[text.index('Находящиеся в недрах земли'):].strip(), '42--43'),
]

preamble = r'''% !TeX program = xelatex
% Вопрос 4. Только цитаты из ../../tex/4/chapter.tex.
% Библиографические сведения взяты из ../../tex/4/main.tex.
% Несогласованность промежуточного равенства Q=...=4πA на странице 41 сохранена как в исходном TeX.
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[english,russian]{babel}
\usepackage{amsmath,amssymb}
\usepackage[margin=22mm]{geometry}
\usepackage[unicode,hidelinks]{hyperref}
\DeclareMathOperator{\grad}{grad}
\DeclareMathOperator{\Div}{div}
\setlength{\emergencystretch}{3em}
\interfootnotelinepenalty=10000
\setlength{\parindent}{0pt}
\renewcommand{\thefootnote}{\arabic{footnote})}
\newenvironment{textquote}{\begin{quote}}{\end{quote}}
\newcommand{\source}[1]{\par\nobreak\smallskip{\small Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд., 2017. Глава II, §~7, с.~#1.}\par\medskip}
\begin{document}
% BEGIN QUESTION HEADER
\section*{Вопрос 4}
\noindent Замкнутая система уравнений для фильтрации несжимаемой жидкости. Стационарные решения для одномерных течений (с плоскими волнами, течений в случае осевой симметрии). Напорный приток к совершенной скважине с постоянным расходом (дебитом). Формула Дюпюи для напорной фильтрации.

\medskip
\noindent\textbf{Источник:} Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд. Москва: МАКС Пресс, 2017. Глава II, § 7, печатные страницы 38--43. Ответ составлен из дословных цитат перенесённого в TeX текста учебника.
\par\bigskip
% END QUESTION HEADER
'''
parts = [preamble]
for i,(quote,pages) in enumerate(quotes,1):
    parts.append(f'% Цитата {i}; печатные страницы: {pages}\n')
    parts.append('\\begin{textquote}\n'+quote+'\n')
    parts.append(f'\\source{{{pages}}}\n\\end{{textquote}}\n\n')
parts.append('\\end{document}\n')
(Path(__file__).resolve().parent/'4.tex').write_text(''.join(parts),encoding='utf-8')
print('Saved 4.tex; quotations:',len(quotes))

# % Paths updated
