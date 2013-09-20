from setuptools import setup, find_packages

version = '0.0.0.2'

setup(name='tomcom.buildout.scripts',
      version=version,
      description='buildout helper scripts',
      long_description=open("README.md").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "Intended Audience :: Other Audience",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        ],
      keywords='buildout helper',
      author='tomcom GmbH',
      author_email='info@tomcom.de',
      url='https://pypi.python.org/pypi/tomcom.buildout.scripts',
      license='GPL version 2',
      packages=find_packages(),
      namespace_packages=['tomcom','tomcom.buildout'],
      include_package_data=True,
      install_requires=[
        'setuptools'
      ],
      extras_require={'test': [
        'collective.testcaselayer',
      ]},
      entry_points={
          'console_scripts': ['upgrade_version=tomcom.buildout.scripts.upgrade_version:main',
                             'pin_version=tomcom.buildout.scripts.pin_version:main',
                             'cleanup_eggs=tomcom.buildout.scripts.cleanup_eggs:main',
                             ]
        },
      platforms='Any',
      zip_safe=False,
)