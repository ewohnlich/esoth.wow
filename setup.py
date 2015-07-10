# -*- coding: utf-8 -*-
"""
This module contains the tool of esoth.wow
"""
import os
from setuptools import setup, find_packages

version = '2.0'

tests_require=['zope.testing']

setup(name='esoth.wow',
      version=version,
      description="character progression and stuff",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='Esoth',
      author_email='oolitegroove@gmail.com',
      url='https://github.com/esoth/esoth.wow',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['esoth', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'esoth.wow.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )

