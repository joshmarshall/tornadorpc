import unittest
from tests.utils import *
import sys
    
if __name__ == "__main__":
    if '--json' in sys.argv:
        sys.argv.pop(sys.argv.index('--json'))
        from tests.json import *
    else:
        from tests.xml import *
        
    unittest.main()
