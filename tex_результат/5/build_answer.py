from pathlib import Path
import re
import shutil

out = Path(__file__).resolve().parent
root = out.parents[1]
text = (root/'tex/5/chapter.tex').read_text(encoding='utf-8')
text = re.sub(r'^%.*\n', '', text, flags=re.M)
def keep_dam_diagram(match):
    return match.group() if 'figure-15.png' in match.group() else ''
text = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', keep_dam_diagram, text, flags=re.S)
text = re.sub(r'\\setcounter\{figure\}\{\d+\}', '', text)
text = text.replace(r'\begin{figure}[H]', '\\setcounter{figure}{14}\n'+r'\begin{figure}[H]')
footnote_number = 0
def preserve_footnote_number(match):
    global footnote_number
    if match.group().startswith(r'\setcounter'):
        footnote_number = int(re.search(r'\{(\d+)\}$', match.group()).group(1))
        return ''
    footnote_number += 1
    return r'\footnote['+str(footnote_number)+']'
text = re.sub(r'\\setcounter\{footnote\}\{\d+\}|\\footnote(?=\{)', preserve_footnote_number, text)
text = re.sub(r'\\eqref\{q5:eq-(\d+)-(\d+)\}', lambda m: '('+m[1]+'.'+m[2]+')', text)
text = re.sub(r'\\ref\{q5:fig-(\d+)\}', lambda m: m[1], text)

def excerpt(start,end):
    a = text.index(start)
    return text[a:text.index(end,a)].strip()

quotes = [
    (excerpt('Во многих практически важных', r'\topic{Плоскопараллельная'), '43'),
    (excerpt('Рассмотрим плоское фильтрационное', '\nПокажем, к каким условиям'), '44--45'),
    (excerpt('На непроницаемой границе,', r'\topic{Граница с водоемом}'), '45'),
    (excerpt('На границах этого типа', r'\topic{Поверхность депрессии}'), '45--46'),
    (excerpt(r'В случае \textit{стационарной}', r'\topic{Поверхность высачивания}'), '46'),
    (excerpt('Для поверхности высачивания', '\nПриведем теперь примеры'), '47'),
    (excerpt(r'\topic{Непроницаемая плотина', '\nБесконечность функции тока'), '47--48'),
    (excerpt('Если теперь нам удастся', '\nДифференцируя это соотношение'), '48'),
    (excerpt('Аналогичным образом методы', r'\topic{Скважина в поступательном потоке}'), '52'),
]

preamble = r'''% !TeX program = xelatex
% Цитаты только из ../../tex/5/chapter.tex и отдельно разрешённого пользователем ../../tex/5/notes.tex.
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[english,russian]{babel}
\usepackage{amsmath,amssymb}
\usepackage[margin=22mm]{geometry}
\usepackage{graphicx,float}
\usepackage[unicode,hidelinks]{hyperref}
\DeclareMathOperator{\grad}{grad}
\setlength{\emergencystretch}{3em}
\interfootnotelinepenalty=10000
\setlength{\parindent}{0pt}
\renewcommand{\thefootnote}{\arabic{footnote})}
\newcommand{\topic}[1]{\par\medskip\noindent\textbf{#1}\par\nobreak\smallskip}
\newenvironment{textquote}{\begin{quote}\sloppy}{\end{quote}}
\newcommand{\source}[1]{\par\nobreak\smallskip{\small Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд., 2017. Глава II, §~8, с.~#1.}\par\medskip}
\begin{document}
\section*{Вопрос 5}
\noindent Плоская установившаяся фильтрация несжимаемой жидкости. Типичные постановки задач. Применение методов ТФКП. Примеры: постановка задачи о водонепроницаемой плотине с плоским основанием; постановка задачи о работе кротового оросителя.

\medskip
\noindent\textbf{Источники:} Н. Е. Леонтьев. \textit{Основы теории фильтрации}. 2-е изд. Москва: МАКС Пресс, 2017. Глава II, § 8, печатные страницы 43--54. Для трубы-источника отдельно включён фрагмент \textit{рукописного конспекта лекций}, файл \texttt{porous-lecture-notes.pdf}, страницы PDF 14--15; автор и год не указаны. Ниже приведены дословные цитаты перенесённых в TeX материалов.
\par\bigskip
'''
parts = [preamble]
for i,(quote,pages) in enumerate(quotes,1):
    parts.append(f'% Цитата {i}; печатные страницы: {pages}\n')
    parts.append('\\begin{textquote}\n'+quote+'\n')
    parts.append(f'\\source{{{pages}}}\n\\end{{textquote}}\n\n')
parts.append(r'\clearpage\section*{Отдельный фрагмент конспекта: труба-источник}'+'\n')
parts.append('\\begin{textquote}\n')
parts.append((root/'tex/5/notes.tex').read_text(encoding='utf-8'))
parts.append('\n\\par\\nobreak\\smallskip{\\small Рукописный конспект лекций, \\texttt{porous-lecture-notes.pdf}, страницы файла 14--15, видимые рукописные номера разворотов 14 и 15. Автор, год, глава и параграф не указаны. Печатная нумерация не установлена.}\n\\end{textquote}\n')
parts.append('\\end{document}\n')
(out/'5.tex').write_text(''.join(parts),encoding='utf-8')
(out/'figures').mkdir(exist_ok=True)
for name in ['figure-15.png','notes-physical-domain.png','notes-potential-domain.png','notes-hodographs.png']:
    shutil.copy2(root/'tex/5/figures'/name,out/'figures'/name)
print('Saved 5.tex; textbook quotations:',len(quotes),'; separate notes fragment included')
