from pathlib import Path
import re,sys,json
root=Path(__file__).resolve().parent.parent;n=int(sys.argv[1]);d=root/'tex'/str(n);out=root/'tex_результат'/str(n);out.mkdir(exist_ok=True)
cfg=json.loads((d/'config.json').read_text(encoding='utf-8'));body=(d/'chapter.tex').read_text(encoding='utf-8')
pre=(root/'tex/9/main.tex').read_text(encoding='utf-8').split('\\begin{document}')[0]
header=f'\\section*{{Вопрос {n}}}\n'+cfg['question']+'\n\n\\medskip\n\\noindent\\textbf{Источник:} '+cfg['source']+'\n\\par\\bigskip\n'
(d/'main.tex').write_text(pre+'\\begin{document}\n'+header+'\\input{chapter}\n\\end{document}\n',encoding='utf-8')
pieces=[]
for x in cfg['quotes']:
 a=body.index(x['start']);b=body.index(x['end'],a) if x.get('end') else len(body);s=body[a:b].strip()
 s=re.sub(r'^%.*(?:\n|$)','',s,flags=re.M);s=re.sub(r'\\begin\{figure\}.*?\\end\{figure\}','',s,flags=re.S)
 s=re.sub(r'\\renewcommand\{\\thefigure\}\{[\dIVX]+\.\\arabic\{figure\}\}|\\setcounter\{figure\}\{\d+\}','',s)
 s=re.sub(r'\\eqref\{q\d+:eq-([\dIVX-]+)\}',lambda m:'('+m[1].replace('-','.')+')',s)
 s=re.sub(r'\\ref\{q\d+:fig-([\dIVX-]+)\}',lambda m:m[1].replace('-','.'),s)
 pieces.append('\\begin{quote}\\sloppy\n'+s+'\n\\par\\nobreak\\smallskip{\\small '+x['cite']+'}\\par\n\\end{quote}\n\n')
(out/f'{n}.tex').write_text(pre+'\\begin{document}\n'+header+''.join(pieces)+'\\end{document}\n',encoding='utf-8')
