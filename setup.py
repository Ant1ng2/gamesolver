import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gamesolver", # Replace with your own username
    version="0.0.2",
    author="Anthony Ling",
    author_email="acling2k@gmail.com",
    description="A solver of 2-player games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ant1ng2/Gamesolver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
