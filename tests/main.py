from loguru import logger

from gedutil import Parser, Tabular_Output

from path_util import stabilize


@logger.catch
def main():
    parser = Parser(stabilize("", "main/control.ged"))
    parser.read()
    parser.parse()
    # parser.print_input_output_project_2_assignment()
    t = Tabular_Output()
    t.print_individuals()
    t.print_families()


if __name__ == "__main__":
    main()
