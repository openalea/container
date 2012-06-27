# -*- coding: utf-8 -*-
__revision__ = "$Id$"

# Setup script has been commented to ease the writing of your own file. 

# A setup script mainly consist of a call to the setup function of setuptool, that allows to create a distribution archive of a set of python modules grouped in packages (ie in directories with an __init__.py file).
# In the context of OpenAlea, this function has been extended by the openalea.deploy module to ease the simultaneaous distribution of binaries and libraries.

# (To adapt this script for your package, you mainly have to change the content of the variable defined before the call to setup function, and comment out unused options in the call of the function)

import sys
import os

from setuptools import setup, find_packages


# Meta information
# (used to construct egg infos)

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))



pkg_root_dir = 'src'
pkgs = [ pkg for pkg in find_packages(pkg_root_dir) if namespace not in pkg]
top_pkgs = [pkg for pkg in pkgs if  len(pkg.split('.')) < 2]
packages = [ namespace + "." + pkg for pkg in pkgs]
package_dir = dict( [('',pkg_root_dir)] + [(namespace + "." + pkg, pkg_root_dir + "/" + pkg) for pkg in top_pkgs] )


share_dirs = {'share':'share'}

# List of top level wralea packages (directories with __wralea__.py) 
# (to be kept only if you have visual components)
wralea_entry_points = ['container.mesh = openalea.container.wralea.mesh']






# dependencies to other eggs
# (This is used by deploy to automatically downloads eggs during the installation of your package)
# (allows 'one click' installation for windows user)
# (linux users generally want to void this behaviour and will use the dependance list of your documentation)
# (dependance to deploy is mandatory for runing this script)
setup_requires = ['openalea.deploy']
if("win32" in sys.platform):
    install_requires = []
else:
    install_requires = []
# web sites where to find eggs
dependency_links = ['http://openalea.gforge.inria.fr/pi']


# scons build-prefix 
#(to be kept only if you contruct C/C++ binaries)

build_prefix = "build-scons"



# setup function call
#
setup(
    # Meta data (no edition needed if you correctly defined the variables above)
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    keywords = '',
    # package installation
    packages= packages,
    package_dir= package_dir,
    # Namespace packages creation by deploy
    namespace_packages = [namespace],
    create_namespaces = True,
    # tell setup not  tocreate a zip file but install the egg as a directory (recomended to be set to False)
    zip_safe= False,
    # Dependencies
    setup_requires = setup_requires,
    install_requires = install_requires,
    dependency_links = dependency_links,


    # Binary installation (if necessary)
    # Define what to execute with scons 
    #scons_scripts=['SConstruct'],
    # Tell deploy where to find libs, includes and bins generated by scons.
    #lib_dirs = {'lib' : build_prefix+'/lib' },
    #inc_dirs = { 'include' : build_prefix+'/include' },
    #bin_dirs = { 'bin' : build_prefix+'/bin' },

    # Eventually include data in your package
    # (flowing is to include all versioned files other than .py)
    include_package_data = True,
    # (you can provide an exclusion dictionary named exclude_package_data to remove parasites).
    # alternatively to global inclusion, list the file to include   
    package_data = {'' : ['*.pyd', '*.so', '*.zip', '*.png'],},

    # postinstall_scripts = ['',],

    # Declare scripts and wralea as entry_points (extensions) of your package 
    entry_points = {
            'wralea': wralea_entry_points
        },

    pylint_packages = ['src/container', 'src/container/backend', 'src/container/utils', 'src/container/generator', 'src/openalea/iterator', 'src/openalea/traversal']

    )

