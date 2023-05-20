
## Useful git commands

### to add to a previous commit without new messages etc.
git commit --amend --no-edit --all 

### To remove a folder from git
git commit -m "Removed folder from repository"
git rm -r --cached _autosummary
git push origin master


### To Build the documentation locally
rm -r ./docs/source/_autosummary/*   #delete the content of ./docs/source/_autosummary
sphinx-build ./docs/source ./docs/build  -a


## To publish the package
 ensure we are in the right environment!!!
conda activate pydit

* update version in pyproject.toml
* run black . from the terminal to reformat everything
* update version in ./setup.cfg
* update version in ./CHANGELOG.md
* update version in ./docs/source/conf.py
* update version in ./pydit/__init__.py
* update any change in requirements in the README.md
poetry publish --build # or poetry build and then poetry publish

## Update RTD
Go to 
https://readthedocs.org/projects/pydit/builds/17220399/
And refresh from there as it would point to the current GitHub repo
Note that there is a .readthedocs.yaml that links to the package requirements,
so you need to keep requirements.txt updated too.



## Other configs
Ensure you have 
$ cat .condarc
channel_priority: strict
channels:
  - conda-forge
  - defaults