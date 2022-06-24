from .utils import bisection_and_newton_input, print_table, evaluate


def bisection():
    # problem inputs
    period, approximation_error, formula = bisection_and_newton_input()

    # solution values
    a = period[0]
    b = period[1]
    root = (a + b) / 2
    f_a = evaluate(a, formula)
    f_r = evaluate(root, formula)
    index = 0
    table = [{'index': index + 1, 'a': a, 'b': b, 'root': root, 'f(a)': f_a, 'f(r)': f_r}]

    while True:
        index += 1
        if ((f_a == f_r) and (f_a == 0)) or (f_a * f_r > 0):
            a = root
        else:
            b = root

        root = (a + b) / 2
        f_a = evaluate(a, formula)
        f_r = evaluate(root, formula)

        table.append({'index': index + 1, 'a': a, 'b': b, 'root': root, 'f(a)': evaluate(a, formula),
                      'f(r)': evaluate(root, formula)})

        if abs(table[index]['root'] - table[index - 1]['root']) <= approximation_error:
            print_table(table)
            break
