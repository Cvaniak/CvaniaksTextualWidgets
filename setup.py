from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ck-widgets",
    version="0.1",
    description="Package with widgets and components for Textual TUI Framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cvaniak",
    author_email="igna.cwaniak@gmail.com",
    packages=["ck_widgets"],
    install_requires=["rich", "textual"],
)
