"""
rigspec.py
Created: Thursday, 14th September 2023 10:13:03 am
Matthew Riche
Last Modified: Thursday, 14th September 2023 10:13:29 am
Modified By: Matthew Riche
"""

# Example rigspic statement.
# placer:(x, y, z), local, pa, sa, cl, sz, p
from .console import dprint
from . import placer


class Expression:
    valid_commands = ["placer"]

    def __init__(self, expression: str):
        """Takes a string of rigspec code and parses it.

        Args:
            expression (str): The rigspec expression.
        """
        self.unparsed_expression = expression
        self.command_type = None
        self.args = None

        self.parse_command()
        self.parse_arguments()
        self.cast_arguments()
        dprint(f"Expression Argument Data is:\n\t{self.args}")
            

    def parse_command(self):
        """Determines what command is called.

        Raises:
            SyntaxError: If there's no ':' separator.
            NameError: If the command doesn't exist.
        """
        dprint(f"Parsing: {self.unparsed_expression}")

        if ":" not in self.unparsed_expression:
            raise SyntaxError(f"Expected ':' in statement {self.unparsed_expression}")
        else:
            command = self.unparsed_expression.split(":")[0]

        if command not in Expression.valid_commands:
            raise NameError(f"{command} isn't a recognized rigspec command.")

        dprint(f"Parsed command as a valid '{command}' command.")
        self.command_type = command

    def parse_arguments(self):
        """Builds a dictionary of arguments.

        Raises:
            SyntaxError: If command isn't delimeted by a ':'
            SyntaxError:
        """
        if ":" not in self.unparsed_expression:
            raise SyntaxError(f"Expected ':' in statement {self.unparsed_expression}")
        else:
            # Split args from command by ':', then split by comma, then sanitize spaces.
            arguments_str = self.unparsed_expression.split(":")[-1]

            # To make this simpler, we are going to change , to '|' if they aren't in parens.
            # Also guard against mismatched parenthesis.
            in_parens = 0
            for i in range(len(arguments_str)):
                if arguments_str[i] == "(":
                    in_parens += 1
                elif arguments_str[i] == ")":
                    if in_parens == 0:
                        raise SyntaxError(
                            f'Mismatched parens in "{self.unparsed_expression}"'
                        )
                    in_parens -= 1
                elif arguments_str[i] == ",":
                    if in_parens == 0:
                        arguments_str = arguments_str[:i] + "|" + arguments_str[i + 1 :]

            arguments = arguments_str.split("|")
            arguments = [arg.replace(" ", "") for arg in arguments]

            # Convert this into a dict:
            arg_data = {}
            for arg in arguments:
                if "=" not in arg:
                    raise SyntaxError(f"Expected '=', but got '{arg}'.")
                attr, value = arg.split("=")
                arg_data[attr] = value

            self.args = arg_data

    def cast_arguments(self):
        # This is for turning all that string data into tuples, numbers, etc.
        if self.args is None:
            raise ValueError("Can't cast args before they've been parsed yet.")

        for i in self.args:
            arg = self.args[i]
            if "(" in arg:
                # Remove parens and spaces, then cast the delimeted strings to floats.
                numbers = arg.replace("(", "").replace(")", "").replace(" ", "")
                arg = [float(n) for n in numbers.split(",")]
                arg = tuple(arg)
                self.args[i] = arg

            elif arg.replace(".", "").isdigit():
                # If there are numbers only, we check for a . or not and cast as float or int.
                if "." in arg:
                    arg = float(arg)
                    self.args[i] = arg
                else:
                    arg = int(arg)
                    self.args[i] = arg



def run_parsed_expression(expression: Expression):
    if isinstance(expression, Expression) == False:
        raise TypeError(f"Parameter {expression} is not a rigspec.Expression.")

    if expression.command_type is None or expression.args is None:
        raise ValueError(f"Expression doesn't appear to be parsed yet.")

    if expression.command_type == "placer":
        new_placer = placer.Placer()
