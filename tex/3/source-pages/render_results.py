from pathlib import Path
import fitz
from PIL import Image

root = Path(__file__).resolve().parents[3]
out = Path(__file__).resolve().parent
for name, file in [('full', root/'tex/3/main.pdf'), ('answer', root/'tex_результат/3.pdf')]:
    doc = fitz.open(file)
    print(name, len(doc))
    for j in range(0, len(doc), 2):
        canvas = Image.new('RGB', (1440, 1020), '#cccccc')
        for i in range(j, min(j+2, len(doc))):
            pix = doc[i].get_pixmap(matrix=fitz.Matrix(1.2, 1.2))
            canvas.paste(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), ((i-j)*720, 0))
        canvas.save(out/f'{name}-{j//2+1}.png')
