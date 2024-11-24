# def resolution_algorithm(clauses):
#     """
#     Виконання алгоритму резолюції для перевірки виконуванності множини диз’юнктів
#     """
#     new_clauses = set(frozenset(clause) for clause in clauses)  # Початкова множина диз’юнктів
#     print("Початкова множина диз’юнктів:")
#     for clause in new_clauses:
#         print(f"  {set(clause)}")
#     print()
#
#     step = 1
#     while True:
#         # Отримати всі можливі пари диз’юнктів
#         pairs = [(ci, cj) for ci in new_clauses for cj in new_clauses if ci != cj]
#         resolved = set()
#
#         print(f"Крок {step}: перевіряємо всі пари диз’юнктів...")
#         for (ci, cj) in pairs:
#             print(f"  Резолюція: {set(ci)} і {set(cj)}")
#             # Спроба застосувати резолюцію
#             resolvent = resolve(ci, cj)
#             if resolvent is None:
#                 print("    Неможливо застосувати резолюцію.")
#                 continue
#             print(f"    Отримано новий диз’юнкт: {set(resolvent)}")
#             if not resolvent:  # Якщо порожній диз’юнкт
#                 print("\nЗнайдено порожній диз’юнкт! Множина диз’юнктів є невиконуваною.\n")
#                 return False
#             resolved.add(frozenset(resolvent))
#
#         # Якщо нових диз’юнктів не з'явилось, множина виконувана
#         if resolved.issubset(new_clauses):
#             print("\nНових диз’юнктів не знайдено. Множина диз’юнктів є виконуваною.\n")
#             return True
#
#         # Оновлюємо множину диз’юнктів
#         new_clauses.update(resolved)
#         print("Оновлена множина диз’юнктів:")
#         for clause in new_clauses:
#             print(f"  {set(clause)}")
#         print()
#         step += 1
#
#
# def resolve(clause1, clause2):
#     """
#     Спроба виконати резолюцію між двома диз’юнктами.
#     """
#     for literal in clause1:
#         if negate_literal(literal) in clause2:
#             # Формуємо новий диз’юнкт, виключаючи суперечливі літерали
#             resolvent = (clause1 - {literal}) | (clause2 - {negate_literal(literal)})
#             return resolvent
#     return None
#
#
# def negate_literal(literal):
#     """
#     Заперечення літерала: якщо він заперечений, повернути незаперечений, і навпаки.
#     """
#     if literal.startswith("~"):
#         return literal[1:]  # Прибираємо "~", якщо це заперечення
#     else:
#         return "~" + literal  # Додаємо "~", якщо це незаперечений літерал
#
#
# def input_clauses():
#     """
#     Введення множини диз’юнктів користувачем із підтримкою диз’юнкції, кон’юнкції, імплікації та заперечення.
#     """
#     print("Введіть множину диз’юнктів або логічних формул.")
#     print("Для введення використовуйте наступний синтаксис:")
#     print("  - Диз’юнкція: p q (еквівалентно p ∨ q)")
#     print("  - Кон’юнкція: p & q (еквівалентно p ∧ q)")
#     print("  - Імплікація: p -> q (еквівалентно p → q)")
#     print("  - Заперечення: ~p (еквівалентно ¬p)")
#     print("Введіть порожній рядок, щоб завершити.")
#
#     clauses = []
#     while True:
#         line = input("Логічна формула: ").strip()
#         if not line:  # Порожній рядок завершує введення
#             break
#         clause = parse_formula(line)
#         if clause is None:
#             print("Неправильний формат формули. Повторіть введення.")
#         else:
#             clauses.append(clause)
#     return clauses
#
#
# def parse_formula(formula):
#     """
#     Розбір формули у форматі диз’юнктів, кон’юнкцій, імплікацій і заперечень.
#     """
#     # Перевірка на використання цифр у літералах
#     for token in formula.replace("~", "").replace("->", "").replace("&", "").split():
#         if token.isdigit():
#             print(f"Літерал '{token}' не може бути числом.")
#             return None
#
#     # Перевірка і розбір формули
#     if "->" in formula:  # Імплікація
#         parts = formula.split("->")
#         antecedent = parts[0].strip()
#         consequent = parts[1].strip()
#         # Імплікація A -> B перетворюється на ~A ∨ B
#         return {negate_literal(antecedent), consequent}
#     elif "&" in formula:  # Кон’юнкція
#         parts = formula.split("&")
#         return [{part.strip()} for part in parts]  # Кожен терм окремо
#     else:  # Диз’юнкція або одиничний терм
#         return set(formula.split())  # Просто набір літералів
#
#
# def negate_literal(literal):
#     """
#     Заперечення літерала: якщо він заперечений, повернути незаперечений, і навпаки.
#     """
#     literal = literal.strip()
#     if literal.startswith("~"):
#         return literal[1:]  # Прибираємо "~", якщо це заперечення
#     else:
#         return "~" + literal  # Додаємо "~", якщо це незаперечений літерал
#
#
# # Тестування
# clauses = input_clauses()
# print("\nВведені формули:")
# for clause in clauses:
#     print(clause)


