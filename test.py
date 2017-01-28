from pydbg import *
from pydbg.defines import *

import struct

dbg = pydbg()

path_exe = "C:\\windows\\system32\\calc.exe"

dbg.load(path_exe, "-u amir")
dbg.debug_event_loop()

parameter_addr = dbg.context.Esp #(+ 0x8)

print 'ESP (address) ',parameter_addr
