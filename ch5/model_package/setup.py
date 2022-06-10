from churn_model.model import __version__
from setuptools import setup
from os import path

# Get the long description from the README file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='churn_model',
    version=__version__,
    description='A simple ML model example project.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='xx',
    author='xx',
    author_email='xx@email',
    py_modules=["churn_model"],
    packages=["churn_model"],
    install_requires=[
        'schema==0.7.0'
    ],
    package_data={'churn_model': [
        'model_files/model.pkl',
        'model_files/transformer.pkl'
    ]},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'churn_model=churn_model',
        ]
    }
)