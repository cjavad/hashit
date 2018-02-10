from setuptools import setup
from hashit.version import __version__

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
    description = "Hashing Application with muliple modes, settings and more! Hashit, is an hashing application used as an verification tool, intendet to replace the 'standard' linux hashing utilities such as md5sum, sha1sum and so on. One of the main reasons why this program was develop was to create an easy-to-use command line tool for newcomers and professionals alike to hash/verify files and other data. For more see our homepage at https://javadsm.github.io/hashit",
    long_description = open("README.rst", "r").read(),
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
