from setuptools import setup, find_packages
import os

version = '1.3.1'

tests_require = [
    'ftw.builder',
    'ftw.testbrowser >= 1.22.0',
    'ftw.testing',
    'plone.app.testing',
    'unittest2',
]


setup(name='ftw.raven',
      version=version,
      description="Plone integration for raven / sentry.",
      long_description=open("README.rst").read() + "\n" + open(
          os.path.join("docs", "HISTORY.txt")).read(),

      classifiers=[
          "Environment :: Web Environment",
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
          "Intended Audience :: Developers",
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],

      keywords='ftw raven plone',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.raven',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,


      install_requires=[
          'Plone',
          'ftw.upgrade',
          'plone.memoize',
          'raven',
          'setuptools',
          'yolk',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """)
