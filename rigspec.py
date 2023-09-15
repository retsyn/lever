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
            arguments = arguments_str.split(",")
            arguments = [arg.replace(" ", "") for arg in arguments]
            dprint(f"Arguments are: {arguments}")

            # Convert this into a dict:
            arg_data = {}
            for arg in arguments:
                if "=" not in arg:
                    raise SyntaxError(f"Expected '=', but got '{arg}'.")
                attr, value = arg.split("=")
                arg_data[attr] = value

            dprint(f"Argument Data: {arg_data}")
            self.args = arg_data

    def cast_arguments(self):
        # This is for turning all that string data into tuples, numbers, etc.
        pass




def run_parsed_expression(expression: Expression):
    if(isinstance(expression, Expression) == False):
        raise TypeError(f"Parameter {expression} is not a rigspec.Expression.")
    
    if(expression.command_type is None or expression.args is None):
        raise ValueError(f"Expression doesn't appear to be parsed yet.")
    
    if(expression.command_type == 'placer'):
        new_placer = placer.Placer()


    
