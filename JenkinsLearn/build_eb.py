# 
# Wayland Additive Ltd Proprietary Information
# ==============================================
# 
# Copyright (c) Wayland Additive, 2016.
# ---------------------------------------
# 
# All rights reserved.
# No part of this software may be copied or disclosed
# without the prior permission of the copyright holder.
# 
# Written by David Knight
# www.knightgraphics.co.uk
# 
# Python imports
import os
import sys
import subprocess
import shutil
import argparse
import re

# Add parent folder to sys to import ev_sign if available 
from os.path import dirname, abspath
parent = dirname(dirname(abspath(__file__)))
p = os.path.abspath(parent)
sys.path.insert(1, p)

do_sign = True
try:
    import ev_sign
except ModuleNotFoundError:
    # If ev_sign does not exist do not sign
    do_sign = False
    
#
# This module builds the Wayland Build software.
#
nobuild = False       # TESTING
build_doc = False     # Build documentation
branch_name = "master"

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--nobuild', action='store_true', help='No build solution')                   
parser.add_argument('--build_doc', action='store_true', help='Generate Doxygen')
parser.add_argument('branch_name', help='Branch name for installer')

args = parser.parse_args()

nobuild = args.nobuild
build_doc = args.build_doc

if(args.branch_name != ""):
    branch_name = args.branch_name

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
log_file = open("build_eb.log", "a")



WaylandDir = os.environ['WAYLAND_BUILD']

# Step 0: get dep
# Get nuget packages for V8:
os.chdir('packages')
nuget = os.path.join(os.path.dirname(__file__), '../', 'nuget.exe') 
if not os.path.exists(nuget):
    print("Download nuget from nuget.org and copy it to root's parent folder first!")
    sys.exit(1)

