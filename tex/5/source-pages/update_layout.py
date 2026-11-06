from pathlib import Path
import fitz

root = Path(__file__).resolve().parents[3]
doc = fitz.open(root/'Литература/porous-lecture-notes.pdf')
doc[13].get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(610,447,842,542)).save(str(root/'tex/5/figures/notes-potential-domain.png'))
p = root/'tex/5/notes.tex'
s = p.read_text(encoding='utf-8').replace('width=.38\\linewidth]{figures/notes-potential', 'width=.54\\linewidth]{figures/notes-potential')
p.write_text(s,encoding='utf-8')
p = root/'tex/5/main.tex'
s = p.read_text(encoding='utf-8').replace('\\input{notes}', '\\par\\medskip\n\\input{notes}')
p.write_text(s,encoding='utf-8')
p = root/'tex_результат/5/build_answer.py'
s = p.read_text(encoding='utf-8').replace("parts.append(r'\\section*{Отдельный", "parts.append(r'\\clearpage\\section*{Отдельный")
p.write_text(s,encoding='utf-8')
print('Updated layout and complete potential-domain crop')
