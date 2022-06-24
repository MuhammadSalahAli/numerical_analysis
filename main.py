from rich.console import Console
from rich.markdown import Markdown

from methods.bisection import bisection
from methods.gauss_seidel import gauss_seidel
from methods.newton_raphson import newton_raphson

from methods.utils import c_input

console = Console()

methods = {
    1: bisection,
    2: newton_raphson,
    3: gauss_seidel,
}


class ChoiceDoesNotExist(Exception):
    def __init__(self, message="The choice you selected is not in the list"):
        self.message = message
        super().__init__(self.message)


def main():
    while True:
        try:
            choice = c_input(Markdown("# Select one of the equation types below:\n"
                                      "\n1. bisection method.  \n2. newton raphson method. \n3. gauss seidel method."
                                      "\n 4. exit."), int)
            if choice == 4:
                break
            elif choice > 4:
                raise ChoiceDoesNotExist

            methods[choice]()

            choice = c_input("continue ? y/n")

            if choice.lower() == 'n' or choice.lower() == 'no':
                break
            elif choice.lower() not in ['n', 'y']:
                raise ChoiceDoesNotExist

        except ChoiceDoesNotExist as e:
            console.print(e.message, style="bold red")

        except:
            console.print("The equation you typed was wrong!\n", style="bold red")

if __name__ == '__main__':
    main()
