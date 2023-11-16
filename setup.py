# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

#!/usr/bin/env python

import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/compass-legacy-visits>`_.
"""

version_path = 'visits/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='compass-legacy-visits',
    version=VERSION,
    packages=['visits'],
    include_package_data=True,
    install_requires = [
        'pyodbc<5',
        'pandas~=1.1',
        'urllib3~=1.25',
        'requests',
        'commonconf',
        'pymssql==2.2.2',
        'axdd-person-client>=1.1.18',
    ],
    license='Apache License, Version 2.0',
    description='Collects Instruction Center Visit data',
    long_description=README,
    url='https://github.com/uw-it-aca/compass-legacy-visits',
    author = "UW-IT AXDD",
    author_email = "aca-it@uw.edu",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