# This should always be in sync with src\core\v8.pri
packages = [('v8.redist-v142-x64', '10.0.139.9'), ('v8-v142-x64', '10.0.139.9')]
for pack, pack_ver in packages:
    proc = subprocess.run (
        args = [nuget, 'install', pack, '-version', pack_ver],
        shell = True,
        universal_newlines = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    log_file.write(proc.stdout)
    log_file.write(proc.stderr)
os.chdir("..") 
pack_file = os.path.join(WaylandDir, 'packages', packages[0][0] + '.' + packages[0][1], 'lib', 'Release')
for file in os.listdir(pack_file):
    shutil.copy(os.path.join(pack_file, file), os.path.join(WaylandDir, 'bin'))


    
# Step 2a: regenerate vcxproj for GUI
if nobuild == False:
    qmake_bat = "generate_vcxproj.bat"
    print("Generating projects using qmake")
    proc = subprocess.run (
        args = [qmake_bat],
        shell = True,
        universal_newlines = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    log_file.write(proc.stdout)
    log_file.write(proc.stderr)
    if proc.returncode != 0:
        print("ERROR: build failed. See build_eb.log for details.")
        sys.exit(1)
# Step 2b: build eb.sln
    msbuild_exe = "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\MSBuild\\Current\\Bin\\MSBuild.exe"
    msbuild_target = "/t:Build" # "/t:Rebuild"
    msbuild_config = "/property:Configuration=Release"
    msbuild_platform = "/property:Platform=x64"
    msbuild_sln = "eb.sln"
    msbuild_args = "/m" # Enable parallel build
    print("Building " + msbuild_sln)
    proc = subprocess.run (
        args = [msbuild_exe, msbuild_sln, msbuild_target, msbuild_config, msbuild_platform, msbuild_args],
        universal_newlines = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    log_file.write(proc.stdout)
    log_file.write(proc.stderr)
    if proc.returncode != 0:
        print("ERROR: build failed with return code %d. See build_eb.log for details." % proc.returncode)
        sys.exit(1)

# Step 2c: digital sign binaries
    if do_sign:
        print("Signing with an EV Sectigo Code Signing Certificate")    
        fname=("^(Wayland|eb|gui|wab).*(exe|dll)$") # starts with Wayland, eb, gui or wab, and ends with exe or dll
        dirname = "bin"        # in bin folder        
        for files in os.listdir(dirname):
            if re.search(fname, files, re.IGNORECASE):
                ev_sign.sign(dirname + '/' + files, log_file)


# Step 3a: Generate configs
#config_bat = "create_configs.bat"
#print("Generating machine configurations")
#proc = subprocess.run (
#    args = [config_bat],
#    shell = True,
#    universal_newlines = True,
#    stdout = subprocess.PIPE,
#    stderr = subprocess.PIPE
#)
#log_file.write(proc.stdout)
#log_file.write(proc.stderr)
#if proc.returncode != 0:
#    print("ERROR: build failed. See build_eb.log for details.")
#    sys.exit(1)

# Step 4a: Generate automatic documentation, non optional as it should be quick
create_doc = "create_doc.bat"
print("Generate automatic documentation")
proc = subprocess.run (
    args = [create_doc],
    shell = True,
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)
log_file.write(proc.stdout)
log_file.write(proc.stderr)
if proc.returncode != 0:
    print("ERROR: build failed. See build_eb.log for details.")
    sys.exit(1)
    
# Step 4b: Build documentation, optional
if build_doc:
    print("Building documentation")
    os.chdir("doc") # Need to be in doc as Doxygen has relative paths
    doxy_exe = "C:\\Program Files\\doxygen\\bin\\doxygen"
    doxy_file = "eb.dox"
    proc = subprocess.run (
        args = [doxy_exe, doxy_file],
        universal_newlines = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    log_file.write(proc.stdout)
    log_file.write(proc.stderr)
    os.chdir("..") # back to main directory

    # eb.exe is not supported, an alternative method to export commands is needed
    # # Generate commands help
    # eb_exe = "bin\\eb.exe"
    # eb_args = "export table -filename doc\\commands.html -table commands -sort system"
    # proc = subprocess.run (
    #     args = [eb_exe, eb_args],
    #     universal_newlines = True,
    #     stdout = subprocess.PIPE,
    #     stderr = subprocess.PIPE
    # )
    # log_file.write(proc.stdout)
    # log_file.write(proc.stderr)

#
### TEMPORARILIY IGNORE RC. See https://github.com/AndyMcC0/EB-Software/issues/234
#
#if proc.returncode != 0:
#    print("ERROR: build failed with return code %d. See build_eb.log for details." % proc.returncode)
#    sys.exit(1)
#
# Step 4b: Get Qt depends

print("Gathering Qt dependencies")

dir_WaylandView_bin = "install\\bin\\WaylandView_bin"
dir_WaylandTechnix_bin = "install\\bin\\WaylandTechnix_bin"
dir_WaylandRecover_bin = "install\\bin\\WaylandRecover_bin"
dir_WaylandBuild_bin = "install\\bin\\WaylandBuild_bin"
dir_WaylandPrep_bin = "install\\bin\\WaylandPrep_bin"
dir_WaylandImgConv_bin = "install\\bin\\WaylandImgConv_bin"

app_dirs = (dir_WaylandView_bin, dir_WaylandTechnix_bin, dir_WaylandPrep_bin,
            dir_WaylandRecover_bin, dir_WaylandBuild_bin, dir_WaylandImgConv_bin)

InstalltionDir = os.path.join(WaylandDir, "")

# VCINSTALLDIR used by windeployqt to extracts Visual C++ Redistributable Packages like "vc_redist.x64.exe"
try:
    result = subprocess.run([r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe", "-latest", "-property", "installationPath"], capture_output=True)
    os.environ['VCINSTALLDIR'] = result.stdout.decode('ascii').splitlines()[0] + r'\VC'
except:
    print("Error while getting Visual Studio path")

print("Removing existing dirs")
for dir in app_dirs:
  if os.path.exists(dir):
    shutil.rmtree(dir)

dir_common_bin = "install\\bin\\WaylandCommon_bin"

if os.path.exists(dir_common_bin):
  shutil.rmtree(dir_common_bin)
os.mkdir(dir_common_bin)

print("Gathering Qt dependencies")
qt_exe = "windeployqt"

proc = subprocess.run (
    args = [qt_exe, "bin\\WaylandPrep.exe", "--release", "--no-translations",  "--dir", dir_WaylandPrep_bin],
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

print(proc.stdout)
print(proc.stderr)

proc = subprocess.run (
    args = [qt_exe, "bin\\WaylandBuild.exe", "--release", "--no-translations", "bin\\gui_hmi.dll", "--qmldir", "src\\gui\\gui_system\\gui_hmi", "--dir", dir_WaylandBuild_bin],
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

print(proc.stdout)
print(proc.stderr)

proc = subprocess.run (
    args = [qt_exe, "bin\\WaylandImgConv.exe", "--release", "--no-translations",  "--dir", dir_WaylandImgConv_bin],
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

print(proc.stdout)
print(proc.stderr)

proc = subprocess.run (
    args = [qt_exe, "bin\\WaylandRecover.exe", "--release", "--no-translations",  "--dir", dir_WaylandRecover_bin],
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

print(proc.stdout)
print(proc.stderr)

proc = subprocess.run (
    args = [qt_exe, "bin\\WaylandTechnix.exe", "--release", "--no-translations",  "--dir", dir_WaylandTechnix_bin],
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

print(proc.stdout)
print(proc.stderr)

proc = subprocess.run (
    args = [qt_exe, "bin\\WaylandView.exe", "--release", "--no-translations", "--qmldir", "src\\gui\\WaylandView\\qml", "--dir", dir_WaylandView_bin],
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

print(proc.stdout)
print(proc.stderr)

print("Removing duplicats")

if (len(app_dirs) > 1):

    print(" - Copy common items")
    # get common items
    common = os.listdir(app_dirs[0])
    for dir in app_dirs[1:]:
        common = [value for value in common if value in os.listdir(dir)]

    # copy common items to separate dir
    for item in common:
        src = os.path.join(InstalltionDir , app_dirs[0], item)
        dst = os.path.join(InstalltionDir , dir_common_bin, item)

        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)

    print(" - remove common items from others dirs")

    # remove common items form all dirs
    for dir in app_dirs:
        for item in common:
            delItem = os.path.join(InstalltionDir , dir, item)
            if os.path.isdir(delItem):
                shutil.rmtree(delItem)
            else:
                os.remove(delItem)

#
# Step 5a: Build Qt installer   
print("Building installer (Qt)")
proc = subprocess.run (
    args = ["python", "install\\qt_installer.py", branch_name, "qt5"],
    universal_newlines = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

log_file.write(proc.stdout)
log_file.write(proc.stderr)

if proc.returncode != 0:
    print("Installer failure in qt_installer")
    sys.exit(2)
    
# Step 5b: digital sign installers 
if do_sign:
    print("Signing with an EV Sectigo Code Signing Certificate, installers")
    ext = ('.exe')       # sign all exe files
    dirname = "install"  # in install folder
    for files in os.listdir(dirname):
        if files.endswith(ext):
            ev_sign.sign(dirname + '/' + files, log_file)
            
print("DONE. See build_eb.log for details.")
