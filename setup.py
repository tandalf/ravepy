from __future__ import absolute_import, unicode_literals

from distutils.core import setup
setup(
name = 'ravepy',
packages = ['ravepy'],
version = '0.2.1',
description = 'Rave payment gateway client library for python',
author = 'Timothy Ebiuwhe',
author_email = 'timothy_ebiuwhe@live.com',
url = 'https://github.com/tandalf/ravepy',
download_url = 'https://github.com/tandalf/ravepy/archive/0.2.1.zip',
keywords = ['ravepy', 'Rave', 'Rave Pay', 'Rave Python Client', 'Rave Gateway',
    'Flutterwave Rave', 'python'],
classifiers = [],
install_requires=['requests', 'pycrypto']
)
