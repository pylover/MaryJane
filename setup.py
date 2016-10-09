
from setuptools import setup, find_packages
import os.path
import re

# reading package's version (same way sqlalchemy does)
with open(os.path.join(os.path.dirname(__file__), 'maryjane', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

long_description = """
Maryjane is a Python automatic file merge tool.
Docs at http://github.com/pylover/maryjane.
"""

setup(
    name='maryjane',
    version=package_version,
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    url='http://github.com/pylover/maryjane',
    description='Python file watcher and task manager',
    long_description=long_description,
    install_requires=['watchdog'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'maryjane = maryjane:main'
        ]
    },
    license='WTFPL',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Utilities'
        ]
    )
