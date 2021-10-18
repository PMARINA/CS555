DEBUG_IMPORTS = False
if DEBUG_IMPORTS:  # pragma: no cover
    print("hit GED_Parse/init")

# Imports for testing (user stories)

from .base import ID, GED_Line, GED_Tag
from .checks.us01 import US01
from .checks.us03 import US03
from .checks.us05 import US05
from .checks.us06 import US06
from .checks.us08 import Family
from .checks.us10 import US10
from .checks.us12 import US12
from .checks.us15 import US15
from .checks.us16 import US16
from .checks.us20 import US20
from .checks.us22 import US22
from .checks.us25 import US25
from .checks.us29 import US29
from .checks.us33 import US33
from .checks.us37 import US37
from .parser import Parser
from .tabular_output import Tabular_Output

# Important base imports for general use
# from .mongo_client import families, individuals
