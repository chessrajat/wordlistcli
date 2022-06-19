from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="wordlistcli",
    author="Drag0",
    version="0.1.0",
    url="https://github.com/chessrajat/wordlistcli",
    description="A command line tool to search and download pre-made wordlist from online archives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="wordlists, discovery, fuzzing",
    packages=["."],
    data_files=[(".", ["source.json"])],
    install_requires=["requests", "termcolor"],
     entry_points={
        "console_scripts": [
            "wordlistcli = wordlistcli:main",
        ],
    }

)