from BOOT_sector import *
from FAT_table import *
from ROOT_dir import *
from DATA_area import *
from decode_file import *

''' ----------- MAIN PROGRAM ----------- '''
''' Uncomment desired function to run it '''

BOOT_sector()
FAT_table()
ROOT_dir()
DATA_area()

''' ------------------------------------ '''

# TEST.TXT
# decode_file('544553542020202054585420184f93951e311e3100008c951e31fd000c000000')

# SYSTEM.DAT
# decode_file('e5595354454d20204441542018395b8f1e311e310000748e1e310401ed070000')