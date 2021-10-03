from loguru import logger

from gedutil import Parser


@logger.catch
def main():
    parser = Parser("input_files/US01/control.ged")
    parser.read()
    parser.parse()
    # parser.print_input_output_project_2_assignment()


if __name__ == "__main__":
    main()
