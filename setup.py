import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup_requires = [
    ]

install_requires = [
    'networkx',
    'matplotlib',
    'scipy',
    'gensim',
    'scikit-learn'
    ]

with open('LICENSE') as f:
    license = f.read()

setup(
    name="coredottext",
    version="0.0.1",
    author="Core.Today",
    author_email="help" "@" "core.today",
    description=("Text Mining Tool"),
    license=license,
    keywords="CoreDotToday Text Mining Library",
    url="http://packages.python.org/coredottext",
    install_requires=install_requires,
    setup_requires=setup_requires,
    packages=find_packages(),
    long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
    ],
)
