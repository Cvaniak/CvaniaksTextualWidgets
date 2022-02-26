from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ck-widgets",
    version="0.4.0",
    description="Package with widgets and components for Textual TUI Framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/Cvaniak/CvaniaksTextualWidgets",
    author="Cvaniak",
    author_email="igna.cwaniak@gmail.com",
    packages=find_packages(exclude=["not/"]),
    install_requires=["rich", "textual"],
)
