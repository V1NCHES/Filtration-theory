from pathlib import Path
import re, sys

root=Path(__file__).resolve().parent.parent
n=int(sys.argv[1])
settings={
6:('Гидравлическая теория безнапорной фильтрации. Уравнение Буссинеска. Формула Дюпюи для безнапорной фильтрации.','II','9','54--58',[
('Строгое математическое описание','К указанной гипотезе'),
('С использованием предположений',r'\topic{Формулы Дюпюи'),
('В случае стационарного плоскопараллельного',r'\topic{Строгое доказательство'),
('Формулы Дюпюи являются приближенными','Этот результат,')]),
7:('Изотермическая фильтрация газа в недеформируемой пористой среде. Уравнение для давления (уравнение Лейбензона). Аналогия с пологими безнапорными движениями несжимаемой жидкости в пористой среде.','III','11','66--69',[
('При фильтрации газа','Из этих уравнений'),
('Из этих уравнений',r'\topic{Граничные условия}')]),
8:('Упругий режим фильтрации. Уравнение пьезопроводности. Постановка задачи о распространении плоской волны повышения давления в полубесконечном пласте. Оценка характерного времени распространения возмущения давления.','III','12','70--77',[('В отличие от газов', 'Как и в случае фильтрации газа'),('Как и в случае фильтрации газа',r'\topic{Распространение'),('Рассмотрим одномерную задачу',r'\topic{Пуск скважины')]),
}
question,chap,sec,pages,selections=settings[n]
folder=root/'tex'/str(n);out=root/'tex_результат'/str(n);out.mkdir(parents=True,exist_ok=True)
body=(folder/'chapter.tex').read_text(encoding='utf-8')
preamble=r'''% !TeX program = xelatex
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[english,russian]{babel}
\usepackage{amsmath,amssymb,mathrsfs,cancel}
\usepackage[margin=22mm]{geometry}
\usepackage{graphicx,float}
\usepackage[unicode,hidelinks]{hyperref}
\DeclareMathOperator{\grad}{grad}
\DeclareMathOperator{\Div}{div}
\newcommand{\Rey}{\mathrm{Re}}
\setlength{\emergencystretch}{3em}
\interfootnotelinepenalty=10000
\newcommand{\topic}[1]{\par\medskip\noindent\textbf{#1}\par\nobreak\smallskip}
\renewcommand{\thefootnote}{\arabic{footnote})}
'''
header=f'\\section*{{Вопрос {n}}}\n\\noindent {question}\n\n\\medskip\n\\noindent\\textbf{{Источник:}} Н. Е. Леонтьев. \\textit{{Основы теории фильтрации}}. 2-е изд. Москва: МАКС Пресс, 2017. Глава {chap}, § {sec}, печатные страницы {pages}.\n\\par\\bigskip\n'
(folder/'main.tex').write_text(preamble+'\\begin{document}\n'+header+'\\input{chapter}\n\\end{document}\n',encoding='utf-8')
if not selections:
    print('Created main only; answer selections must be provided for',n);sys.exit()
pieces=[]
markers=list(re.finditer(r'% Источник:.*?печатная страница: (\d+);.*',body))
def pageat(index):
    return [int(m[1]) for m in markers if m.start()<=index][-1]
for start,end in selections:
    a=body.index(start);b=body.index(end,a)
    piece=body[a:b].strip()
    p1=pageat(a)
    content_lines=[m for m in re.finditer(r'^.+$',body[a:b],re.M) if m[0].strip() and not m[0].lstrip().startswith(('%',r'\setcounter'))]
    p2=pageat(a+content_lines[-1].end()-1)
    piece=re.sub(r'^%.*\n','',piece,flags=re.M)
    piece=re.sub(r'\\begin\{figure\}.*?\\end\{figure\}','',piece,flags=re.S)
    piece=re.sub(r'\\setcounter\{figure\}\{\d+\}','',piece)
    piece=re.sub(r'\\eqref\{q\d+:eq-(\d+)-(\d+)\}',lambda m:'('+m[1]+'.'+m[2]+')',piece)
    piece=re.sub(r'\\ref\{q\d+:fig-(\d+)\}',lambda m:m[1],piece)
    pieces.append('\\begin{quote}\\sloppy\n'+piece+f'\n\\par\\nobreak\\smallskip{{\\small Н. Е. Леонтьев. \\textit{{Основы теории фильтрации}}. 2-е изд., 2017. Глава {chap}, § {sec}, с. {p1}'+(f'--{p2}' if p2!=p1 else '')+'.}\\par\n\\end{quote}\n\n')
(out/f'{n}.tex').write_text(preamble+'\\begin{document}\n'+header+''.join(pieces)+'\\end{document}\n',encoding='utf-8')
print('Created main and answer',n)