def resolution_algorithm(clauses):
    """
    Виконання алгоритму резолюції для перевірки виконуванності множини диз’юнктів.
    """
    new_clauses = set(frozenset(clause) for clause in clauses)  # Початкова множина диз’юнктів
    print("\nПочаткова множина диз’юнктів:")
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
        print("\nОновлена множина диз’юнктів:")
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


def input_clauses():
    """
    Введення множини диз’юнктів користувачем із підтримкою диз’юнкції, кон’юнкції, імплікації та заперечення.
    """
    print("Введіть множину диз’юнктів або логічних формул.")
    print("Для введення використовуйте наступний синтаксис:")
    print("  - Диз’юнкція: p q (еквівалентно p ∨ q)")
    print("  - Кон’юнкція: p & q (еквівалентно p ∧ q)")
    print("  - Імплікація: p -> q (еквівалентно p → q)")
    print("  - Заперечення: ~p (еквівалентно ¬p)")
    print("Введіть порожній рядок, щоб завершити.")

    clauses = []
    while True:
        line = input("Логічна формула: ").strip()
        if not line:  # Порожній рядок завершує введення
            break
        clause = parse_formula(line)
        if clause is None:
            print("Неправильний формат формули. Повторіть введення.")
        else:
            if isinstance(clause, list):  # Якщо це кон’юнкція, додаємо кожен терм окремо
                clauses.extend(clause)
            else:
                clauses.append(clause)
    return clauses


def parse_formula(formula):
    """
    Розбір формули у форматі диз’юнктів, кон’юнкцій, імплікацій і заперечень.
    """
    # Перевірка на використання цифр у літералах
    for token in formula.replace("~", "").replace("->", "").replace("&", "").split():
        if token.isdigit():
            print(f"Літерал '{token}' не може бути числом.")
            return None

    # Перевірка і розбір формули
    if "->" in formula:  # Імплікація
        parts = formula.split("->")
        antecedent = parts[0].strip()
        consequent = parts[1].strip()
        # Імплікація A -> B перетворюється на ~A ∨ B
        return {negate_literal(antecedent), consequent}
    elif "&" in formula:  # Кон’юнкція
        parts = formula.split("&")
        return [{part.strip()} for part in parts]  # Кожен терм окремо
    else:  # Диз’юнкція або одиничний терм
        return set(formula.split())  # Просто набір літералів


# Основна програма

print("Алгоритм резолюції для перевірки виконуванності множини диз’юнктів.\n")
clauses = input_clauses()

print("\nВведені формули:")
for clause in clauses:
    print(clause)

result = resolution_algorithm(clauses)
if not result:
    print("Висновок: множина диз’юнктів є невиконуваною. Існує протиріччя.\n")
else:
    print("Висновок: множина диз’юнктів є виконуваною. Протиріччя відсутнє.\n")