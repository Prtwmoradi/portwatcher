from setuptools import setup, find_packages

setup(
    name="portwatcher",  # Package name
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here
    entry_points={
        "console_scripts": [
            "portwatcher=portwatcher.main:main",  # Command-line usage
        ],
    },
)
