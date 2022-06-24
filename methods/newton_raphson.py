from .utils import bisection_and_newton_input, evaluate, print_table
from sympy import Derivative


def newton_raphson():
    # problem inputs
    period, approximation_error, formula = bisection_and_newton_input()
    deravative_formula = str(Derivative(formula).doit())

    # solution variables
    x = (period[0] + period[1]) / 2
    f_xi = evaluate(x, formula)
    f_prime_xi = evaluate(x, deravative_formula)
    xi_plus_1 = x - (f_xi / f_prime_xi)
    index = 0
    table = [{'index': index + 1, 'xi': x, 'f(xi)': f_xi, "f'(xi)": f_prime_xi, "xi+1": xi_plus_1}]

    while True:
        index += 1
        x = xi_plus_1
        f_xi = evaluate(x, formula)
        f_prime_xi = evaluate(x, deravative_formula)
        xi_plus_1 = x - (f_xi / f_prime_xi)
        table.append({'index': index + 1, 'xi': x, 'f(xi)': f_xi, "f'(xi)": f_prime_xi, "xi+1": xi_plus_1})

        if abs(xi_plus_1 - x) <= approximation_error:
            print_table(table)
            break
