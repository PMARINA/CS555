from loguru import logger

from gedutil import Parser, Tabular_Output, run_all_checks

if __name__ == "__main__":
    from path_util import stabilize
else:
    from .path_util import stabilize


@logger.catch
def main():
    parser = Parser(stabilize("US", "all.ged"))
    parser.read()
    parser.parse()
    run_all_checks()
    # parser.print_input_output_project_2_assignment()
    t = Tabular_Output()
    t.print_individuals()
    t.print_families()
    t.print_outputs()


if __name__ == "__main__":
    main()
