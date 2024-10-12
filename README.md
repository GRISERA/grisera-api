# GRISERA API
Graph Representation Integrating Signals for Emotion Recognition and Analysis (GRISERA) framework provides a persistent model for storing integrated signals and methods for its creation. 
This project is an api library of the Grisera project. It is added as an requirement to all implementations of Grisera backend service.

To upload new versions:
1. `python3 setup.py sdist bdist_wheel`
2. `twine upload dist/*`
   1. if you don't have twine installed then: `pip3 install twine`
   2. if you are publishing it for testing purposes use `twine upload -r testpypi dist/*`

In powershell you can use oneliner `Remove-Item dist\* ; python setup.py sdist bdist_wheel ; twine upload dist/*`
or if you want to publish to testing pypi `Remove-Item dist\* ; python setup.py sdist bdist_wheel ; twine upload -r testpypi dist/*`

Remember that to publish new version it must have changed version in `setup.py` and all old versions (already uploaded) must be deleted from `dist` folder (both `.tar.gz` and `.whl`)
