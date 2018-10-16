from setuptools import setup, find_packages

version = '0.0.2'
setup(
    name="tacli",
    version=version,
    description="TA Command Line Interface",
    long_description="UW-Madison CS301 TA cli",
    keywords='tacli',
    author='Anthony',
    author_email="arebello@wisc.edu",
    url="https://github.com/algrebe/tacli", # TODO change this
    download_url="https://github.com/algrebe/tacli/tarball/%s" % version, # TODO change this url
    license='MIT License',
    install_requires=[
        "colorama",
        "structlog",
        "requests",
        "boto3",
    ],
    package_dir={'tacli': 'tacli'},
    packages=find_packages('.', exclude=['tests*']),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': ['tacli=tacli.cli:main'],
    },
)
