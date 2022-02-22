import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pydit",
    version="0.1.0",
    description="Data munging/validation functions for an Internal Audit use case",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jcresearch/reader",
    author="JCreseach",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pydit"],
    include_package_data=True,
    install_requires=["pandas", "numpy"],
    entry_points={
        ]
    },
)