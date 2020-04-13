import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lookml",
    version="2.0.0",
    author="Russell Garner",
    author_email="russelljgarner@gmail.com",
    description="A pythonic api for programatically manipulating LookML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llooker/lookml",
    packages=setuptools.find_packages(),
    install_requires=[
        "lkml >= 0.2.2",
        "PyGithub >= 1.47"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
