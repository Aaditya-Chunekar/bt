from setuptools import setup, find_packages

setup(
    name="bt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["yfinance", "pandas"],
    entry_points={"console_scripts": ["bt=bt.__main__:main"]},
)
