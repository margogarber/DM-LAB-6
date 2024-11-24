def resolution_algorithm(clauses):
    """
    Виконання алгоритму резолюції для перевірки виконуванності множини диз’юнктів
    """
    new_clauses = set(frozenset(clause) for clause in clauses)  # Початкова множина диз’юнктів
    print("Початкова множина диз’юнктів:")
    for clause in new_clauses:
        print(f"  {set(clause)}")
    print()

    step = 1
    while True:
        # Отримати всі можливі пари диз’юнктів
        pairs = [(ci, cj) for ci in new_clauses for cj in new_clauses if ci != cj]
        resolved = set()

        print(f"Крок {step}: перевіряємо всі пари диз’юнктів...")
        for (ci, cj) in pairs:
            print(f"  Резолюція: {set(ci)} і {set(cj)}")
            # Спроба застосувати резолюцію
            resolvent = resolve(ci, cj)
            if resolvent is None:
                print("    Неможливо застосувати резолюцію.")
                continue
            print(f"    Отримано новий диз’юнкт: {set(resolvent)}")
            if not resolvent:  # Якщо порожній диз’юнкт
                print("\nЗнайдено порожній диз’юнкт! Множина диз’юнктів є невиконуваною.\n")
                return False
            resolved.add(frozenset(resolvent))

        # Якщо нових диз’юнктів не з'явилось, множина виконувана
        if resolved.issubset(new_clauses):
            print("\nНових диз’юнктів не знайдено. Множина диз’юнктів є виконуваною.\n")
            return True

        # Оновлюємо множину диз’юнктів
        new_clauses.update(resolved)
        print("Оновлена множина диз’юнктів:")
        for clause in new_clauses:
            print(f"  {set(clause)}")
        print()
        step += 1


def resolve(clause1, clause2):
    """
    Спроба виконати резолюцію між двома диз’юнктами.
    """
    for literal in clause1:
        if negate_literal(literal) in clause2:
            # Формуємо новий диз’юнкт, виключаючи суперечливі літерали
            resolvent = (clause1 - {literal}) | (clause2 - {negate_literal(literal)})
            return resolvent
    return None


def negate_literal(literal):
    """
    Заперечення літерала: якщо він заперечений, повернути незаперечений, і навпаки.
    """
    if literal.startswith("~"):
        return literal[1:]  # Прибираємо "~", якщо це заперечення
    else:
        return "~" + literal  # Додаємо "~", якщо це незаперечений літерал


# Множина диз’юнктів задається символами:
# clauses = [
#     {"~p", "q"},   # ~p ∨ q
#     {"~p", "s"},   # ~p ∨ s
#     {"~s"},        # ~s
#     {"~p"},        # ~p
# ]
#
# # Виконання алгоритму
# result = resolution_algorithm(clauses)
# if not result:
#     print("Висновок: множина диз’юнктів є невиконуваною. Існує протиріччя.\n")
# else:
#     print("Висновок: множина диз’юнктів є виконуваною. Протиріччя відсутнє.\n")

# def input_clauses():
#     """
#     Введення множини диз’юнктів користувачем.
#     """
#     print("Введіть множину диз’юнктів.")
#     print("Кожен диз’юнкт вводьте через пробіл (наприклад: ~q h).")
#     print("Введіть порожній рядок, щоб завершити.")
#
#     clauses = []
#     while True:
#         line = input("Диз’юнкт: ").strip()
#         if not line:  # Порожній рядок завершує введення
#             break
#         clauses.append(set(line.split()))  # Розділяємо літерали у множину
#     return clauses
#
#
# # Основна програма
# print("Алгоритм резолюції для перевірки виконуванності множини диз’юнктів.\n")
# clauses = input_clauses()
# result = resolution_algorithm(clauses)
# if not result:
#     print("Висновок: множина диз’юнктів є невиконуваною. Існує протиріччя.\n")
# else:
#     print("Висновок: множина диз’юнктів є виконуваною. Протиріччя відсутнє.\n")

