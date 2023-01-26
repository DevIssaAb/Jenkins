# 
# Reliance Precision Ltd Proprietary Information
# ==============================================
# 
# Copyright (c) Reliance Precision, 2016.
# ---------------------------------------
# 
# All rights reserved.
# No part of this software may be copied or disclosed
# without the prior permission of the copyright holder.
# 
# Written by David Knight
# www.knightgraphics.co.uk
# 
import os
import subprocess
import sys
from db.create_db import create_db
import argparse
import subprocess
from time import gmtime, strftime
################################################################################
# This module updates version numbers. The src/version.h is first scanned to
# determine the current version numbers, then the eb_version_bid is incremented
# and the file written back. The RC files are then also updated with the new
# version numbers.
################################################################################
def git_describe():
    proc = subprocess.run (
        args = 'git describe --long --all',
        universal_newlines = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    # Strip the trailing \n
    g = proc.stdout.replace("\n","")
    return g
    #
def update_version(filename, eb_wayland_version):
    eb_version_major = eb_wayland_version[0]
    eb_version_minor = eb_wayland_version[1]
    eb_version_bid = eb_wayland_version[2]
    eb_company_name = eb_wayland_version[3]
    eb_copyright = eb_wayland_version[4]
    eb_product_name = eb_wayland_version[5]
    print("Updating: " + filename)
    with open(filename, "r+") as f:
        lines = f.readlines()
    #
    with open(filename, "w") as f:    
        for line in lines:
            if "#define EB_VERSION_MAJOR" in line:
                eb_version_major = int(line.split(" ")[2])
                f.write(line)
            elif "#define EB_VERSION_MINOR" in line:
                eb_version_minor = int(line.split(" ")[2])
                f.write(line)
            elif "#define EB_COMPANYNAME_STR" in line:
                eb_company_name = line.split("\"")[1]
                f.write(line)
            elif "#define EB_LEGALCOPYRIGHT_STR" in line:
                eb_copyright = line.split("\"")[1]
                f.write(line)
            elif "#define EB_PRODUCTNAME_STR" in line:
                eb_product_name = line.split("\"")[1]
                f.write(line)
            elif "#define EB_VERSION_BID" in line:
                cols = line.split(" ")
                eb_version_bid = int(cols[2]) + 1
                newline = "#define EB_VERSION_BID " + str(eb_version_bid) + "\n"
                f.write(newline)
            elif "eb_version_git" in line:
                eb_version_git = git_describe()
                newline = 'static const std::string eb_version_git = "' + eb_version_git + '";\n'
                f.write(newline)
            else: 
                f.write(line)
    # 
    print("Updating version to: %d.%d.%d" % (eb_version_major, eb_version_minor, eb_version_bid))
    return (eb_version_major, eb_version_minor, eb_version_bid,eb_company_name,eb_copyright,eb_product_name)
    
def read_version(filename, eb_wayland_version):
    eb_version_major = eb_wayland_version[0]
    eb_version_minor = eb_wayland_version[1]
    eb_version_bid = eb_wayland_version[2]
    eb_company_name = eb_wayland_version[3]
    eb_copyright = eb_wayland_version[4]
    eb_product_name = eb_wayland_version[5]
    with open(filename, "r+") as f:
        lines = f.readlines()
    #    
    for line in lines:
        if "#define EB_VERSION_MAJOR" in line:
            eb_version_major = int(line.split(" ")[2])
        elif "#define EB_VERSION_MINOR" in line:
            eb_version_minor = int(line.split(" ")[2])
        elif "#define EB_COMPANYNAME_STR" in line:
            eb_company_name = line.split("\"")[1]
        elif "#define EB_LEGALCOPYRIGHT_STR" in line:
            eb_copyright = line.split("\"")[1]
        elif "#define EB_PRODUCTNAME_STR" in line:
            eb_product_name = line.split("\"")[1]
        elif "#define EB_VERSION_BID" in line:
            cols = line.split(" ")
            eb_version_bid = int(cols[2])
        elif "eb_version_git" in line:
            eb_version_git = git_describe()
    return (eb_version_major, eb_version_minor, eb_version_bid,eb_company_name,eb_copyright,eb_product_name)

    #
def update_pri(filename, eb_wayland_version):
    print("Updating PRI: " + filename)
    with open(filename, "w") as f:
        f.write("# Version file, included in .pro files.\n")
        f.write("# Microsoft resources. Used to create the .rc file.\n")
        f.write("# This file is automatically updated by update_versions.py and should not be edited manually.\n")
        f.write("VERSION = \"%d.%d.%d.0\"\n" % (eb_wayland_version[0:3]))
        f.write("QMAKE_TARGET_COMPANY = \"%s\"\n" % (eb_wayland_version[3]))
        f.write("QMAKE_TARGET_COPYRIGHT = \"%s\"\n" % (eb_wayland_version[4]))
        f.write("QMAKE_TARGET_PRODUCT = \"%s\"\n" % (eb_wayland_version[5]))
    #
def update_doc(filename, eb_wayland_version):
    print("Updating doc: " + filename)
    with open(filename, "r+") as f:
        lines = f.readlines()
    #
    with open(filename, "w") as f:    
        for line in lines:
            if "PROJECT_NUMBER" in line:
                newline = "PROJECT_NUMBER = %d.%d.%d\n" % (eb_wayland_version[0:3])
                f.write(newline)
            else: 
                f.write(line) 
    # 

def update_sql(filename, eb_wayland_version):
    ''' This needs to run before code compiled '''
    print("Updating: " + filename)
    with open(filename, "r+") as f:
        lines = f.readlines()
    #
    with open(filename, "w") as f:
        for line in lines:
            if "VALUES(\"version\"," in line:
                # Create a new empty key for the next version
                f.write("INSERT OR REPLACE INTO \"metadata\" VALUES(\"version\",\"%d.%d.%d\");\n" % (eb_wayland_version[0:3]))
            else:
                f.write(line)
                
# Update db. 
# This takes the SQL source, updates the version, and creates a .DB file from it.
# The SQL only contains the schema of the database and no records.
# The DB files should only be installed for new installations. 
# The output is placed into install/db so does not overwrite the current db.
def update_db(dbfile,sqlfile, eb_wayland_version):
    # Update the version
    update_sql(sqlfile, eb_wayland_version)
    # Create the db
    ret = create_db(sqlfile, dbfile)
    if ret > 0:
        print("ERROR: build failed with return code %d. See build_eb.log for details." % ret)
        return ret
    return 0
    
def generate_db():
    eb_wayland_version = (-1,-1,-1,-1,-1,-1)
    version_file = "src/core/eb_version.h"
    eb_wayland_version = read_version(version_file, eb_wayland_version)
    version_str = "%d.%d.%d" % (eb_wayland_version[0:3])
    version_file = open("version.log", "w")
    version_file.write(version_str)
    ret = update_db("install/db/eb_data.db", "src/sql/eb_data.sql", eb_wayland_version)
    if ret > 0:
        print("ERROR: build failed with return code %d. See build_eb.log for details." % ret)
        sys.exit(1)
    #
    ret = update_db("install/db/eb_pattern.db", "src/sql/eb_pattern.sql", eb_wayland_version)
    if ret > 0:
        print("ERROR: build failed with return code %d. See build_eb.log for details." % ret)
        sys.exit(1)
    #
    ret = update_db("install/db/eb_log.db", "src/sql/eb_log.sql", eb_wayland_version)
    if ret > 0:
        print("ERROR: build failed with return code %d. See build_eb.log for details." % ret)
        sys.exit(1)
    return eb_wayland_version
                
def main():
    eb_wayland_version = (-1,-1,-1,-1,-1,-1)
    print("Updating version numbers")
    version_file = "src/core/eb_version.h"
    eb_wayland_version = update_version(version_file, eb_wayland_version)
    version_str = "%d.%d.%d" % (eb_wayland_version[0:3])
    version_file = open("version.log", "w")
    version_file.write(version_str)
    
    # Update PRI file
    pri_file = "src/version.pri"
    update_pri(pri_file, eb_wayland_version)
    # Update doc
    update_doc("doc/eb.dox", eb_wayland_version)
    
    ret = update_db("install/db/eb_data.db", "src/sql/eb_data.sql", eb_wayland_version)
    if ret > 0:
        print("ERROR: build failed with return code %d. See build_eb.log for details." % ret)
        sys.exit(1)
    #
    ret = update_db("install/db/eb_pattern.db", "src/sql/eb_pattern.sql", eb_wayland_version)
    if ret > 0:
        print("ERROR: build failed with return code %d. See build_eb.log for details." % ret)
        sys.exit(1)
    #
    ret = update_db("install/db/eb_log.db", "src/sql/eb_log.sql", eb_wayland_version)
    if ret > 0:
        print("ERROR: build failed with return code %d. See build_eb.log for details." % ret)
        sys.exit(1)
    return eb_wayland_version

#
# This module builds the Wayland Build software.
#
nobuild = False       # TESTING
increment_ver = False # increment version


# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--nobuild', action='store_true', help='No build solution')                   
parser.add_argument('--increment_ver', action='store_true', help='Increment version')


args = parser.parse_args()

nobuild = args.nobuild
increment_ver = args.increment_ver



if nobuild:
    print("Skipping rebuild")
# Make sure that we are in WAYLAND_BUILD
eb_build = os.environ.get("WAYLAND_BUILD")
if eb_build == None:
    print("Environment variable WAYLAND_BUILD is not set. Cannot continue.")
    sys.exit(1)
#
os.chdir(eb_build)
# Open Log file to record build outputs
print("Building in directory: " + eb_build)
log_file = open("build_eb.log", "w")
log_file.truncate()
log_file.write("#################################################\n")
log_file.write("build_eb log file\n")
log_file.write("#################################################\n")
log_file.write("# time: " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
log_file.write("\n#################################################\n")
# Remove version log file
if os.path.exists("version.log"):
    os.remove("version.log")





# Step 1: update versions
# Version numbers
# Step 1a: Update databases.
# This means:
# 1. Updating the version in the SQL file
# 2. Creating the .db version
if increment_ver:
    eb_wayland_version=main()
    
    # Generating DV
    print("Generating DV")
    proc = subprocess.run (
    args = ["python", "generate_dv.py"],
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
    )
    log_file.write(proc.stdout)
    log_file.write(proc.stderr)
    if proc.returncode != 0:
        print("ERROR: build failed. See build_eb.log for details.")
        sys.exit(1)

    # Generating RC
    print("Generating RC")
    proc = subprocess.run (
    args = ["python", "generate_rc.py"],
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
    )
    log_file.write(proc.stdout)
    log_file.write(proc.stderr)
    if proc.returncode != 0:
        print("ERROR: build failed. See build_eb.log for details.")
        sys.exit(1)
    
else:
    eb_wayland_version=generate_db()

print("Updates version numbers done. See build_eb.log for details.")