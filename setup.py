from setuptools import setup, find_packages

setup(
    name="rocky-cli",
    version="0.1.0-beta",
    description="Rocky — your Eridian terminal companion from Project Hail Mary",
    author="Elitsuv",
    packages=find_packages(),
    py_modules=["rocky"],          
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "rocky=rocky:main",
        ],
    },
)