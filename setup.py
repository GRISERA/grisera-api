from setuptools import setup, find_packages

VERSION = '0.0.39.7'
# VERSION = '0.0.40.dev0'
DESCRIPTION = 'Grisera-api package'
LONG_DESCRIPTION = 'Graph Representation Integrating Signals for Emotion Recognition and Analysis (GRISERA) framework provides a persistent model for storing integrated signals and methods for its creation.'

# Setting up
setup(
    name="grisera",
    version=VERSION,
    author="",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'fastapi~=0.94.1',
        'uvicorn[standard]',
        'requests~=2.28.2',
        'fastapi-utils',
        'pydantic~=1.10.6',
        'starlette~=0.26.1',
        'pyjwt',
        'cryptography~=44.0.0',
        'setuptools~=75.6.0',
        'minio~=7.1.0',
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
