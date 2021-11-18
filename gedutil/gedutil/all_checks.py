from gedutil import (  # Family,
    US01,
    US03,
    US05,
    US06,
    US07,
    US10,
    US12,
    US15,
    US16,
    US20,
    US22,
    US25,
    US29,
    US33,
    US37,
    Family,
)


def run_all():
    for cls in [
        US01,
        US03,
        US05,
        US06,
        US07,
        # Family,
        US10,
        US12,
        # US15,
        US16,
        US20,
        US22,
        US25,
        US29,
        US33,
        US37,
    ]:
        obj = cls()
        obj.run()
