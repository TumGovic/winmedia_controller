from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="winmedia_controller",
    version="1.1",
    author="TumGovic",
    author_email="ygmweuaw2@gmail.com",
    description="Windows System Media Controller with Async Support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TumGovic/winmedia_controller",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "keyboard>=0.13.5"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.7",
)