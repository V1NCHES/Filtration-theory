from pathlib import Path
import re
root=Path.cwd();folder=root/'tex/9';out=root/'tex_результат/9'
pre=(root/'tex/8/main.tex').read_text(encoding='utf-8').split('\\begin{document}')[0]
pre=pre.replace('\\setlength{\\emergencystretch}{3em}','\\setlength{\\emergencystretch}{3em}\n\\sloppy')
question='Вытеснение несмешивающихся жидкостей. Одномерная задача о поршневом вытеснении несмешивающихся жидкостей (модель Лейбензона — Маскета). Устойчивость фронта вытеснения (элементарная теория).'
source=r'К. С. Басниев, А. М. Власов, И. Н. Кочина, В. М. Максимов. \textit{Подземная гидравлика}. Москва: Недра, 1986. Глава 8, §§ 1, 2, 4; с. 188--193, 196--198.'
header='\\section*{Вопрос 9}\n'+question+'\n\n\\medskip\n\\noindent\\textbf{Источник:} '+source+'\n\\par\\bigskip\n'
body=(folder/'chapter.tex').read_text(encoding='utf-8')
(folder/'main.tex').write_text(pre+'\\begin{document}\n'+header+'\\input{chapter}\n\\end{document}',encoding='utf-8')
# Retain the figure numbering of the book; selected quotes contain text and equations.
items=[
('Согласно условию неразрывности','Касательные составляющие', '1','188'),
('Линии тока не будут преломляться',r'\subsection*{§ 2.', '1','189'),
('При поршневом вытеснении','Вспомним, что', '2','189'),
('При этом изобарами','Определим теперь', '2','190'),
('2. Скорость фильтрации.','3. Расход жидкости', '2','190'),
('5. Закон движения границы','Для нахождения зависимости', '2','191'),
('Пусть нефтяная залежь',None, '4','197--198')]
pieces=[]
for start,end,sec,pages in items:
 a=body.index(start);b=body.index(end,a) if end else len(body);s=body[a:b].strip()
 s=re.sub(r'^%.*(?:\n|$)','',s,flags=re.M)
 s=re.sub(r'\\begin\{figure\}.*?\\end\{figure\}','',s,flags=re.S)
 s=re.sub(r'\\renewcommand\{\\thefigure\}\{8\.\\arabic\{figure\}\}\\setcounter\{figure\}\{5\}','',s)
 s=re.sub(r'\\eqref\{q9:eq-(\d+)-(\d+)\}',lambda m:'('+m[1]+'.'+m[2]+')',s)
 s=re.sub(r'\\ref\{q9:fig-8-(\d+)\}',lambda m:'8.'+m[1],s)
 citation=r'{\small К. С. Басниев, А. М. Власов, И. Н. Кочина, В. М. Максимов. \textit{Подземная гидравлика}. 1986. Глава 8, § '+sec+', с. '+pages+'.}'
 pieces.append('\\begin{quote}\\sloppy\n'+s+'\n\\par\\nobreak\\smallskip\n'+citation+'\\par\n\\end{quote}\n\n')
notice='\\noindent В формуле (8.42) перед $\\partial z$ на скане виден дополнительный вертикальный штрих. Это место требует сверки с более чётким изображением оригинала; штрих сохранён.\n'
(out/'9.tex').write_text(pre+'\\begin{document}\n'+header+''.join(pieces)+notice+'\\end{document}\n',encoding='utf-8')
# Fix the tiny spill of the adjacent caption in figure 8.4.
from PIL import Image
im=Image.open(folder/'source-pages/page-193.png');im.crop((130,1320,835,1610)).save(folder/'figures/fig-8-4.png')
