from setuptools import setup
from setuptools import setup, find_packages, __version__ as setuptools_version

setup(
    name='ConfigManager',
    version='0.1',
    packages=find_packages(),
    url='',
    license='',
    author='leixu',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[

    ],
    python_requires='>=3.5',
    author_email='lei.xu@grandhonor.com.cn',
    description='A lib easy to load config.'
)

