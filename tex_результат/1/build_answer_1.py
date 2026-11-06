from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
text = (root / 'tex/1/chapter.tex').read_text(encoding='utf-8')
text = re.sub(r'^%.*\n', '', text, flags=re.M)
text = re.sub(r'\\setcounter\{footnote\}\{0\}', '', text)
text = text.replace('\\ref{q1:fig-1}', '1').replace('\\ref{q1:fig-2}', '2').replace('\\ref{q1:fig-3}', '3')

def excerpt(start, end):
    a = text.index(start)
    return text[a:text.index(end, a)].strip()

quotes = [
    (excerpt(r'\textit{Фильтрацией}', ' Фильтрационные процессы'), '1', '7'),
    (excerpt('Вне зависимости', ' Но и даже'), '1', '7'),
    (excerpt('К счастью, однако', r'\begin{figure}'), '1', '7--8'),
    (excerpt('Например, при просачивании', r'\subsection*{§ 2.'), '1', '8--9'),
    (excerpt('Важной характеристикой', '\n\nУ некоторых'), '2', '9'),
    (excerpt('У некоторых пористых материалов', ' В качестве примера сред') + r' […]', '2', '9'),
    (excerpt('Для неоднородных пористых сред', r'\begin{figure}'), '2', '9'),
    (excerpt('Подчеркнем, что при континуальном', ' Если бы осреднение'), '2', '10'),
    (excerpt('Если сделать мысленный', '\n\nВеличина просветности'), '2', '10'),
    (excerpt('Величина просветности', ' В самом деле,') + '\n\n[…]\n\n' + excerpt('Доказанное свойство', ' Отметим также'), '2', '10--11'),
    (excerpt('Обратим внимание, что упоминавшиеся', '\n\n\\topic{Скорость'), '2', '11'),
    (excerpt('Для характеристики массопереноса', ' Например, для речного песка'), '2', '11--12'),
    (excerpt('В общем случае неодномерного', '\n\nВстречающиеся'), '2', '12'),
]

preamble = r'''% !TeX program = xelatex
% Вопрос 1. Источники текста: ../../tex/1/chapter.tex и библиографические сведения ../../tex/1/main.tex.
% Ответ составлен только из цитат предоставленного TeX; по PDF оригинала в этой работе не сверялся.
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[english,russian]{babel}
\usepackage{amsmath,amssymb}
\usepackage[margin=22mm]{geometry}
\usepackage[unicode,hidelinks]{hyperref}
\setlength{\emergencystretch}{3em}
\setlength{\parindent}{0pt}
\renewcommand{\thefootnote}{\arabic{footnote})}
\newenvironment{textquote}{\begin{quote}}{\end{quote}}
\newcommand{\source}[2]{\par\nobreak\smallskip{\small Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд., 2017. Глава I, §~#1, с.~#2.}\par\medskip}
\begin{document}
% BEGIN QUESTION HEADER
\section*{Вопрос 1}
\noindent Основные физические сведения о пористых средах. Описание фильтрации в рамках механики сплошных сред. Пористость. Скорость фильтрации.

\medskip
\noindent\textbf{Источник:} Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд. Москва: МАКС Пресс, 2017. Глава I, §§ 1--2, печатные страницы 7--13. Ответ составлен из дословных цитат перенесённого в TeX текста учебника.
\par\bigskip
% END QUESTION HEADER
'''
parts = [preamble]
for i, (quote, section, pages) in enumerate(quotes, 1):
    parts.append(f'% Цитата {i}; печатные страницы: {pages}\n')
    parts.append('\\begin{textquote}\n' + quote + '\n\\end{textquote}\n')
    parts.append(f'\\source{{{section}}}{{{pages}}}\n\n')
parts.append('\\end{document}\n')
(root / 'tex_результат/1/1.tex').write_text(''.join(parts), encoding='utf-8')
print('Saved tex_результат/1/1.tex; quotations:', len(quotes))

# % Paths updated
