# Release Procedure

- Update CHANGELOG.md with new release
- Increment version in pyproject.toml
- Commit and push changes
- Create pull request
- Merge pull request to main
- Switch to main branch
- Build distribution with command `py -m build`
- Upload to PyPI with command `py -m twine upload dist/*`
  - This step requires appropriate keys to be setup to upload
  - If necessary you can upload to the test PyPI with the command `py -m twine
    upload --repository testpypi dist/*`
- Verify the upload was successful at https://pypi.org/project/metno-locationforecast/
- Create release on GitHub
  - Create a new tag on release in the format of 'v2.1.0'
  - Title should be the version number in the format of 'v2.1.0'
  - Body should be the text from the CHANGELOG
  - Attach tar.gz and whl distributable files from dist folder

For more information on packaging Python projects see
https://packaging.python.org/en/latest/tutorials/packaging-projects/.
