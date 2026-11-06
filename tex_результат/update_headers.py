from pathlib import Path

folder = Path(__file__).resolve().parent
questions = {
    1: ('Основные физические сведения о пористых средах. Описание фильтрации в рамках механики сплошных сред. Пористость. Скорость фильтрации.', 'Глава I, §§ 1--2, печатные страницы 7--13.'),
    2: ('Закон Дарси и пределы его применимости. Учёт анизотропии пористой среды. Двучленный закон фильтрации Форхгеймера. Фильтрация с предельным градиентом давления.', 'Глава I, §§ 3--4, печатные страницы 13--24.'),
    3: ('Уравнения баланса массы, импульса и энергии для течений в пористых средах. Соотношения на разрывах. Типичные граничные условия.', 'Глава I, §§ 3, 5--6, печатные страницы 13--17 и 24--37.'),
    4: ('Замкнутая система уравнений для фильтрации несжимаемой жидкости. Стационарные решения для одномерных течений (с плоскими волнами, течений в случае осевой симметрии). Напорный приток к совершенной скважине с постоянным расходом (дебитом). Формула Дюпюи для напорной фильтрации.', 'Глава II, § 7, печатные страницы 38--43.'),
}

for n, (question, location) in questions.items():
    header = (
        '% BEGIN QUESTION HEADER\n'
        f'\\section*{{Вопрос {n}}}\n'
        f'\\noindent {question}\n\n'
        '\\medskip\n'
        '\\noindent\\textbf{Источник:} Н. Е. Леонтьев. '
        '\\textit{Основы теории фильтрации}. 2-е изд. Москва: МАКС Пресс, 2017. '
        f'{location} Ответ составлен из дословных цитат перенесённого в TeX текста учебника.\n'
        '\\par\\bigskip\n'
        '% END QUESTION HEADER\n'
    )
    tex_path = folder / str(n) / f'{n}.tex'
    content = tex_path.read_text(encoding='utf-8')
    if '% BEGIN QUESTION HEADER' not in content:
        content = content.replace('\\begin{document}\n', '\\begin{document}\n'+header, 1)
        tex_path.write_text(content, encoding='utf-8')

    script = folder/str(n)/('build_answer.py' if n == 4 else f'build_answer_{n}.py')
    content = script.read_text(encoding='utf-8')
    # Questions 1--3 were moved into numbered folders after their creation.
    content = content.replace('root = Path(__file__).resolve().parent.parent', 'root = Path(__file__).resolve().parents[2]')
    content = content.replace(f"tex_результат/{n}.tex", f"tex_результат/{n}/{n}.tex")
    if '% BEGIN QUESTION HEADER' not in content:
        content = content.replace('\\begin{document}\n', '\\begin{document}\n'+header, 1)
    content = content.replace('../tex/', '../../tex/').replace('../../../tex/', '../../tex/') if '% Paths updated' not in content else content
    if '% Paths updated' not in content:
        # Keep this marker in Python syntax; it makes path adjustment idempotent.
        content += '\n# % Paths updated\n'
    script.write_text(content, encoding='utf-8')
    print(f'Updated {n}/{n}.tex and generator')
