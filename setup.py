from setuptools import find_packages, setup

setup(
    name="recom",
    version="1.0.0",
    packages=find_packages(),
    maintainer='michael',
    description="show the 365company's data",
    install_requires=[
        'flask',
        'urllib3',
        'numpy',
        'pandas',
        'cx_Oracle'
    ]
)
