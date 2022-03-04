
# -----------------------------------
# Studio Library
# www.studiolibrary.com
# -----------------------------------

import os
import sys
    
if not os.path.exists(r'C:\Users\punit.girdhar\Documents\maya\2017\scripts\studiolibrary\src'):
    raise IOError(r'The source path "C:\Users\punit.girdhar\Documents\maya\2017\scripts\studiolibrary\src" does not exist!')
    
if r'C:\Users\punit.girdhar\Documents\maya\2017\scripts\studiolibrary\src' not in sys.path:
    sys.path.insert(0, r'C:\Users\punit.girdhar\Documents\maya\2017\scripts\studiolibrary\src')
    
import studiolibrary
studiolibrary.main()
