import os
import re
import string

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from sympy import Poly
from sympy.solvers import solve

console = Console()

alphabet_string = string.ascii_lowercase
alphabet_list = list(alphabet_string)


# utility functions
def clear():
    os.system('clear')


def c_input(message, type_conversion_function=str):
    while True:
        console.print(message)
        print("\n----")
        try:
            value = type_conversion_function(input())
            clear()
            return value
        except ValueError as e:
            clear()
            console.print("You entered something wrong!\n", style="bold red")


def evaluate(x, formula):
    new_formula = list(formula)

    for index, char in enumerate(new_formula, start=0):
        if char.isalpha():
            new_formula[index] = 'x'

    return eval("".join(new_formula))


def stringify_table(table):
    string_table = []

    for row in table:
        string_table_values = {}
        for key, value in row.items():
            string_table_values[str(key)] = str(value)
        string_table.append(string_table_values)

    return string_table


def print_table(table):
    t = Table()

    string_table = stringify_table(table)

    # add columns
    for column in table[0].keys():
        t.add_column(column)

    # add rows
    for row in string_table:
        t.add_row(*row.values())

    # print table
    console.print(t)


def bisection_and_newton_input():
    period = []
    for index in range(2):
        period.append(c_input(
            Markdown(f"Enter an integer number for the the {'starting' if index == 0 else 'ending'} period:"), int))
    approximation_error = c_input(Markdown("Enter the approximation error:"), float)
    formula = c_input(Markdown("Enter the formula you want to find the root of:"))
    return period, approximation_error, formula


def split_formula_into_terms(formula):
    return remove_space(re.split(r"([+ |\-=])", formula.replace(' ', '')))


def remove_space(some_list):
    while True:
        if '' in some_list:
            some_list.remove('')
        else:
            return some_list


def make_linear(formula):
    new_formula = formula.copy()

    for index, term in enumerate(new_formula, start=0):
        if term not in ['-', '+', '=']:
            new_formula[index] = f'+({term})'

    if "=" in formula:
        other_side_index = new_formula.index('=') + 1
        equal_sign_index = new_formula.index('=')
        # move all terms to the other side
        for index, term in enumerate(new_formula, start=0):
            if index == other_side_index:
                if term not in ['+', '-']:
                    if '-' in term:
                        term = term.replace('-', '+')
                    if '+' in term:
                        term = term.replace('+', '-')

                    new_formula.insert(equal_sign_index, '+')
                    equal_sign_index += 1
                    other_side_index += 1

                new_formula.insert(equal_sign_index, term)
                equal_sign_index += 1
                other_side_index += 1

                del new_formula[other_side_index]
        del new_formula[equal_sign_index]

    return "".join(new_formula)


def remove_duplicates(test_list):
    new_list = []
    for index in test_list:
        if index not in new_list:
            new_list.append(index)

    return new_list


def get_system_variables(system):
    variables = []

    for formula in system:
        if len(variables) < len(remove_duplicates(re.findall('[a-z]+', formula))):
            variables = remove_duplicates(re.findall('[a-z]+', formula))

    return variables


def guass_seidel_and_jacobi_input():
    system_size = c_input(Markdown("Enter the equation system size"), int) or 3
    approximation_error = c_input(Markdown(f"Enter the approximation error: "), float)

    system = []
    s_values = []

    for index in range(system_size):
        system.append(c_input(Markdown(f"Enter equation number {index + 1}:")))

    for variable in get_system_variables(system):
        s_values.append(c_input(Markdown(f"Enter the starting value of {variable}:"), float))

    return system_size, system, s_values, approximation_error


def convert_to_aplha(formula):
    memory = {}
    new_formula = []
    for char in formula:
        if char.isalpha():
            if char not in memory.keys():
                add_variable(memory, char)
            char = memory[char]
        new_formula.append(char)

    return ''.join(new_formula)


def add_variable(memory, name):
    for letter in alphabet_list:
        if letter not in memory.values():
            memory[name] = letter
            break


def order_system(system):
    ordered_system = []
    system_variables = get_system_variables(system)

    for v_index, variable in enumerate(system_variables, start=0):
        value_list = {}

        for f_index, formula in enumerate(system, start=0):
            if formula not in ordered_system:
                poly = Poly(formula)
                value_list[f_index] = poly.coeffs()[v_index]

        index, _ = largest_in_dict(value_list, ordered_system)
        ordered_system.append(system[index])

    return ordered_system


def populate_formula(formula, variables, values, skip_index=0):
    populated_formula = ''

    for v_index, variable in enumerate(variables):
        if v_index != skip_index:
            populated_formula = formula.replace(variable, str(values[v_index]))
            formula = populated_formula

    return populated_formula


def solve_system(ordered_system, values):
    solution = []
    variables = get_system_variables(ordered_system)

    for f_index, formula in enumerate(ordered_system):
        solution.append(float(solve(populate_formula(formula, variables, values, f_index))[0]))

    return solution


def largest_in_dict(v_dict, ordered_system):
    largest = float('-inf')
    index = None

    for key, value in v_dict.items():
        if value > largest:
            largest = value
            index = key

    return index, largest