def input_clauses():
    """
    Введення множини диз’юнктів користувачем із підтримкою імплікацій.
    """
    print("Введіть множину диз’юнктів.")
    print("Кожен диз’юнкт вводьте через пробіл (наприклад: p q для p ∨ q).")
    print("Для імплікації використовуйте стрілку -> (наприклад: p -> q).")
    print("Введіть порожній рядок, щоб завершити.")

    clauses = []
    while True:
        line = input("Диз’юнкт або імплікація: ").strip()
        if not line:  # Порожній рядок завершує введення
            break
        if "->" in line:  # Якщо є імплікація
            parts = line.split("->")
            antecedent = parts[0].strip()  # Ліва частина імплікації
            consequent = parts[1].strip()  # Права частина імплікації
            # Імплікація A -> B перетворюється на ~A ∨ B
            clauses.append({negate_literal(antecedent), consequent})
        else:
            # Додати диз’юнкт як набір літералів
            clauses.append(set(line.split()))
    return clauses


# Завдання 2
print("Алгоритм резолюції для перевірки виконуванності множини диз’юнктів.\n")
clauses = input_clauses()
result = resolution_algorithm(clauses)
if not result:
    print("Висновок: множина диз’юнктів є невиконуваною. Існує протиріччя.\n")
else:
    print("Висновок: множина диз’юнктів є виконуваною. Протиріччя відсутнє.\n")


def unify(disjunct1, disjunct2):
    """
    Алгоритм уніфікації для двох диз’юнктів.
    Знаходить підстановку, яка робить обидва диз’юнкти еквівалентними.
    """
    substitutions = {}  # Зберігає підстановки для уніфікації
    for literal1 in disjunct1:
        for literal2 in disjunct2:
            # Спроба уніфікувати два літерали
            result = unify_literals(literal1, literal2, substitutions)
            if result is None:
                return None  # Уніфікація неможлива
            substitutions.update(result)  # Оновлюємо підстановки
    return substitutions


def unify_literals(literal1, literal2, substitutions):
    """
    Уніфікація двох літералів з урахуванням поточних підстановок.
    """
    # Застосовуємо поточні підстановки
    literal1 = apply_substitution(literal1, substitutions)
    literal2 = apply_substitution(literal2, substitutions)

    # Якщо літерали рівні, уніфікація успішна
    if literal1 == literal2:
        return {}

    # Якщо один із літералів є змінною
    if is_variable(literal1):
        return {literal1: literal2}
    if is_variable(literal2):
        return {literal2: literal1}

    # Якщо уніфікація неможлива
    return None


def is_variable(term):
    """
    Перевіряє, чи є терм змінною (змінні починаються з великої літери).
    """
    return term[0].isupper()


def apply_substitution(term, substitutions):
    """
    Застосовує підстановки до терма.
    """
    while term in substitutions:
        term = substitutions[term]
    return term


def input_disjuncts():
    """
    Введення диз’юнктів для уніфікації.
    """
    print("Введіть два диз’юнкти для уніфікації.")
    print("Диз’юнкти вводяться як списки літералів, розділених пробілом.")
    print("Наприклад: P(x) Q(y) R(z).")

    disjunct1 = input("Перший диз’юнкт: ").strip().split()
    disjunct2 = input("Другий диз’юнкт: ").strip().split()
    return set(disjunct1), set(disjunct2)


# Основна програма
print("Алгоритм уніфікації для пари диз’юнктів.\n")
disjunct1, disjunct2 = input_disjuncts()

result = unify(disjunct1, disjunct2)
if result is not None:
    print("\nУніфікація можлива. Підстановки:")
    for var, value in result.items():
        print(f"  {var} -> {value}")
else:
    print("\nУніфікація неможлива.")


# def input_disjuncts():
#     """
#     Введення диз’юнктів для уніфікації у форматі функцій.
#     """
#     print("Введіть два диз’юнкти для уніфікації.")
#     print("Диз’юнкти вводяться як списки літералів, розділених пробілом.")
#     print("Функції можна вводити у вигляді: P(a, x, f(g(y))).")
#
#     disjunct1 = input("Перший диз’юнкт: ").strip().split()
#     disjunct2 = input("Другий диз’юнкт: ").strip().split()
#     return set(disjunct1), set(disjunct2)
#
#
# # Основна програма
# print("Алгоритм уніфікації для пари диз’юнктів із функціями.\n")
# disjunct1, disjunct2 = input_disjuncts()
#
# result = unify(disjunct1, disjunct2)
# if result is not None:
#     print("\nУніфікація можлива. Підстановки:")
#     for var, value in result.items():
#         print(f"  {var} -> {value}")
# else:
#     print("\nУніфікація неможлива.")