import sys, platform
from setuptools import setup, find_packages

OS = platform.system()

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "flask",
    "flask-sqlalchemy",
    "sqlalchemy",
    "python-dotenv",
    "stringcase",
    "black",
]

if "PyPy" in sys.version:
    requirements.append("psycopg2cffi")
else:
    if OS == "Darwin" or OS == "Linux":
        requirements.append("psycopg2-binary")
    else:
        requirements.append("psycopg2")

setup_requirements = ["setuptools_git"]

test_requirements = ["pytest", "faker", "factory_boy", "sqlalchemy_utils"]


setup(
    author="Lunatic Labs",
    author_email="lunaticlabs@lipscomb.edu",
    classifiers=[
        "Development Status :: 1 Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    description="DataWarehouse",
    install_requires=requirements + test_requirements,
    long_description=readme,
    incluse_package_data=True,
    name="DataWarehouse",
    packages=find_packages(),
    setup_requires=setup_requirements,
    version="0.0.1",
    zip_safe=False,
    tests_require=test_requirements,
    extras_require={"dev": requirements + test_requirements},
)
