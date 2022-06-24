from .utils import (guass_seidel_and_jacobi_input, make_linear, split_formula_into_terms, convert_to_aplha,
                    order_system, solve_system, print_table)


def test_condition(matrix_a, matrix_b, error_rate):
    new_matrix = []

    for index, element in enumerate(matrix_a, start=0):
        new_matrix.append(matrix_b[index] - matrix_a[index])

    return max(new_matrix) >= error_rate


def gauss_seidel():
    system_size, system, s_values, approximation_error = guass_seidel_and_jacobi_input()

    alpha_system = []
    for formula in system:
        alpha_system.append(convert_to_aplha(formula))

    linear_system = []
    for formula in alpha_system:
        linear_system.append(make_linear(split_formula_into_terms(formula)))

    ordered_system = order_system(linear_system)

    index = 0
    table = [{'index': index + 1, 'value': s_values}]

    while True:
        index += 1
        s_values = solve_system(ordered_system, s_values)
        table.append({'index': index + 1, 'value': s_values})

        if test_condition(table[index - 1]['value'], s_values, approximation_error):
            print_table(table)
            break
