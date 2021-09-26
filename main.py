from loguru import logger

import ged_parse


@logger.catch
def main():
    parser = ged_parse.GED_Parser("old/tests/custom/input.ged")
    parser.parse()
    parser.print_input_output_project_2_assignment()


if __name__ == "__main__":
    main()
