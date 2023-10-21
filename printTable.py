from rich import print
from rich import table


def display(struct: dict = {}) -> None:
    if not struct == {}:
        tableformat = table.Table()
        for column in struct['columns']:
            tableformat.add_column(column)
        for row in struct['rows']:
            tableformat.add_row(*row)
        
        print(tableformat)