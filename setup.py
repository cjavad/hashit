from setuptools import setup
from hashit.version import __version__

LONG_DES = open("README.rst", "r").read()

setup(
    name = "hashit",
    author = "Javad Shafique",
    author_email = "javadshafique@hotmail.com",
    version=__version__,
    license="MIT",
    include_package_data=True,
    test_suite="tests",
    zip_safe=True,
    entry_points = {
        "console_scripts":[
            "hashit = hashit.__main__:main"
        ]
    },
    url="https://github.com/JavadSM/hashit",
    packages=["hashit"],
    description = "Hashing Application with muliple modes, settings and more!",
    long_description = LONG_DES,
    classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators"
    ]
)
