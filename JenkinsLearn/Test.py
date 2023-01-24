import argparse
import os

#
# This module builds the Wayland Build software.
#
nobuild = False       # TESTING
increment_ver = False # increment version
build_doc = False     # Build documentation
branch_name = "master"

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--nobuild', action='store_true', help='No build solution')                   
parser.add_argument('--increment_ver', action='store_true', help='Increment version')
parser.add_argument('--build_doc', action='store_true', help='Generate Doxygen')
parser.add_argument('--branch_name', help='Branch name for installer')

args = parser.parse_args()

nobuild = args.nobuild
increment_ver = args.increment_ver
build_doc = args.build_doc

os.system('echo increment_ver = {} , build_doc = {}> Hi.txt'.format(increment_ver,build_doc))